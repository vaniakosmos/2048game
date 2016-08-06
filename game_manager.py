from random import random

from grid import Grid
from tile import Tile
from vector import Vector
from animator import Animator
from utils import get_command, yes_no_prompt


class GameManager(object):
    def __init__(self, size, debug_mode, fps):
        self.size = size
        self.debug_mode = debug_mode
        self.grid = Grid(self.size)
        self.fps = fps
        self.animator = Animator(self.grid, self.fps)
        self.score = 0
        self.over = False
        self.won = False
        self.logger = self.grid.logger

        self.add_start_tiles(2)

    def restart(self):
        self.grid = Grid(self.size)
        self.animator = Animator(self.grid, self.fps)
        self.score = 0
        self.over = False
        self.won = False
        self.logger = self.grid.logger

        self.add_start_tiles(2)
        self.game_loop()

    def add_start_tiles(self, n):
        for _ in range(n):
            self.add_random_tile()

    def add_random_tile(self):
        if self.grid.cells_available():
            value = 2 if random() < 0.9 else 4
            tile = Tile(self.grid.random_available_cell(), value=value)

            self.grid.insert_tile(tile)

    def prepare_tiles(self):
        def callback(x, y, tile):
            if tile:
                tile.merged_from = None
                tile.save_position()
        self.grid.for_each_cell(callback)

    def move_tile(self, tile, cell):
        self.logger.add_log('~ move {} to {}'.format(tile, cell))
        self.grid.cells[tile.pos.x][tile.pos.y] = None
        self.grid.cells[cell.x][cell.y] = tile
        tile.update_pos(cell)

    def move(self, direction):
        if self.over:
            return

        vector = GameManager.get_vector(direction)
        traversals = self.build_traversals(vector)
        moved = False

        self.prepare_tiles()

        for x in traversals['x']:
            for y in traversals['y']:
                cell = Vector(x, y)
                tile = self.grid.cell_content(cell)

                if tile:
                    positions = self.find_farther_position(cell, vector)
                    next_tile = self.grid.cell_content(positions['next'])

                    if (next_tile and next_tile.value == tile.value and
                            not next_tile.merged_from):
                        merged = Tile(positions['next'], tile.value * 2)
                        merged.merged_from = [tile, next_tile]

                        self.logger.add_log('+ merge {} and {}'.format(tile, next_tile))

                        self.grid.insert_tile(merged)
                        self.grid.remove_tile(tile)

                        tile.update_pos(positions['next'])

                        self.score += merged.value

                        if merged.value == 2048:
                            self.won = True
                    else:
                        self.move_tile(tile, positions['farthest'])

                    if cell != tile.pos:
                        moved = True
        if moved:
            self.add_random_tile()

            if not self.move_available():
                self.over = True

    @staticmethod
    def get_vector(direction):
        dirs = [Vector(0, -1),  # left
                Vector(1, 0),   # down
                Vector(0, 1),   # right
                Vector(-1, 0)]   # up
        return dirs[direction]

    def build_traversals(self, vector):
        traversals = {'x': [], 'y': []}

        for pos in range(self.size):
            traversals['x'].append(pos)
            traversals['y'].append(pos)

        if vector.x == 1:
            traversals['x'].reverse()
        if vector.y == 1:
            traversals['y'].reverse()

        return traversals

    def find_farther_position(self, cell, vector):
        def do(_cell):
            return _cell, _cell + vector

        previous, cell = do(cell)
        while self.grid.within_bounds(cell) and self.grid.cells_available(cell):
            previous, cell = do(cell)

        return {
            'farthest': previous,
            'next': cell
        }

    def move_available(self):
        return self.grid.cells_available() or self.tile_matches_available()

    def tile_matches_available(self):
        for x in range(self.size):
            for y in range(self.size):
                tile = self.grid.cell_content(Vector(x, y))

                if tile:
                    for d in range(4):
                        vector = GameManager.get_vector(d)
                        cell = tile.pos + vector
                        if not self.grid.within_bounds(cell):
                            continue

                        other = self.grid.cell_content(cell)
                        if not other or other.value == tile.value:
                            return True
        return False

    def show_game_stats(self):
        print('WASD - control, q - quit', end='\t')
        print('Score: {}\n'.format(self.score))

    def game_loop(self):
        directions = {'a': 0, 's': 1, 'd': 2, 'w': 3}

        while True:
            if self.over:
                self.animator.show_grid()
                self.show_game_stats()
                print('\aGAME OVER')
                print('Restart? ', end='')
                if yes_no_prompt():
                    self.restart()
                else:
                    print('(-_o) /')
                break
            self.animator.show_grid()
            self.show_game_stats()
            if self.debug_mode:
                self.logger.print_logs()

            command = get_command()

            while command != 'q':
                if command in 'wasd':
                    self.move(directions[command])
                    break
                else:
                    print('try to use WASD')
                    command = get_command()
            if command == 'q':
                print('Quit? ', end='')
                if yes_no_prompt():
                    print('(-_o) /')
                    break
