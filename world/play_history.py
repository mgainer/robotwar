import collections

# TODO(mgainer) Fix indentation: laptop likes 4-space tabs too much
class PlayHistory:
  def __init__(self):
      self._rounds = []

  def new_round(self, robots):
    round = Round(robots)
    self._rounds.append(round)
    return round

  def dump(self, map):
    for round in self._rounds:
      round.dump()
      

class Round:
    def __init__(self, robots):
        self._actions = {}
        for robot in robots:
            action = Action(robot)
            self._actions[robot] = action

    def set_shot(self, robot, direction):
        self._actions[robot].set_shot(direction)

    def set_move(self, robot, direction):
        self._actions[robot].set_move(direction)

    def set_radar(self, robot, direction):
        self._actions[robot].set_radar(direction)

    def set_radar_return(self, robot, radar_return):
        self._actions[robot].set_radar_return(radar_return)

    def set_starting_position(self, robot, position):
        self._actions[robot].set_starting_position

    def set_ending_position(self, robot, position):
        self._actions[robot].set_ending_positions

    def set_lose_reason(self, robot, reason):
        self._actions[robot].set_lose_reason

    def add_damage_dealt(self, robot, amount, description):
        self._actions[robot].dealt_damage(Damage(amount, description))

    def add_damage_taken(self, robot, amount, description):
        self._actions[robot].took_damage(Damage(amount, description))

        
class Action:
    def __init__(self):
        self._shot = None  # Direction
        self._radar = None  # Direction
        self._radar_return = None  # RadarReturn
        self._move = None  # Direction
        self._starting_position = None  # Position
        self._ending_position = None  # Position
        self._damage_dealt = []  # Damage
        self._damage_taken = []  # Damage
        self._lose_reason = None  # string

    def set_shot(self, shot):
        self._shot = shot

    def set_radar(self, radar):
        self._radar = radar

    def set_radar_return(self, radar_return):
        self._radar_return = radar_return

    def set_move(self, move):
        self._move = move

    def set_start_position(self, start_position):
        self._start_position = start_position

    def set_end_position(self, end_position):
        self._end_position = end_position

    def took_damage(self, damage):
        self._damage_taken.append(damage)

    def dealt_damage(self, damage):
        self._damage_dealt.append(damage)
    
    def set_lose_reason(self, reason):
        self._lose_reason = reason

Damage = (collections.namedtuple('DamageTuple', ['amount', 'description'])
