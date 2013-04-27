from output import output_module

class Text(output_module.Output):
  """Print the rounds of a battle as text."""

  def output(self, writable):
    """Print the rounds of a battle as text."""

    for number, play_round in enumerate(self._play_history.rounds):
      writable.write("===================== Round %d ===================\n" %
                     number)

      for robot, action in play_round.actions.iteritems():
        writable.write("-------- Robot " + str(robot) + "---------\n")
        write_action(writable, action)


def write_action(writable, action):
  if action.starting_health == action.ending_health:
    writable.write("health: %d\n" % action.starting_health)
  else:
    writable.write("starting_health: %3d\n" % action.starting_health)
    writable.write("ending_health:   %3d\n" % action.ending_health)
  if action.starting_position == action.ending_position:
    writable.write("position: %s\n" % str(action.starting_position))
  else:
    writable.write("starting_position: %s\n" % str(action.starting_position))
    writable.write("ending_position:   %s\n" % str(action.ending_position))
  if action.shot_direction:
    writable.write("shot_direction: %s\n" % str(action.shot_direction))
    writable.write("shot_distance: %d\n" % action.shot_distance)
  if action.radar_direction:
    writable.write("radar_direction: %s\n" % action.radar_direction)
  if action.radar_return:
    writable.write("radar_return.direction: %s\n" %
                   str(action.radar_return.direction))
    writable.write("radar_return.range: %d\n" % action.radar_return.range)
    writable.write("radar_return.health: %d\n" % action.radar_return.health)
    writable.write("radar_return.last_move_direction: %s\n" %
                   str(action.radar_return.last_move_direction))
    writable.write("radar_return.last_move_distance: %d\n",
                   action.radar_return.last_move_distance)
  if action.move_direction:
    writable.write("move_direction: %s\n" % action.move_direction)
    writable.write("move_distance: %d\n", action.move_distance)
  for damage in action.damage_dealt:
    writable.write("damage_dealt.amount: %d\n" % damage.amount)
    writable.write("damage_dealt.description: %s\n" % damage.description)
  for damage in action.damage_taken:
    writable.write("damage_taken.amount: %d\n" % damage.amount)
    writable.write("damage_taken.description: %s\n" % damage.description)
  if action.lose_reason:
    writable.write("lose_reason: %s" % action.lose_reason)
