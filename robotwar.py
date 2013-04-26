#!/usr/bin/env python

import imp
import simplejson
import optparse
import os
import random
import sys
import time

from robots import robot_module
from world import master
from world import play_history
from world import terrain


def parse_options(argv):
  parser = optparse.OptionParser()
  parser.add_option('--robot', action='append', dest='robots')
  parser.add_option('--max_rounds', type='int', default=1000)
  parser.add_option('--shot_range', type='int', default=30)
  parser.add_option('--shot_damage', type='int', default=10)
  parser.add_option('--collision_damage', type='int', default=5)
  parser.add_option('--radar_range', type='int', default=50)
  parser.add_option('--robot_health', type='int', default=30)
  parser.add_option('--map', default='tiny')
  parser.add_option('--random_seed', type='int', default=time.time())
  options, unused_argv = parser.parse_args(argv)
  return options


def run(options):
  random.seed(options.random_seed)
  world_map = terrain.TerrainMap(terrain.read_map(options.map), options.map)
  robots = robot_module.load_robots(options.robots, world_map)
  history = play_history.PlayHistory()
  master.Master(options, robots, world_map, history).run()
  return history, world_map


def main(argv):
  options = parse_options(argv)
  history, world_map = run(options)
  history.dump()
  print simplejson.dumps({
      'history': history.simple(),
      'map': world_map.simple(),
      }, indent=2)


if __name__ == '__main__':
  main(sys.argv[1:])
