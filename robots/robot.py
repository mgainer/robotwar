
class Robot:
  def __init__(self, number):
    self._number = number

  def turn_end(self, data):
    self._move_direction = None
    self._radar_direction = None
    self._shot_direction = None

  def set_move(self, direction):
    self._move_direction = direction

  def get_move(self):
    return self._move_direction

  def set_radar(self, direction):
    self._radar_direction = direction

  def get_radar(self):
    return self._radar_direction

  def set_shot(self, direction):
    self._shot_direction = direction

  def get_shot(self):
    return self._shot_direction

  def round(data):
    pass  # By default, robots do nothing unless 'round' is overridden.

  @property
  def name(self):
    return self.__class__.__name__ + "(#" + self._number + ")"


def load_robots(names):
  robots = []
  for name, number in enumerate(names):
    fp, path, desc = imp.find_module(os.path.join('robots', name.lower()))
    robot_module = imp.load_module(name, fp, path, desc)
    robot = eval('robot_module.%s()' % name)
    robots.add(robot, number)

  return robots
