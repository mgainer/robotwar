import collections

class RobotData(collections.namedtuple(
    'RobotDataTuple', [
        'position',
        'last_move',
        'last_radar',
        'last_shot',
        'radar_return',
        'health',
        ]):
