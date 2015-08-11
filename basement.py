#!/usr/bin/env python3
import fov
import generate
from actor import Player, MovementObstructed
from level import InfiniteMatrix


class Basement:
    MOVEMENT = dict(h=(-1, 0), j=(0, 1), k=(0, -1), l=(1, 0))

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.level = generate.caverns(24, 200)
        self.level_memory = InfiniteMatrix(10, lambda x, y: ' ')
        self.player = Player(self.level[0, 0])

    def draw(self):
        height, width = self.stdscr.getmaxyx()
        self.stdscr.clear()
        self.stdscr.addstr(self.level_memory.view(self.player.x - width // 2, self.player.y - height // 2, self.player.x + width // 2, self.player.y + height // 2))
        self.stdscr.move(0, 0)
        if self.player.tile.items:
            for item in self.player.tile.items:
                self.stdscr.addstr(item.name + "\n")
        self.stdscr.move(height // 2, width // 2)

    def see(self, x, y):
        self.level_memory[x, y] = self.player.level[x, y].symbol

    def run(self):
        while True:
            fov.fieldOfView(self.player.x, self.player.y, 10, see, lambda x, y: not self.player.level[x, y].is_passable)
            self.draw()
            c = chr(self.stdscr.getch())
            if c == 'q':
                self.stdscr.addstr(0, 0, "Really quit? [yN] ")
                if chr(self.stdscr.getch()).lower() == 'y':
                    return
            elif c in 'hjkl':
                dxy = self.MOVEMENT[c]
                try:
                    self.player.move_by(*dxy)
                except MovementObstructed:
                    pass


def main(stdscr):
    Basement(stdscr).run()


if __name__ == '__main__':
    from curses import wrapper
    wrapper(main)
