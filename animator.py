from time import sleep
from tile import Tile
from vector import Vector
from grid import Grid
import os

SLEEP_TIME = 0.5


class Animator:
    cell_v_size = 3  # better to use even number
    cell_h_size = cell_v_size * 2 + 1

    ft_colors = [30 + i for i in range(8)]  # font colors 30-37, white -> black
    bg_colors = [41 + i for i in range(8)]  # background colors 40-47, black -> white

    values = [2 ** i for i in range(1, 12)]  # 1-2048

    h_gap = 1  # ' ' * gap
    v_gap = 1  # '\n' * gap

    def __init__(self, grid, fps):
        self.grid = grid
        self.events = {'move': [],
                       'merge': [],
                       'add': [Tile(Vector(1, 1), 64), Tile(Vector(1, 3), 128)]}
        self.state = None

    @staticmethod
    def map_value(value):
        return Animator.bg_colors[Animator.values.index(value) % len(Animator.bg_colors)]

    @staticmethod
    def esc_color_char(bg_color, ft_color):
        return '\033[{}m'.format(';'.join(['1', str(ft_color), str(bg_color)]))

    @staticmethod
    def coloring(tile_value, what_to_print):
        return (Animator.esc_color_char(Animator.map_value(tile_value), 30) +
                what_to_print +
                '\033[0m')

    @staticmethod
    def coloring_empty():
        return Animator.esc_color_char(40, 30) + ' \033[0m'

    @staticmethod
    def center(thing, length, fill_char):
        a = length - (len(thing) - 14)
        b = a // 2
        return [fill_char] * b + [thing] + [fill_char] * (a - b)

    def save_state(self):
        state = [[] for _ in range(self.grid.size * self.cell_v_size)]
        for x in range(self.grid.size):
            for i in range(self.cell_v_size):
                line_num = x * self.cell_v_size + i
                for y in range(self.grid.size):
                    tile = self.grid.cells[x][y]

                    if tile:
                        cs = self.coloring(tile.value, ' ')
                        cv = self.coloring(tile.value, str(tile.value))
                    else:
                        cs = cv = self.coloring_empty()  # empty cell

                    if i == self.cell_v_size // 2:
                        chunk = ([cs] * self.cell_h_size if not tile else
                                 Animator.center(cv, self.cell_h_size, cs))
                    else:
                        chunk = [cs] * self.cell_h_size

                    state[line_num] += list(chunk)
        self.state = state.copy()

    def move(self):
        events = []
        move_events = [[Vector(1, 1), Vector(1, 0)], [Vector(2, 2), Vector(2, 0)]]
        for vectors in move_events:
            vec_from, vec_to = vectors
            event = {'h': None, 'steps': []}
            signum = lambda x: -1 if x > 0 else (0 if x == 0 else 1)
            if vec_from.x != vec_to.x:
                event['h'] = False
                event['steps'] = [vec_from + i * Vector(signum(vec_from.x - vec_to.x), 0)
                                  for i in range(abs(vec_from.x - vec_to.x) + 1)]
                event['steps'].reverse()
            else:
                event['h'] = True
                # event['steps'] = [vec_from + i * Vector(0, signum(vec_from.y - vec_to.y))
                #                   for i in range(abs(vec_from.y - vec_to.y) + 1)]
                # event['steps'].reverse()
                event['steps'] = list(range(vec_to.y * self.cell_h_size,
                                            vec_from.y * self.cell_h_size))

            print(event['steps'])
            print()
            events.append(event)

        # for _ in range(10):
        #     os.system("clear")
        #     self.show_grid()
        #     steps = []
        #     for event in events:
        #         steps.append({'step': event['steps'].pop() if event['steps'] else None,
        #                       'h': event['h']})
        #     for line in self.state:
        #         for step in steps:
        #             if step['h'] and step['step']:
        #                 print(step['step'])
        #
        #             elif step['step']:
        #                 pass
        #     sleep(SLEEP_TIME)

    def show_grid(self):
        os.system("clear")
        self.save_state()
        print()
        for line in self.state:
            print('' + ''.join(line))
        print()


# def normal_tile(grid, x, y, i):
#     tile = grid.cells[x][y]
#
#     if i == 0:
#         print('+{}+'.format('-' * (cell_h_size - 2)), end=h_gap)
#     elif i == cell_v_size - 1:
#         print('+{}+'.format('-' * (cell_h_size - 2)), end=h_gap)
#     elif i == cell_v_size // 2:
#         print('|{}|'.format(
#             ' '.center(cell_h_size - 2, ' ') if not tile else
#             coloring(tile.value).center(21 - 2, ' ')), end=h_gap)
#     else:
#         print('|{}|'.format(' ' * (cell_h_size - 2)), end=h_gap)
#
# def colored_tile(grid, x, y, i):
#     tile = grid.cells[x][y]
#
#     if tile:
#         cs = coloring(tile.value, ' ')
#         cv = coloring(tile.value, str(tile.value))
#     else:
#         cs = cv = coloring(1, ' ')
#         # cv = coloring(40, ' ')
#
#     if i == cell_v_size // 2:
#         print(cs * cell_h_size if not tile else
#               center(cv, cell_h_size, cs), end=' ' * h_gap)
#     else:
#         print(cs * cell_h_size, end=' ' * h_gap)
#
#
# def show_grid(grid):
#     for x in range(grid.size):
#         for i in range(cell_v_size):
#             print(end='   ')
#             for y in range(grid.size):
#                 # normal_tile(grid, x, y, i)
#                 colored_tile(grid, x, y, i)
#             print()
#         print('\n' * v_gap, end='')
#
#

def main():
    grid = Grid(3)
    grid.cells[1][1] = Tile(Vector(1, 1), 2)
    grid.cells[2][2] = Tile(Vector(2, 2), 4)
    anim = Animator(grid, 2)
    anim.save_state()
    anim.show_grid()
    anim.move()
    pass

if __name__ == '__main__':
    main()
