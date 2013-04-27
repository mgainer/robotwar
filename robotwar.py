#!/usr/bin/env python

import imp
import optparse
import os
import random
import StringIO
import sys
import time

from output import output_module
from robots import robot_module
from world import master
from world import play_history
from world import terrain

class BadOptions(Exception):
  def __init__(self, error_code, message):
    self._error_code = error_code
    self._message = message

  def __str__(self):
    return "bad options; error %d: %s" % (self._error_code, self._message)


def raise_bad_options(error_code, message):
  raise BadOptions(error_code, message)

def parse_options(argv):
  parser = optparse.OptionParser()
  parser.add_option('--full_dump', action='store_true')
  parser.add_option('--robot', action='append', dest='robots')
  parser.add_option('--max_rounds', type='int', default=1000)
  parser.add_option('--shot_range', type='int', default=30)
  parser.add_option('--shot_damage', type='int', default=10)
  parser.add_option('--collision_damage', type='int', default=5)
  parser.add_option('--radar_range', type='int', default=50)
  parser.add_option('--robot_health', type='int', default=30)
  parser.add_option('--map', default='tiny')
  parser.add_option('--random_seed', type='int', default=time.time())
  parser.add_option('--output', default='Ascii')

  # Stupid optparse is written to sys.exit() if it doesn't like the options,
  # rather than throw.  Psych it out by temporarily replacing sys.exit().
  save_exit = sys.exit
  save_stderr = sys.stderr
  sys.stderr = StringIO.StringIO()
  sys.exit = lambda err: raise_bad_options(err, sys.stderr.getvalue())
  options, unused_argv = parser.parse_args(argv)
  sys.exit = save_exit
  sys.stderr = save_stderr
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
  outputter = output_module.load_outputter(options.output, history, world_map)
  outputter.get_output(sys.stdout)


if __name__ == '__main__':
  main(sys.argv[1:])
