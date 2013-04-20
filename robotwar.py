#!/usr/bin/env python

import imp
import os
import sys
import optparse

from world import terrain_map

def parse_options(argv):
  parser = optparse.OptionParser()
  parser.add_option('--shot_range', type='int', default=30)
  parser.add_option('--shot_speed', type='int', default=10)
  parser.add_option('--shot_damage', type='int', default=10)
  parser.add_option('--collision_damage', type='int', default=5)
  parser.add_option('--radar_range', type='int', default=50)
  parser.add_option('--robot_health', type='int', default=30)
  parser.add_option('--map')
  parser.add_option('--robot', action='append', dest='robots')
  options, unused_argv = parser.parse_args(argv)
  return options


def load_robots(names):
  robots = {}
  for name in names:
    fp, path, desc = imp.find_module(os.path.join('robots', name.lower()))
    robot_module = imp.load_module(name, fp, path, desc)
    robot = eval('robot_module.%s()' % name)
    robots[name] = robot
  return robots

def main(argv):
  options = parse_options(argv)
  robots = load_robots(options.robots)
  for name, robot in robots.items():
    print name, robot
  world_map = terrain_map.TerrainMap(options.map)
  world_map.dump()

if __name__ == '__main__':
  main(sys.argv[1:])
