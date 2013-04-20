
class Robot:
  def __init__(self):
    pass

  def turn_end(self, data):
    self.data = data
    self.move_direction = None
    self.radar_direction = None
    self.shot_direction = None

  def set_move(self, direction):
    self.move_direction = direction

  def get_move(self):
    return self.move_direction

  def set_radar(self, direction):
    self.radar_direction = direction

  def set_shot(self, direction):
    self.shot_direction = direction

  def round():
    pass  # By default, robots do nothing unless 'round' is overridden.

  @property
  def name(self):
    return self.__class__.__name__


def load_robots(names):
  robots = []
  for name in names:
    fp, path, desc = imp.find_module(os.path.join('robots', name.lower()))
    robot_module = imp.load_module(name, fp, path, desc)
    robot = eval('robot_module.%s()' % name)
    robots.add(robot)

  return robots
