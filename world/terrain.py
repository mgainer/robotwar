import collections
import os

class NamedTupleToJson:
  def simple(self):
    return self.__dict__

class Terrain(NamedTupleToJson, collections.namedtuple(
    'TerrainTuple',
    [
        'name',
        'symbol',
        'can_move_onto',
        'can_radar_through',
        'can_shoot_through',
        ])):

  def __str__(self):
    return self.symbol

WALL = Terrain('wall', '#', False, False, False)
PLAINS = Terrain('plains', ' ', True, True, True)

terrain_by_symbol = {
  WALL.symbol: WALL,
  PLAINS.symbol: PLAINS,
}


# TODO(anybody): Using space characters for plains is a lot less cluttered
# visually, but makes it hard to edit maps.  Change character, or allow a
# different character to be used when editing maps versus displaying them.

class TerrainMap:
  def __init__(self, map_text, map_name):
    """Initialize a terrain map from text.

    Note that map data is stored as rows (as it was read from the file)
    which makes printing things out simple and convenient, but necessitates
    looking up things as row-primary, meaning code like self._map[y][x], which
    is counter-intuitive enough to merit mention.

    Map coordinates are specified as (0,0) being the upper-leftmost corner.

    Args:
      map_text: One big string representing map text, as if read from a file.
        Rows are terminated by newlines.
    """

    self._map = self._read_map(map_text, map_name)

  def _read_map(self, map_text, map_name):
    # Parse map rows
    rows = []
    for line in map_text.split('\n'):

      # TODO(anybody): Introduce a comment character so maps can contain
      # remarks as well as terrain definitions.
      if len(line) == 0:
        continue   # Skip leading or trailing blank lines.
      row = []
      rows.append(row)
      for symbol in line:
        if symbol in terrain_by_symbol:
          row.append(terrain_by_symbol[symbol])
        else:
          raise RuntimeError('Error: Unrecognized map symbol "%s" in map %s' %
                             (symbol, map_name))

    # Surround whole map with walls, to simplify logic of main world.
    # Also right-pad any ragged rows to full width.
    max_len = 0
    for row in rows:
      max_len = max(max_len, len(row))
    for row in rows:
      row.insert(0, WALL)
      row.append(WALL)
      while len(row) < max_len + 2:
        row.append(WALL)
    bounding_row = [WALL] * (max_len + 2)
    rows = [bounding_row] + rows + [bounding_row]
    return rows

  # returns a Terrain
  def get(self, position):
    return self._map[position.y][position.x]

  def get_xy(self, x, y):
    return self._map[y][x]

  @property
  def width(self):
    return len(self._map[0])

  @property
  def height(self):
    return len(self._map)

  def get_map_array(self):
    """Get a printable map of the terrain.

    Return:
      List of rows,
        each containing a list of symbol characters for each column
    """
    width = len(self._map[0])
    height = len(self._map)
    map_array = []
    for y in range(height):
      line = []
      for x in range(width):
        line.append(str(self._map[y][x]))
      map_array.append(line)
    return map_array

  def dump(self):
    for line in self.get_map_array():
      print ' '.join(line)

  def __eq__(self, other):
    return self._map == other._map

  def simple(self):
    return self._map

def read_map(map_name):
  """Reads text of map from file.

  This function is separate from the main body of the TerrainMap class to
  simplify unit testing.  Rather than always reading from the maps/
  subdirectory, tests can just define their own map text within the body
  of the test itself.

  Args:
    map_name
  Returns:
    Text of the file as read from the maps/ directory.
  """

  fp = open(os.path.join('maps', map_name))
  text = fp.read()
  fp.close()
  return text
