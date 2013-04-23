import collections
import copy
import imp
import os

class Robot:
  def __init__(self, id_number, world_map):
    self._id_number = id_number
    self._map = world_map
    self.pre_round()

  def pre_round(self):
    self._move_direction = None
    self._radar_direction = None
    self._shot_direction = None
    self._exception = None

  def set_exception(self, exception):
    self._exception = exception

  def get_exception(self):
    return self._exception

  def set_move(self, direction):
    """Call this function to tell your robot to move in a direction this turn.

    Example:
    set_move(direction.NORTH)

    Note that moving into another robot causes damage.  Attempting to
    move into impassible terrain will just fail.

    Args:
      Which direction to move in.
    """
    self._move_direction = direction

  def get_move(self):
    """Called by the game master to find out how your robot should move."""
    return self._move_direction

  def set_radar(self, direction):
    """Call this function to tell your robot to send out a radar pulse.

    Example:
    set_radar(direction.SOUTHEAST)

    To find out what your radar pulse did last turn, examine the
    last_move_info.last_radar_return variable.  Example:


    if last_move_info.last_radar_return is not None:  # Did we see a robot?
      set_shot(last_move_info.last_radar_return.direction)  # Shoot it!
    Args:
      dirction: Which direction to send a radar pulse in.
    """
    self._radar_direction = direction

  def get_radar(self):
    """Called by the master to see in what direction to send a radar pulse."""
    return self._radar_direction

  def set_shot(self, direction):
    """Call this function to tell your robot to shoot its cannon in a direction.

    Args:
      direction: Which direction to shoot in.
    """
    self._shot_direction = direction

  def get_shot(self):
    """Called by the master to learn which direction your robot should shoot."""
    return self._shot_direction

  def round(self, last_move_info):
    """This function should be implemented by robots.

    This is the function called by the main loop of the game master program.
    In it, you should call the set_move(), set_radar(), and set_shot() functions
    to tell the master what you want your robot to do this round.

    TODO(anybody): Add options info to MoveData structure.  Robots need to know
    the range of the radar and range of shots -- if you see a robot on radar
    that's further away than your cannon can reach, you need to move towards
    it, rather than shoot at it.

    Args:
      data: A robot.MoveData instance.  This is filled out with the results
        of the previous round of game play.  This tells you what damage
        your robot caused and incurred.  This also provides you with
        the result of any radar pulse you emitted last turn.
    Return:
      The return value from this function is ignored.
    """

    pass  # By default, robots do nothing unless this function is overridden.

  @property
  def name(self):
    return self.__class__.__name__ + "(#" + str(self._id_number) + ")"

  def __str__(self):
    return self.name


def load_robots(names, world_map):
  robots = []
  for id_number, name in enumerate(names):
    fp, path, desc = imp.find_module(os.path.join('robots', name.lower()))

    # TODO(anybody): Better handling of exceptions at load time for when we
    # are running as a web application.
    robot_module = imp.load_module(name, fp, path, desc)
    cloned_map = copy.deepcopy(world_map)  # No cheating messing with the map!
    robot = eval('robot_module.%s(id_number, cloned_map)' % name)
    robots.append(robot)

  return robots


MoveData = collections.namedtuple(
    'MoveDataTuple', [
        'health',
        'position',
        'last_shot_direction',
        'last_shot_distance',
        'last_move_direction',
        'last_move_distance',
        'last_radar_direction',
        'last_radar_return',
        'damage_dealt',
        'damage_taken',
        ])


Damage = collections.namedtuple(
    'DamageTuple', [
        'amount',
        'description',
        ])


RadarReturn = collections.namedtuple(
    'RadarReturnTuple', [
        'direction',
        'range',
        'health',
        'last_move_direction',
        'last_move_distance',
        ])
