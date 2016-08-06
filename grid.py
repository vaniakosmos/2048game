from tile import Tile
from vector import Vector
from random import random
from math import floor
from utils import Logger


class Grid(object):
    def __init__(self, size):
        self.size = size
        self.cells = self.empty()
        self.logger = Logger()

    def empty(self):
        return [[None] * self.size for _ in range(self.size)]

    def from_state(self, state):
        """ in case of using saved state of game
            currently function is redundant
        """
        cells = self.empty()
        for x in range(self.size):
            for y in range(self.size):
                tile = state[x][y]
                cells[x][y] = Tile(tile.pos, tile.value) if tile else None
        return cells

    def random_available_cell(self):
        cells = self.available_cells()
        if len(cells):
            return cells[floor(random() * len(cells))]

    def available_cells(self):
        cells = []
        self.for_each_cell(lambda x, y, tile:
                           cells.append(Vector(x, y)) if not tile else None)
        return cells

    def for_each_cell(self, callback):
        for x in range(self.size):
            for y in range(self.size):
                callback(x, y, self.cells[x][y])

    def cells_available(self, cell=None):
        if cell is None:
            return bool(len(self.available_cells()))
        else:
            return not self.cell_occupied(cell)

    def cell_occupied(self, cell):
        return bool(self.cell_content(cell))

    def cell_content(self, cell):
        if self.within_bounds(cell):
            return self.cells[cell.x][cell.y]
        else:
            return None

    def insert_tile(self, tile):
        self.logger.add_log('+ insert {}'.format(tile))
        self.cells[tile.pos.x][tile.pos.y] = tile

    def remove_tile(self, tile):
        self.logger.add_log('- remove {}'.format(tile))
        self.cells[tile.pos.x][tile.pos.y] = None

    def within_bounds(self, position):
        return (0 <= position.x < self.size and
                0 <= position.y < self.size)
