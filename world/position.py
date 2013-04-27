import collections

class Position(collections.namedtuple('PositionTuple', ['x', 'y'])):

  def move_by(self, direction):
    return Position(self.x + direction.x_delta, self.y + direction.y_delta)

  def __str__(self):
    return "x: %d, y: %d" % (self.x, self.y)
