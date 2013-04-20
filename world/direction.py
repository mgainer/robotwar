import collections

DirectionTuple = collections.namedtuple(
    'DirectionTuple', ['x_delta', 'y_delta'])
class Direction(DirectionTuple):

  def __new__(cls, x, y):
    # Restrict deltas to being -1, 0, or 1 only.
    return DirectionTuple.__new__(cls, cmp(x,0), cmp(y,0))

NORTH = Direction(0, 1)
SOUTH = Direction(0, -1)
EAST = Direction(1, 0)
WEST = Direction(-1, 0)
NORTHWEST = Direction(-1, 1)
NORTHEAST = Direction(1, 1)
SOUTHEAST = Direction(1, -1)
SOUTHWEST = Direction(-1, -1)
