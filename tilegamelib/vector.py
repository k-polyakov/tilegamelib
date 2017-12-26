
class Vector:
    """
    Direction vectors for moves, positions etc.

    Vector objects can be used for simple arithmetics,
    like adding positions to each other.

    They are hashable, unlike NumPy arrays.
    """

    def __init__(self, *args):
        if len(args) == 1:  # tuple
            self.coord = args[0]
        elif len(args) == 2:  # x, y
            self.coord = tuple(args)

    @property
    def x(self):
        return self.coord[0]

    @property
    def y(self):
        return self.coord[1]

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Vector(x, y)

    def __mul__(self, number):
        x = self.x * number
        y = self.y * number
        return Vector(x, y)

    def __iter__(self):
        return self.coord.__iter__()

    def __eq__(self, other):
        if type(other) == type(self):
            if self.x == other.x and self.y == other.y:
                return True

    def __hash__(self):
        return str(self).__hash__()

    def __repr__(self):
        return '[%i;%i]' % (self.x, self.y)


ZERO_VECTOR = Vector([0, 0])
UP = Vector([0, -1])
DOWN = Vector([0, 1])
LEFT = Vector([-1, 0])
RIGHT = Vector([1, 0])
UPLEFT = Vector([-1, -1])
DOWNLEFT = Vector([-1, 1])
UPRIGHT = Vector([1, -1])
DOWNRIGHT = Vector([1, 1])
