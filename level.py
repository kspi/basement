import math
from tile import Tile, Wall


class InfiniteMatrix:
    def __init__(self, block_size, defaultfn):
        self.block_size = block_size
        self.blocks = {}
        self.defaultfn = defaultfn

    def _block(self, x, y):
        b = (x // self.block_size, y // self.block_size)
        if b not in self.blocks:
            self.blocks[b] = [[self.defaultfn(b[0] + bx, b[1] + by) for bx in range(self.block_size)] for by in range(self.block_size)]
        return self.blocks[b]

    def __getitem__(self, xy):
        x, y = xy
        assert(isinstance(x, int))
        assert(isinstance(y, int))
        return self._block(x, y)[x % self.block_size][y % self.block_size]

    def __setitem__(self, xy, value):
        x, y = xy
        assert(isinstance(x, int))
        assert(isinstance(y, int))
        self._block(x, y)[x % self.block_size][y % self.block_size] = value

    def view(self, x0, y0, x1, y1):
        return '\n'.join(
            ''.join(str(self[x, y]) for x in range(x0, x1))
            for y in range(y0, y1)
        )


class Level(InfiniteMatrix):
    BLOCK_SIZE = 10

    def __init__(self):
        super().__init__(self.BLOCK_SIZE, lambda x, y: Wall(self, x, y))
        self.actors = set()

    def act(self):
        time = 0
        schedule = []
        while True:
            time += 100
            in_schedule = set()
            new_schedule = []
            for t, a in self.schedule:
                in_schedule.add(a)
                if t <= self.time:
                    if isinstance(a, Player):
                        yield
                    else:
                        a.act()
                    new_schedule.append((self.time + a.speed, a))
                else:
                    new_schedule.append((t, a))
            for a in self.actors:
                if a not in in_schedule:
                    a.act()
                    new_schedule.append((self.time + a.speed, a))
            self.schedule = sorted(new_schedule)

    @staticmethod
    def from_strings(lines):
        level = Level()
        for y, line in enumerate(lines):
            for x, ch in enumerate(line):
                if ch != ' ':
                    level[x, y] = Tile.from_symbol(ch)(level, x, y)
        return level
