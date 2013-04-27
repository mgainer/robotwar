import json
from output import output_module

class Rwjson(output_module.Output):
  """Print the rounds of a battle as JSON"""

  def get_output(self, writable):
    to_dump = {}
    to_dump['map'] = self._json_map()
    to_dump['rounds'] = self._json_rounds()
    writable.write(json.dumps(to_dump))
    #writable.write(' '.join(dir(json)))

  def _json_map(self):
    ret = []
    for row in self._world_map.get_map_rows():
      positions = []
      for terrain in row:
        positions.append(terrain.name)
      ret.append(positions)
    return ret

  def _json_rounds(self):
    ret = []
    for round in self._play_history.rounds:
      round_map = {}
      ret.append(round_map)
      for robot, action in round.actions.iteritems():
        round_map[robot.name] = self._json_action(action)
    return ret

  def _json_action(self, action):
    ret = {}
    ret['starting_health'] = action.starting_health
    ret['ending_health'] = action.ending_health
    ret['starting_position'] = self._json_position(action.starting_position)
    ret['ending_position'] = self._json_position(action.ending_position)
    if action.shot_direction:
      ret['shot_direction'] = self._json_direction(action.shot_direction)
      ret['shot_distance'] = action.shot_distance
    if action.radar_direction:
      ret['radar_direction'] = self._json_direction(action.radar_direction)
    if action.radar_return:
      ret['radar_return'] = self._json_radar_return(action.radar_return)
    if action.move_direction:
      ret['move_direction'] = self._move_direction(action.move_direction)
    ret['damage_dealt'] = []
    for damage in action.damage_dealt:
      ret['damage_dealt'].append(self._json_damage(damage))
    ret['damage_taken'] = []
    for damage in action.damage_taken:
      ret['damage_taken'].append(self._json_damage(damage))
    return ret

  def _json_position(self, position):
    ret = {}
    ret['x'] = position.x
    ret['y'] = position.y
    return ret

  def _json_direction(self, direction):
    ret = {}
    ret['x_delta'] = direction.x_delta
    ret['y_delta'] = direction.y_delta
    return ret

  def _json_radar_return(self, radar_return):
    ret = {}
    ret['direction'] = self._json_direction(radar_return.direction)
    ret['range'] = radar_return.range
    ret['health'] = radar_return.health
    if radar_return.last_move_direction:
      ret['last_move_direction'] = self._json_direction(
          radar_return.last_move_direction)
      ret['last_move_distance'] = radar_return.last_move_distance
    return ret

  def _json_damage(self, damage):
    ret = {}
    ret['amount'] = damage.amount
    ret['description'] = damage.description
    return ret
