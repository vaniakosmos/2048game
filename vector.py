class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)

    def __rmul__(self, a):
        return Vector(a * self.x, a * self.y)
