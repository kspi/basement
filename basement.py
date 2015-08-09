#!/usr/bin/env python3
import functools
import fov
import math


class Object:
    def __str__(self):
        return self.symbol


class MovementObstructed(Exception):
    pass


class Actor(Object):
    def __init__(self, tile):
        assert(not tile.is_occupied)
        tile.actor = self
        self.tile = tile

    @property
    def x(self):
        return self.tile.x

    @property
    def y(self):
        return self.tile.y

    @property
    def level(self):
        return self.tile.level

    def move_to(self, tile):
        if not tile.is_passable or tile.is_occupied:
            raise MovementObstructed
        self.tile.actor = None
        self.tile = tile
        tile.actor = self

    def move_by(self, dx, dy):
        self.move_to(self.level[self.x + dx, self.y + dy])


class Player(Actor):
    symbol = '@'


class Tile(Object):
    def __init__(self, level, x, y):
        self.level = level
        self.x = x
        self.y = y
        self.actor = None
        self.seen = False

    def see(self):
        self.seen = True

    @property
    def is_occupied(self):
        return self.actor is not None

    @classmethod
    def from_symbol(cls, symbol):
        try:
            return cls._symbol_map[symbol]
        except AttributeError:
            cls._symbol_map = {c.symbol: c for c in cls.__subclasses__()}
            return cls._symbol_map[symbol]

    def __str__(self):
        #if not self.seen:
        #    return ' '
        if self.is_occupied:
            return str(self.actor)
        return super().__str__()


class Ground(Tile):
    is_passable = True
    symbol = '.'


class Wall(Tile):
    is_passable = False
    symbol = '#'


class Level:
    BLOCK_SIZE = 10

    def __init__(self):
        self.blocks = {}

    def _block(self, x, y):
        b = (x / self.BLOCK_SIZE, y / self.BLOCK_SIZE)
        if b not in self.blocks:
            self.blocks[b] = [[Wall(self, b[0] + bx, b[1] + by) for bx in range(self.BLOCK_SIZE)] for by in range(self.BLOCK_SIZE)]
        return self.blocks[b]

    def __getitem__(self, xy):
        x, y = xy
        return self._block(x, y)[x % self.BLOCK_SIZE][y % self.BLOCK_SIZE]

    def __setitem__(self, xy, value):
        x, y = xy
        self._block(x, y)[x % self.BLOCK_SIZE][y % self.BLOCK_SIZE] = value

    @staticmethod
    def from_strings(lines):
        level = Level()
        for y, line in enumerate(lines):
            for x, ch in enumerate(line):
                if ch != ' ':
                    level[x, y] = Tile.from_symbol(ch)(level, x, y)
        return level

    @staticmethod
    def generate_caverns(sigma):
        import noise
        def dnorm(x, mu, sig):
            return math.exp(-pow(x - mu, 2.) / (2 * pow(sig, 2.)))
        extent = int(sigma * 1.6)
        level = Level()
        for x in range(-extent, extent):
            for y in range(-extent, extent):
                r = math.sqrt(x * x + y * y)
                n = abs(noise.pnoise2(x / extent, y / extent))
                print(n)
                d = dnorm(r, 0, sigma) * n
                if d > 0.5:
                    level[x, y] = Ground(level, x, y)
                else:
                    level[x, y] = Wall(level, x, y)
        return level

    def view(self, x0, y0, x1, y1):
        return '\n'.join(
            ''.join(str(self[x, y]) for x in range(x0, x1))
            for y in range(y0, y1)
        )


def main(stdscr):
    test_level = Level.from_strings([
        "###########                         ",
        "#.........#    #####################",
        "#.........######...................#",
        "#..................................#",
        "#.........######...................#",
        "###########    #...................#",
        "               #...................#",
        "               #...................#",
        "               #####################",
    ])

    caverns = Level.generate_caverns(10)

    movement = dict(h=(-1, 0), j=(0, 1), k=(0, -1), l=(1, 0))

    player = Player(caverns[0, 0])

    while True:
        fov.fieldOfView(player.x, player.y, 2,
                lambda x, y: player.level[x, y].see(),
                lambda x, y: not player.level[x, y].is_passable)

        height, width = stdscr.getmaxyx()
        stdscr.clear()
        stdscr.addstr(player.level.view(player.x - width // 2, player.y - height // 2, player.x + width // 2, player.y + height // 2))
        stdscr.move(height // 2, width // 2)
        c = chr(stdscr.getch())
        if c == 'q':
            stdscr.addstr(0, 0, "Really quit? [yN] ")
            if chr(stdscr.getch()).lower() == 'y':
                return
        elif c in 'hjkl':
            dxy = movement[c]
            try:
                player.move_by(*dxy)
            except MovementObstructed:
                pass


if __name__ == '__main__':
    from curses import wrapper
    wrapper(main)
