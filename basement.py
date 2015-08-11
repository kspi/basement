#!/usr/bin/env python3
import fov
import generate
from actor import Player, MovementObstructed
from level import InfiniteMatrix
import curses


class Basement:
    MOVEMENT = {
        ord('h'): (-1, 0),
        curses.KEY_LEFT: (-1, 0),
        ord('j'): (0, 1),
        curses.KEY_DOWN: (0, 1),
        ord('k'): (0, -1),
        curses.KEY_UP: (0, -1),
        ord('l'): (1, 0),
        curses.KEY_RIGHT: (1, 0),
    }

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.level_memory = InfiniteMatrix(10, lambda x, y: ' ')

        caverns = generate.caverns(24, 2000)
        self.player = Player(caverns[0, 0])

    def act(self):
        pass

    def ask(self, question):
        prevcursor = self.stdscr.getyx()
        self.stdscr.move(self.msgcursor[0], self.msgcursor[1])
        self.stdscr.addstr(question + " ")
        c = chr(self.stdscr.getch())
        self.stdscr.addstr(c)
        self.msgcursor = self.stdscr.getyx()
        self.stdscr.move(*prevcursor)
        return c

    def message(self, msg):
        prevcursor = self.stdscr.getyx()
        self.stdscr.move(self.msgcursor[0], self.msgcursor[1])
        self.stdscr.addstr(msg + "\n")
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
        actcall = self.player.level.act()
        while True:
            fov.fieldOfView(self.player.x, self.player.y, 10, self.see, lambda x, y: not self.player.level[x, y].is_passable)
            self.draw()
            key = self.stdscr.getch()
            if key == ord('q'):
                if self.ask("Really quit? [yN]").lower() == 'y':
                    return
            elif key in self.MOVEMENT:
                delta = self.MOVEMENT[key]
                try:
                    self.player.move_by(*delta)
                except MovementObstructed:
                    pass
                next(actcall)


def main(stdscr):
    Basement(stdscr).run()


if __name__ == '__main__':
    curses.wrapper(main)
