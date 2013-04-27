from output import output_module
from output import text

class Ascii(output_module.Output):
  """Print the rounds of a battle as ASCII graphics."""

  def output(self, writable):
    """Print the rounds of a battle as ASCII graphics."""

    for number, play_round in enumerate(self._play_history.rounds):
      writable.write("===================== Round %d ===================\n" %
                     number)

      self._print_map(writable, play_round.actions, 'starting')
      for robot, action in play_round.actions.iteritems():
        writable.write("Robot " + str(robot) + "------------------------\n")
        text.write_action(writable, action)
      self._print_map(writable, play_round.actions, 'ending')


  def _print_map(self, writable, actions, position_type):
    """Print out a textual map of the game

    Args:
      writable: The writable object to which to print.
      actions: The map of robot -> actions-this-round
      position_type:
        'starting' to print robots in starting position
        'ending' to print robots in ending position
    """
    map_array = self._world_map.get_map_array()
    for robot, robot_data in actions.iteritems():
      if position_type == 'starting':
        pos = robot_data.starting_position
      else:
        pos = robot_data.ending_position
      map_array[pos.x][pos.y] = chr(ord('0') + robot.get_id_number())

    for y in range(0, self._world_map.height):
      for x in range(0, self._world_map.width):
        writable.write(str(map_array[x][y]))
        writable.write(' ')
      writable.write('\n')
