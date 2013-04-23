#!/usr/bin/env python

import os
import sys
sys.path.append(os.getcwd())

import unittest

from world import direction
from world import terrain
from robots import robot_module

class TestMasterPlacement(unittest.TestCase):

  def setUp(self):
    self._world_map = terrain.TerrainMap(' ', 'fred')

  def test_load(self):
    robots = robot_module.load_robots(['Target', 'Target'], self._world_map)
    self.assertEqual(robots[0].name, 'Target(#0)')
    self.assertEqual(robots[1].name, 'Target(#1)')
    self.assertNotEqual(robots[0], robots[1])

    # Ensure maps in robots are equivalent to world map, but are not the
    # same instance (to prevent map rewriting)
    self.assertEquals(robots[0]._map, self._world_map)
    self.assertFalse(robots[0]._map is self._world_map)
    self.assertEquals(robots[1]._map, self._world_map)
    self.assertFalse(robots[1]._map is self._world_map)

  def test_getset(self):
    r = robot_module.Robot(0, self._world_map)

    self.assertEquals(r.get_move(), None)
    r.set_move(direction.NORTH)
    self.assertEquals(r.get_move(), direction.NORTH)

    self.assertEquals(r.get_shot(), None)
    r.set_shot(direction.NORTH)
    self.assertEquals(r.get_shot(), direction.NORTH)

    self.assertEquals(r.get_radar(), None)
    r.set_radar(direction.NORTH)
    self.assertEquals(r.get_radar(), direction.NORTH)



if __name__ == "__main__":
  unittest.main()
