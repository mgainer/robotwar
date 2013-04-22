import random
import sys

from world import position
from world import robot

class Master:

  def __init__(options, robots, map, play_history):
    self._options = options
    self._map = map
    self._play_history = play_history

TODO - clean up use of data; centralize in play_history.

    self._robot_data = {}
    # TODO(mgainer) Add shots in the air; don't fully resolve shots
    # immediately upon launch; rather move them a bit per round until
    # they've hit maximum range.

    for robot in robots:
      position = self._find_empty_position()
      self._robot_data[robot] = RobotData(position, options.robot_health)


  def _find_empty_position(self):
    # Brute force attempt to randomly place a robot somewhere sane.
    # Simpler to just do a lot of tries rather than to enumerate the
    # available spots and randomly pick one.
    patience = 1000
    while patience > 0:
      --patience

      # Pick a spot.
      position = position.Position(
          random.randint(0, self._map.width - 1),
          random.randint(0, self._map.height - 1))

      # Don't drop the robot onto anything unpleasant.
      if !self._map.get(position).can_move_onto:
        continue

      # Or onto another robot.
      other_robot_present = False
      for datum in self._robot_data.values():
        if datum.position == position:
          other_robot_present = True
      if other_robot_present:
        continue
      return position
    raise Error("Tried too may times to place a robot.  Perhaps there are "
                "too many robots for the available space on the map?")

  def run(self):
    for round_counter in range(options.max_rounds):
      round = play_history.new_round(self._robot_data.keys())
      for robot in self._robot_data:
        try:
          # TODO(mgainer): Set a timer or some such to prevent infinite loops.
          # TODO(mgainer): Is there a way to playpen off the robot so it can't
          #   do any harm or rummage any data structures it's not supposed to?
          #   Is 'exec' a jail?
          # TODO(mgainer): maybe profiling interface lets us limit number of
          # VM cycles?
          robot.round()
        except:
          print "Unexpected error from robot %s" % robot.name, sys.exc_info()[0]
          self.dead_robot(robot, "exception")
        
      # First, resolve shots.  This goes before movement so that we don't have
      # robots moving and shooting in the same direction getting clobbered by
      # its own shot.  Next, movement, and last radar.  Radar last so that
      # robot gets a picture of the world consistent with its current
      # position, not where it was.
      self._resolve_shots(round, dead_robots)
      self._resolve_movement(round, dead_robots)
      self._resolve_radar(round)

      # TODO(mgainer): Better recognition of overall winner, collection
      # of stats?
      if len(self._robot_data == 1):
        return robot_data.keys()[0]  # The winner
      elif len(self._robot_data == 0):
        return None  # No winner - simultaneous death
    return None  # No winner - ran out of time.

  def _resolve_shots(self, round):
    # Keep a list of robots killed.  Since all robots shoot at the
    # same instant, we can't remove the ones killed from the list
    # until after all shots have been resolved.
    dead_robots = []

    for shooting_robot, shooter_data in self._robot_data.items():
      shot_direction = shooting_robot.get_shot()
      if shot_direction is not None:
        # Move shot before checking collisions so we don't shoot ourselves.
        shot_location = shooter_data.position

        # TODO(mgainer): Allow robots to specify a range as well as a 
        # direction (as long as the range is less or equal to max range.
        # If shell stops in forest, will we set the forest on fire for
        # a little while?
        for move in range(options.shot_range):
          shot_location = shot_location.move_by(shot_direction)

          target_robot, target_data = self._find_robot(shot_location)
          if target_robot is not None:
            round.add_damage_dealt(shooting_robot, options.shot_damage,
                                   "shot  " + target_robot.name())
            if self._damage_robot(round, target_robot, options.shot_damage,
                                   "shot by " + shooting_robot.name()):
              dead_robots.append(target_robot)
            break  # Shot only damages one robot; terminate loop early.

          # Stop shot on terrain, but only after checking for robot hit.
          # For terrain that's non-move and non-shoot, it doesn't matter.
          # For terrain that's move-able but non-shootable, we presume
          # that the shot stops due to cumulative terrain resistance, rather
          # than at the very edge, and thus a tank on that terrain can still
          # get hit if it's right at the boundary.
          if !self._map.get(shot_location).can_shoot_through:
            break;

          # TODO(mgainer): Add destructible terrain?  If there is, say,
          # a "boulder" terrain type that's un-shootable and un-moveable,
          # but if it absorbs enough shots, it gets destroyed, and becomes
          # some other terrain type...

    # Any robots destroyed by shots don't get to move or send radar.
    for robot in dead_robots:
      del self._robot_data[robot]

  def resolve_movement(self, round):
    dead_robots = []

    for moving_robot, mover_data in self._robot_data.items():
      round.set_starting_position(moving_robot, mover_data.position)
      direction = moving_robot.get_move()
      if move is not None:
        round.set_move(moving_robot, direction)
        new_position = mover_data.position.move_by(direction)
        if self._map.get(new_position).can_move_onto:
          
          # Here, it's OK to move on to the terrain, but maybe another
          # robot is here?  If so, collide, both take damage, and no
          # movement takes place.
          target_robot, target_data = self._find_robot(target_robot)
          if target_robot is not None:
            if self._damage_robot(round, target_robot, options.collision_damage,
                                  "driven into by " + moving_robot.name()):
              dead_robots.append(target_robot)
            if self._damage_robot(round, moving_robot, options.collision_damage,
                                  "drove into " + target_robot.name()):
              dead_robots.append(moving_robot)
          else:
            mover_data.position = new_position

          # TODO(mgainer): any other terrain-based effects?  Damage?
          # Heath bonus?  Etc...
        round.set_ending_position(moving_robot, mover_data.position)

    # Any robots dead due to collision are removed before we ping the
    # radar.
    for robot in dead_robots:
      del self._robot_data[robot]

  def _resolve_radar(self, round):
    for pinging_robot, pinger_data in self._robot_data.items():
      radar_return = robot_data.RadarReturn(None, None, None)
      direction = robot.get_radar()
      round.set_radar(pinging_robot, direction)
      if direction is not None:
        ping_position = pinger_data.position
        
        for distance in range(1, options.radar_range+1):
          ping_position = ping_position.move_by(direction)
          
          target_robot, target_data = self._find_robot(self, position)
          if target_robot is not None:
            radar_return = robot_data.RadarReturn(
              distance, target_data.health, target_data.last_move)
            break  # Radar returns 1st robot in that direction
      round.set_radar_return(robot, radar_return)
      pinger_data.radar_return = radar_return
          
  def _find_robot(self, position):
    for target_robot, target_data in self._robot_data.items():
      if target_data.position == position:
        return target_robot, target_data
    return None, NOne

  def _damage_robot(self, round, target_robot, amount, reason):
    round.add_damage_taken(target_robot, amount, reason)
    self._robot_data[robot].health -= options.shot_damage
    if self._robot_data[target_robot].health <= 0:
      # TODO(mgainer): Add record of kills to play history.
      round.set_lose_reason(robot, reason)
      return True  # Dead
    return False  # Not dead
                                       

class RobotData:
  def __init__(self, position, health):
    self.position = position
    self.health = health
    self.radar_return = robot_data.RadarReturn(None, None, None)
    
