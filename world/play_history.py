import collections

class PlayHistory:
  def __init__(self):
    self._rounds = []

  def new_round(self):
    round = Round()
    self._rounds.append(round)
    return round

  def dump(self):
    for number, round in enumerate(self._rounds):
      print "======================== Round %d =====================" % number
      round.dump()

class Round:
  def __init__(self):
    self._actions = {}

  def add_robot(self, robot, position, health):
    action = Action(position, health)
    self._actions[robot] = action

  def set_shot(self, robot, direction, distance):
    self._actions[robot].set_shot(direction, distance)

  def set_move(self, robot, direction, distance):
    self._actions[robot].set_move(direction, distance)

  def set_radar(self, robot, radar_direction, radar_return):
    self._actions[robot].set_radar(radar_direction, radar_return)

  def set_lose_reason(self, robot, reason):
    self._actions[robot].set_lose_reason(reason)

  def add_damage_dealt(self, robot, damage):
    self._actions[robot].dealt_damage(damage)

  def add_damage_taken(self, robot, damage):
    self._actions[robot].took_damage(damage)

  def get(self, robot):
    return self._actions[robot]

  def dump(self):
    for robot, action in self._actions.items():
      print "Robot", robot, "------------------------"
      action.dump()

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

  def dump(self):
    print "starting_health", self.starting_health
    print "ending_health", self.ending_health
    print "starting_position", self.starting_position
    print "ending_position", self.ending_position
    print "shot_direction", self.shot_direction
    print "shot_distance", self.shot_distance
    print "radar_direction", self.radar_direction
    if self.radar_return:
      print "radar_return.direction", self.radar_return.direction
      print "radar_return.range", self.radar_return.range
      print "radar_return.health", self.radar_return.health
      print "radar_return.last_move_direction",
      print self.radar_return.last_move_direction
      print "radar_return.last_move_distance",
      print self.radar_return.last_move_distance
    print "move_direction", self.move_direction
    print "move_distance", self.move_distance
    for damage in self.damage_dealt:
      print "damage_dealt.amount", damage.amount
      print "damage_dealt.description", damage.description
    for damage in self.damage_taken:
      print "damage_taken.amount", damage.amount
      print "damage_taken.description", damage.description
    print "lose_reason", self.lose_reason
