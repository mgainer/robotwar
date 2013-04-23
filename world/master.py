import random
import sys
import traceback

from world import position
from robots import robot_module


class Master:
  """Operation of game mechanics.

  Game is run until only one (or zero) robot remains, or game runs out of
  moves.
  """

  def __init__(self, options, robots, world_map, play_history):
    """Build game master.

    Args:
      robots: List of robot_module.Robot instances.
      map: terrain_map.TerrainMap instance loaded with a map.
      play_history: Blank play_history.PlayHistory instance.
    """

    self._options = options
    self._map = world_map
    self._play_history = play_history

    # This is a tuple of robot -> RobotData.  This data is the Official Truth
    # about the state of the robot during gameplay.  This is kept in addition
    # to the play_history.Action data so that the play_history stuff can be
    # treated as (very nearly) write-only, and so that play_history classes
    # don't accumulate any responsibilities for game-play logic.
    self._robot_data = {}

    for unplaced_robot in robots:
      position = self._find_empty_position()
      self._robot_data[unplaced_robot] = RobotData(
          position, options.robot_health)


  def _find_empty_position(self):
    """Emplace robts onto the map.

    Brute force attempt to randomly place a robot somewhere sane.  Simpler to
    just do a lot of tries rather than to enumerate the available spots and
    randomly pick one.  Eventually, if terrain acquires a lot of features,
    may need to prove that all robots can eventually travel to the point
    where they can see and/or shoot one another.
    """

    patience = 3
    while patience > 0:
      patience -= 1

      # Pick a spot.
      destination = position.Position(
          random.randint(1, self._map.width - 2),
          random.randint(1, self._map.height - 2))

      # Don't drop the robot onto anything unpleasant.
      if not self._map.get(destination).can_move_onto:
        continue

      # Or onto another robot.
      other_robot, other_robot_data = self._find_robot(destination)
      if other_robot:
        continue

      return destination

    raise RuntimeError("Tried too many times to place a robot.  "
                       "Perhaps there are too many robots for the available "
                       "space on the map?")

  def run(self):

    # Prepare a blank "previous round" as the starting point.  This will tell
    # the robot that it had no previous move/shot/radar/damage.
    round = self._prepare_round()

    # Main loop.  As long as more than one robot remains, and we're not out
    # of rounds in the game, get and evaluate shots, moves, radar pulses.
    for round_counter in range(self._options.max_rounds):
      round = self._do_round(round)

      # TODO(mgainer): Better recognition of overall winner, collection
      # of stats?
      if len(self._robot_data) == 1:
        return robot_data.keys()[0]  # The winner
      elif len(self._robot_data) == 0:
        return None  # No winner - simultaneous death
    return None  # No winner - ran out of time.

  def _do_round(self, previous_round):
    # First, find out what each robot wants to do.
    for robot, robot_data in self._robot_data.items():
        # TODO(mgainer): Set a timer or some such to prevent infinite loops.
        # TODO(mgainer): Is there a way to playpen off the robot so it can't
        #   do any harm or rummage any data structures it's not supposed to?
        #   Is 'exec' a jail?
        # TODO(mgainer): maybe profiling interface lets us limit number of
        # VM cycles?
      last_move_info = self._build_last_move_info(previous_round, robot,
                                                  robot_data)
      try:
        robot.pre_round()
        robot.round(last_move_info)
      except Exception as ex:
        ex.traceback = traceback.format_exc()
        print "Unexpected error from robot %s" % robot.name, sys.exc_info()[0]
        robot.set_exception(ex)

    # When resolving behaviors, do shots first.  This goes before movement so
    # that we don't have a robot moving and shooting in the same direction
    # getting clobbered by its own shot.  Next, movement, and last radar.
    # Radar goes last so that robot gets a picture of the world consistent
    # with its current position, not where it was before it moved.
    round = self._prepare_round()
    self._resolve_exceptions(round)
    self._resolve_shots(round)
    self._resolve_movement(round)
    self._resolve_radar(round)
    return round

  def _prepare_round(self):
    """Prepare a new round of play.

    Tell the play history that we're starting a new round, and clear out
    any temporary data in the self._robot_data set from the previous round.

    Returns:
      A play_history.Round instance ready to accept facts about robots.
    """

    round = self._play_history.new_round()
    for robot, robot_data in self._robot_data.items():
      round.add_robot(robot, robot_data.position, robot_data.health)
      robot_data.radar_return = None
      robot_data.last_move_direction = None
      robot_data.last_move_distance = None
    return round

  def _build_last_move_info(self, previous_round, robot, robot_data):
    """Build a picture of what happened to a robot in the previous round.

    Use the Official Data for health, position.  Pull the other facts about
    history from the play_history log.

    Args:
      previous_round: play_history.Round containing per-robot Actions
      robot: The robot to use to look up the Action in the Round.
    Returns:
      robot_module.MoveData filled out with what happened to this robot in the
      previous round.
    """

    action = previous_round.get(robot)
    return robot_module.MoveData(
        robot_data.health,
        robot_data.position,
        action.shot_direction,
        action.shot_distance,
        action.move_direction,
        action.move_distance,
        action.radar_direction,
        action.radar_return,
        action.damage_dealt,
        action.damage_taken)

  def _resolve_exceptions(self, round):
    dead_robots = []
    for exploding_robot, exploder_data in self._robot_data.items():
      explosion = exploding_robot.get_exception()
      if explosion:
        self._damage_robot(round, exploding_robot, robot_module.Damage(
            exploder_data.health,
            "exploded due to internal failure: " + str(explosion)))
    for dead_robot in dead_robots:
      del self._robot_data[robot]

  def _resolve_shots(self, round):
    """Act upon shot requests from robots.

    For each robot, determine result of shot and record that.  Remove destroyed
    robots.

    Args:
      round: A play_history.Round instance where we record damage to robots.
    """

    # Keep a list of robots killed.  Since all robots shoot at the
    # same instant, we can't remove the ones killed from the list
    # until after all shots have been resolved.
    dead_robots = []

    # TODO(mgainer): Add shots in the air; don't fully resolve shots
    # immediately upon launch; rather move them some amount per round until
    # they've hit maximum range or something solid.

    for shooting_robot, shooter_data in self._robot_data.items():

      # TODO(mgainer): Intentionally leaving open security hole where
      # robot might override get_shot() to take control.  It's moderately
      # easily fixable without changing the official interface.
      shot_direction = shooting_robot.get_shot()
      if shot_direction is not None:
        # Move shot before checking collisions so we don't shoot ourselves.
        shot_location = shooter_data.position

        # TODO(mgainer): Allow robots to specify a range as well as a
        # direction (as long as the range is less or equal to max range.
        # If shell stops in forest, will we set the forest on fire for
        # a little while?
        for shot_distance in range(1, self._options.shot_range+1):
          shot_location = shot_location.move_by(shot_direction)

          target_robot, target_data = self._find_robot(shot_location)
          if target_robot is not None:
            damage = robot_module.Damage(self._options.shot_damage,
                                         "%s shot %s" % (
                                             shooting_robot.name,
                                             target_robot.name))
            if self._damage_robot(round, shooting_robot, target_robot, damage):
              dead_robots.append(target_robot)
            break  # Shot only damages one robot; terminate loop early.

          # Stop shot on terrain, but only after checking for robot hit.
          # For terrain that's non-move and non-shoot, it doesn't matter.
          # For terrain that's move-able but non-shootable, we presume
          # that the shot stops due to cumulative terrain resistance, rather
          # than at the very edge, and thus a tank on that terrain can still
          # get hit if it's right at the boundary.
          if not self._map.get(shot_location).can_shoot_through:
            break

          # TODO(mgainer): Add destructible terrain?  If there is, say,
          # a "boulder" terrain type that's un-shootable and un-moveable,
          # but if it absorbs enough shots, it gets destroyed, and becomes
          # some other terrain type...

        round.set_shot(shooting_robot, shot_direction, shot_distance)

    # Any robots destroyed by shots don't get to move or send radar.
    # TODO(mgainer): Dead robots leave corpses that can't be moved through?
    #   Implement this as just a change to terrain?
    for robot in dead_robots:
      del self._robot_data[robot]

  def _resolve_movement(self, round):
    """Act upon movement requests from robots.

    For each robot, determine result of move and record that.  Remove destroyed
    robots.

    Args:
      round: A play_history.Round instance where we record movement and damage.
    """

    dead_robots = []

    for moving_robot, mover_data in self._robot_data.items():
      move_direction = moving_robot.get_move()
      if move_direction is not None:
        new_position = mover_data.position.move_by(move_direction)
        if self._map.get(new_position).can_move_onto:

          # Here, it's OK to move on to the terrain, but maybe another
          # robot is here?  If so, collide, both take damage, and no
          # movement takes place.
          target_robot, target_data = self._find_robot(new_position)
          if target_robot is not None:
            # TODO(mgainer): Set different amount of damage to move-er and
            # move-ee?  (Ramming is a valid strategy as long as you have
            # more health than the vicitim...)
            damage = robot_module.Damage(self._options.collision_damage,
                                         "%s drove into %s" % (
                                             moving_robot.name,
                                             target_robot.name))
            if self._damage_robot(round, moving_robot, target_robot, damage):
              print "adding dead target robot", target_robot
              dead_robots.append(target_robot)
            if self._damage_robot(round, target_robot, moving_robot, damage):
              print "adding dead moving robot", moving_robot
              dead_robots.append(moving_robot)
            self._move_robot(round, moving_robot, move_direction, 0)
          else:
            # TODO(mgainer): Damage or bonus from successfully moving onto
            # terrain?
            self._move_robot(round, moving_robot, move_direction, 1)
            mover_data.position = new_position
        else:
          # TODO(mgainer): Damage from trying to move into un-moveable
          # terrain and failing?
          self._move_robot(round, moving_robot, move_direction, 0)

    # Any robots dead due to collision are removed before we ping the
    # radar.
    for robot in dead_robots:
      del self._robot_data[robot]

  def _resolve_radar(self, round):
    """Act upon radar requests from robots.

    For each robot, determine result of radar and record that.
    robots.

    Args:
      round: A play_history.Round instance where we record radar outcomes.
    """

    for pinging_robot, pinger_data in self._robot_data.items():
      radar_return = None
      radar_direction = pinging_robot.get_radar()
      if radar_direction is not None:
        ping_position = pinger_data.position

        for radar_distance in range(1, self._options.radar_range+1):
          ping_position = ping_position.move_by(radar_direction)

          target_robot, target_data = self._find_robot(ping_position)
          if target_robot is not None:
            radar_return = robot_module.RadarReturn(
                radar_direction, radar_distance,
                target_data.health,
                target_data.last_move_direction,
                target_data.last_move_distance)
            break  # Radar returns 1st robot in that direction
      round.set_radar(pinging_robot, radar_direction, radar_return)
      pinger_data.radar_return = radar_return

  def _find_robot(self, position):
    for target_robot, target_data in self._robot_data.items():
      if target_data.position == position:
        return target_robot, target_data
    return None, None

  def _damage_robot(self, round, causing_robot, target_robot, damage):
    """Apply damage to a robot.

    Args:
      round: A play_history.Round object where damage to robots is recorded.
      causing_robot: If not None, logs damage caused to this robot's credit.
      target_robot: The robot instance being damaged.
      damage: A robot_module.Damage instance indicating amount and reason.
    Returns:
      True if robot is killed due to the damage; False otherwise.
    """
    if causing_robot is not None:
      round.add_damage_dealt(causing_robot, damage)
    round.add_damage_taken(target_robot, damage)
    self._robot_data[target_robot].health -= damage.amount
    if self._robot_data[target_robot].health <= 0:
      # TODO(mgainer): Add record of kills to play history.
      round.set_lose_reason(target_robot, damage.description)
      return True  # Dead
    return False  # Not dead

  def _move_robot(self, round, moving_robot, move_direction, move_distance):
    self._robot_data[moving_robot].last_move_direction = move_direction
    self._robot_data[moving_robot].last_move_distance = move_distance
    round.set_move(moving_robot, move_direction, move_distance)


class RobotData:
  """Simple class with public members to track per-robot data."""

  def __init__(self, position, health):
    self.position = position
    self.health = health
    self.radar_return = None
    self.last_move_direction = None
    self.last_move_distance = None
