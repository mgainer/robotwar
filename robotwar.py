#!/usr/bin/env python

import imp
import os
import sys
import optparse

from robots import robot
from world import terrain_map
from world import master

def parse_options(argv):
  parser = optparse.OptionParser()
  parser.add_option('--shot_range', type='int', default=30)
  parser.add_option('--shot_speed', type='int', default=10)
  parser.add_option('--shot_damage', type='int', default=10)
  parser.add_option('--collision_damage', type='int', default=5)
  parser.add_option('--radar_range', type='int', default=50)
  parser.add_option('--robot_health', type='int', default=30)
  parser.add_option('--map')
  parser.add_option('--random_seed', type='int', default=0)
  parser.add_option('--robot', action='append', dest='robots')
  options, unused_argv = parser.parse_args(argv)
  return options


def main(argv):
  options = parse_options(argv)
  robots = robot.load_robots(options.robots)
  world_map = terrain_map.TerrainMap(options.map)
  master = world.master(options, robots, world_map)
  master.run()

if __name__ == '__main__':
  main(sys.argv[1:])
