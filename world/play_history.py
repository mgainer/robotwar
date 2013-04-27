import collections
import copy

# TODO(anybody): Write an entirely separate program to consume that output
# and produce:
# - cheapo ASCII graphics
# - better tile-based graphics
# - sound

# TODO(anybody): Hook up robotwar as a web application.  Submit names of robots
# from a web page, and display outputs using HTML5 animations

class PlayHistory:
  def __init__(self):
    self.rounds = []

  def new_round(self, world_map):
    round = Round()
    round._world_map = copy.deepcopy(world_map)
    self.rounds.append(round)
    return round


class Round:
  def __init__(self):
    self.actions = {}

  def add_robot(self, robot, position, health):
    action = Action(position, health)
    self.actions[robot] = action

  def set_shot(self, robot, direction, distance):
    self.actions[robot].set_shot(direction, distance)

  def set_move(self, robot, direction, distance):
    self.actions[robot].set_move(direction, distance)

  def set_radar(self, robot, radar_direction, radar_return):
    self.actions[robot].set_radar(radar_direction, radar_return)

  def set_lose_reason(self, robot, reason):
    self.actions[robot].set_lose_reason(reason)

  def add_damage_dealt(self, robot, damage):
    self.actions[robot].dealt_damage(damage)

  def add_damage_taken(self, robot, damage):
    self.actions[robot].took_damage(damage)

  def get(self, robot):
    return self.actions[robot]


class Action:
  def __init__(self, position, health):
    self.starting_health = health
    self.ending_health = health
    self.starting_position = position
    self.ending_position = position
    self.shot_direction = None
    self.shot_distance = None
    self.radar_direction = None
    self.radar_return = None
    self.move_direction = None
    self.move_distance = None
    self.damage_dealt = []
    self.damage_taken = []
    self.lose_reason = None

  def set_shot(self, direction, distance):
    self.shot_direction = direction
    self.shot_distance = distance

  def set_radar(self, radar_direction, radar_return):
    self.radar_direction = radar_direction
    self.radar_return = radar_return

  def set_move(self, direction, distance):
    self.move_direction = direction
    self.move_distance = distance
    for i in range(distance):
      self.ending_position = self.ending_position.move_by(direction)

  def took_damage(self, damage):
    self.damage_taken.append(damage)
    self.ending_health = max (self.ending_health - damage.amount, 0)

  def dealt_damage(self, damage):
    self.damage_dealt.append(damage)

  def set_lose_reason(self, reason):
    self.lose_reason = reason
