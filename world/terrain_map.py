import os

from world import terrain

class TerrainMap:
  def __init__(self, map_name):
    self._map = self._read_map(map_name)

  def _read_map(self, map_name):
    # Build list of all terrain types:
    terrain_by_symbol = {}
    for terrain_type in terrain.terrain_types:
      if terrain_type.name is 'wall':
        wall = terrain_type
      terrain_by_symbol[terrain_type.symbol] = terrain_type

    fp = open(os.path.join('maps', map_name))
    lines = fp.readlines()
    fp.close()

    # Read in map as rows.
    rows = []
    for line in lines:
      row = []
      rows.append(row)
      for symbol in line.strip():
        if symbol in terrain_by_symbol:
          row.append(terrain_by_symbol[symbol])
        else:
          raise Exception('Error: Unrecognized map symbol "%s" in map %s' %
                          (symbol, map_name))

    # Surround whole map with walls, to simplify logic of main world.
    # Also right-pad any ragged rows to full width.
    max_len = 0
    for row in rows:
      max_len = max(max_len, len(row))
    for row in rows:
      row.insert(0, wall)
      row.append(wall)
      while len(row) < max_len + 2:
        row.append(wall)
    bounding_row = [wall] * (max_len + 2)
    rows = [bounding_row] + rows + [bounding_row]
    return rows

  # returns a Terrain
  def get(self, position):
    return self._map[position.x][position.y]

  def dump(self):
    width = len(self._map[0])
    height = len(self._map)
    for y in range(height):
      for x in range(width):
        print self._map[y][x],
      print
