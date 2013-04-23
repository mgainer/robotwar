#!/usr/bin/env python

import os
import sys
sys.path.append(os.getcwd())

import unittest

from world import terrain

class TestTerrainMap(unittest.TestCase):

  def test_blank(self):
    world = terrain.TerrainMap('', 'fred')
    self.assertEqual(world.width, 2)
    self.assertEqual(world.height, 2)
    self._assertWallBorder(world)

  def test_one_plains(self):
    world = terrain.TerrainMap(' ', 'fred')
    self.assertEqual(world.width, 3)
    self.assertEqual(world.height, 3)
    self._assertWallBorder(world)
    self.assertEqual(world.get_xy(1, 1), terrain.PLAINS)

  def test_two_plains(self):
    world = terrain.TerrainMap('  ', 'fred')
    self.assertEqual(world.width, 4)
    self.assertEqual(world.height, 3)
    self._assertWallBorder(world)
    self.assertEqual(world.get_xy(1, 1), terrain.PLAINS)
    self.assertEqual(world.get_xy(2, 1), terrain.PLAINS)

  def test_right_padding(self):
    world = terrain.TerrainMap(
        '  \n'
        ' \n', 'fred')
    self.assertEqual(world.width, 4)
    self.assertEqual(world.height, 4)
    self._assertWallBorder(world)
    self.assertEqual(world.get_xy(1, 1), terrain.PLAINS)
    self.assertEqual(world.get_xy(2, 1), terrain.PLAINS)
    self.assertEqual(world.get_xy(1, 2), terrain.PLAINS)
    self.assertEqual(world.get_xy(2, 2), terrain.WALL)

  def test_mobility(self):
    self.assertTrue(terrain.PLAINS.can_move_onto)
    self.assertFalse(terrain.WALL.can_move_onto)

  def test_illegal_terrain(self):
    with self.assertRaises(RuntimeError):
      terrain.TerrainMap('Q', 'fred')

  def _assertWallBorder(self, world):
    for x in range(world.width):
      self.assertEquals(world.get_xy(x, 0).symbol, '#')
      self.assertEquals(world.get_xy(x, world.height - 1).symbol, '#')

    for y in range(world.height):
      self.assertEquals(world.get_xy(0, y).symbol, '#')
      self.assertEquals(world.get_xy(world.width - 1, y).symbol, '#')

  def _find_terrain(self, name):
    for t in terrain.terrain_types:
      if t.name == name:
        return t

if __name__ == "__main__":
  unittest.main()
