#!/usr/bin/env python3
import fov
import generate
from actor import Player, MovementObstructed
from level import InfiniteMatrix


def main(stdscr):
    caverns = generate.caverns(30, 100)

    movement = dict(h=(-1, 0), j=(0, 1), k=(0, -1), l=(1, 0))

    player = Player(caverns[0, 0])
    memory = InfiniteMatrix(10, lambda x, y: ' ')

    while True:
        def see(x, y):
            memory[x, y] = str(player.level[x, y])
        fov.fieldOfView(player.x, player.y, 10, see, lambda x, y: not player.level[x, y].is_passable)

        height, width = stdscr.getmaxyx()
        stdscr.clear()
        stdscr.addstr(memory.view(player.x - width // 2, player.y - height // 2, player.x + width // 2, player.y + height // 2))
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
