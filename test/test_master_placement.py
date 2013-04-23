#!/usr/bin/env python

import os
import random
import sys
sys.path.append(os.getcwd())

import unittest

from world import terrain
from world import master
from world import play_history
from world import position
from robots import robot_module
import robotwar

class TestMasterPlacement(unittest.TestCase):

  def setUp(self):
    random.seed(0)
    self._options = robotwar.parse_options([])
    self._history = play_history.PlayHistory()

  def test_impossible(self):
    world_map = terrain.TerrainMap('', '')
    r = robot_module.Robot(0, world_map)
    with self.assertRaises(ValueError):
      game = master.Master(self._options, [r], world_map, self._history)

  def test_one_space_one_robot(self):
    world_map = terrain.TerrainMap(' ', '')
    r = robot_module.Robot(0, world_map)
    game = master.Master(self._options, [r], world_map, self._history)
    self.assertEquals(game._robot_data[r].position, position.Position(1, 1))

  def test_one_space_two_robots(self):
    world_map = terrain.TerrainMap(' ', '')
    r = robot_module.Robot(0, world_map)
    with self.assertRaises(RuntimeError):
      game = master.Master(self._options, [r, r], world_map, self._history)

  def test_two_spaces_two_robots(self):
    world_map = terrain.TerrainMap('  ', '')
    r0 = robot_module.Robot(0, world_map)
    r1 = robot_module.Robot(1, world_map)
    game = master.Master(self._options, [r0, r1], world_map, self._history)


if __name__ == "__main__":
  unittest.main()
