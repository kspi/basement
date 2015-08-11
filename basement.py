#!/usr/bin/env python3
import fov
import generate
from actor import Player, MovementObstructed
from level import InfiniteMatrix


class Basement:
    MOVEMENT = dict(h=(-1, 0), j=(0, 1), k=(0, -1), l=(1, 0))

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.level_memory = InfiniteMatrix(10, lambda x, y: ' ')

        caverns = generate.caverns(24, 200)
        self.player = Player(caverns[0, 0])

    def ask(self, question):
        self.stdscr.addstr(self.msgcursor[0], self.msgcursor[1], question + " ")
        c = str(self.stdscr.getch())
        self.msgcursor = self.stdscr.getyx()
        self.message(c)
        c = str(self.stdscr.getch())
        return c

    def message(self, msg):
        prevcursor = self.stdscr.getyx()
        self.stdscr.addstr(self.msgcursor[0], self.msgcursor[1], msg + "\n")
        self.msgcursor = self.stdscr.getyx()
        self.stdscr.move(*prevcursor)

    def draw(self):
        height, width = self.stdscr.getmaxyx()
        self.stdscr.clear()
        self.stdscr.addstr(self.level_memory.view(self.player.x - width // 2, self.player.y - height // 2, self.player.x + width // 2, self.player.y + height // 2))
        self.msgcursor = (0, 0)
        if self.player.tile.items:
            self.message("You see here:")
            for item in self.player.tile.items:
                self.message("    " + item.name)
        self.stdscr.move(height // 2, width // 2)

    def see(self, x, y):
        self.level_memory[x, y] = self.player.level[x, y].symbol

    def run(self):
        while True:
            fov.fieldOfView(self.player.x, self.player.y, 10, self.see, lambda x, y: not self.player.level[x, y].is_passable)
            self.draw()
            c = chr(self.stdscr.getch())
            if c == 'q':
                if self.ask("Really quit? [yN]").lower() == 'y':
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
