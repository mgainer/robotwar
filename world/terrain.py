import collections

class Terrain(collections.namedtuple(
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

terrain_types = [
    Terrain('wall', '#', False, False, False),
    Terrain('plains', '.', True, True, True),
]

# TODO(mgainer): Break down terrain can-do-X as a Capabilities class?
# Might be hard to abstract; semantics are pretty variable.
