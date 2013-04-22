import collections

RobotData = collections.namedtuple(
    'RobotDataTuple', [
        'position',
        'last_move',
        'last_radar',
        'last_shot',
        'radar_return',
        'health',
	'map',
        ])

RadarReturn = collections.namedtuple(
    'RadarReturnTuple', [
        'distance',
        'health',
	'last_move',
	])

		
