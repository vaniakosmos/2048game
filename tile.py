class Tile(object):
    def __init__(self, position, value):
        self.pos = position
        self.value = value

        self.previous_pos = None
        self.merged_from = None

    def save_position(self):
        self.previous_pos = self.pos

    def update_pos(self, pos):
        self.pos = pos

    def __str__(self):
        return '<tile {}, value: {}>'.format(str(self.pos), self.value)
