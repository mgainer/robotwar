import random
import sys

from world import position
from world import robot_data

class Master:

  def __init__(options, robots, map):
    self._options = options
    self._robots = robots
    self._map = map
    random.seed(options.random_seed)
    #self._mobs = [[None] * map.height] * map.width

    self._robot_data = {}
    for robot in robots:
      position = self._find_empty_position()
      robot_data[robot] = robot_data.RobotData(
          position, None, None, None, None, options.robot_health)

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
    for robot in self._robots:
      try:
        # TODO(mgainer): Set a timer or some such to prevent infinite loops.
        # TODO(mgainer): Is there a way to playpen off the robot so it can't
        #   do any harm or rummage any data structures it's not supposed to?
        #   Is 'exec' a jail?
        robot.round()
      except:
        print "Unexpected error from robot %s" % robot.name, sys.exc_info()[0]
        self.dead_robot(robot, "exception")


    for ro
