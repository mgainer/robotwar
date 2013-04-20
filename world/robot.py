
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
