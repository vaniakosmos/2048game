from random import randint
import os
from getch import getch
import argparse


DEFAULT_GRID_SIZE = 4


class Game(object):
    def __init__(self, size=4):
        self.size = size
        self.zeros_left = size * size
        self.grid = [[0] * self.size for _ in range(self.size)]
        self.table_len = size * size

    def show_table(self):
        for row in self.grid:
            print(' '.join(map(
                lambda e: '.'.center(5, ' ') if e == 0 else '%s' % str(e).center(5, ' '),
                row)))
            print()
        print()

    def set_random_tile(self):
        if self.zeros_left == 0:
            return
        needed_free_pos = randint(0, self.zeros_left-1)
        value = 1 if randint(0, 2) < 2 else 2

        free_pos = 0
        for i in range(self.table_len):
            y, x = i // self.size, i % self.size
            if self.grid[y][x] == 0:
                if free_pos == needed_free_pos:
                    self.grid[y][x] = value
                    break
                free_pos += 1
        self.zeros_left -= 1

    def horizontal_shift(self, direction):
        is_left = direction == 'a'
        x_range = range(self.size) if is_left else range(self.size-1, -1, -1)
        x_i = 0 if is_left else self.size-1
        x_dir = -1 if is_left else 1

        table = [[0] * self.size for _ in range(self.size)]
        for y in range(self.size):
            last, upgraded, i = -1, False, x_i
            for x in x_range:
                e = self.grid[y][x]
                if e != 0 and last == e and not upgraded:
                    table[y][i + x_dir] = e * 2
                    upgraded = True
                    self.zeros_left += 1
                elif e != 0:
                    table[y][i] = e
                    last = e
                    upgraded = False
                    i -= x_dir

        self.grid = table.copy()

    def vertical_shift(self, direction):
        is_left = direction == 'w'
        y_range = range(self.size) if is_left else range(self.size - 1, -1, -1)
        y_i = 0 if is_left else self.size - 1
        y_dir = -1 if is_left else 1

        grid = [[0] * self.size for _ in range(self.size)]
        for x in range(self.size):
            last, upgraded, i = -1, False, y_i
            for y in y_range:
                e = self.grid[y][x]
                if e != 0 and last == e and not upgraded:
                    grid[y + y_dir][x] = e * 2
                    upgraded = True
                    self.zeros_left += 1
                elif e != 0:
                    grid[i][x] = e
                    last = e
                    upgraded = False
                    i -= y_dir

        self.grid = grid.copy()

    def game_over(self):
        if self.zeros_left > 0:
            return False
        for y in range(self.size):
            for x in range(self.size-1):
                if self.grid[y][x] == self.grid[y][x+1]:
                    return False
        for x in range(self.size):
            for y in range(self.size-1):
                if self.grid[y][x] == self.grid[y+1][x]:
                    return False
        return True

    @staticmethod
    def get_command():
        command = ''
        while command == '':
            try:
                command = getch()
            except OverflowError:
                print('change keyboard layout')
        return command

    def game_loop(self):
        command = ''
        self.set_random_tile()
        while command != 'q':
            if self.game_over():
                print('GAME OVER')
                break
            os.system("clear")
            self.set_random_tile()
            self.show_table()

            command = Game.get_command()
            while command != 'q':
                if command in ('a', 'd'):
                    self.horizontal_shift(command)
                    break
                elif command in ('w', 's'):
                    self.vertical_shift(command)
                    break
                else:
                    print('try to use WASD')
                    command = Game.get_command()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--size", help="grid size",
                        type=int, default=DEFAULT_GRID_SIZE)
    args = parser.parse_args()

    gm = Game(size=args.size)
    gm.game_loop()


if __name__ == '__main__':
    main()
