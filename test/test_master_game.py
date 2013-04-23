#!/usr/bin/env python

import os
import random
import sys
sys.path.append(os.getcwd())

import unittest

from robots import robot_module
from world import direction
from world import master
from world import play_history
from world import position
from world import terrain
import robotwar

class TestGame(unittest.TestCase):

  def setUp(self):
    # Pre-set random seed to get robot #0 at 1,1, and #1 at 1,2.  This makes
    # it simpler to set up shot directions.
    random.seed(1)
    self._options = robotwar.parse_options(['--max_rounds=3'])
    self._history = play_history.PlayHistory()
    self._world_map = terrain.TerrainMap('    ', '')
    self._r0 = robot_module.Robot(0, self._world_map)
    self._r1 = robot_module.Robot(1, self._world_map)
    self._game = master.Master(
        self._options, [self._r0, self._r1], self._world_map, self._history)

  def test_sneeches(self):
    self._r0.get_shot = lambda : direction.EAST
    self._r0.get_move = lambda : direction.EAST
    self._r0.get_radar = lambda : direction.EAST

    self._r1.get_shot = lambda : direction.WEST
    self._r1.get_move = lambda : direction.WEST
    self._r1.get_radar = lambda : direction.WEST

    self._game.run()

    self.assertEquals(len(self._history._rounds), 3)

    # Check results of round #1; expect both to have moved, radared, and shot
    # sucessfully, but not conclusively.
    a0 = self._history._rounds[1]._actions[self._r0]
    a1 = self._history._rounds[1]._actions[self._r1]

    self.assertEquals(a0.starting_health, self._options.robot_health)
    self.assertEquals(a0.ending_health,
                      self._options.robot_health - self._options.shot_damage)
    self.assertEquals(a0.starting_position, position.Position(1,1))
    self.assertEquals(a0.ending_position, position.Position(2,1))
    self.assertEquals(a0.shot_direction, direction.EAST)
    self.assertEquals(a0.shot_distance, 3)
    self.assertEquals(a0.radar_direction, direction.EAST)
    self.assertEquals(a0.radar_return, robot_module.RadarReturn(
        direction.EAST, 1,
        self._options.robot_health - self._options.shot_damage,
        direction.WEST, 1))
    self.assertEquals(a0.move_direction, direction.EAST)
    self.assertEquals(a0.move_distance, 1)
    self.assertEquals(len(a0.damage_dealt), 1)
    self.assertEquals(a0.damage_dealt[0].amount, self._options.shot_damage)
    self.assertEquals(a0.damage_dealt[0].description,
                      'Robot(#0) shot Robot(#1)')
    self.assertEquals(len(a0.damage_taken), 1)
    self.assertEquals(a0.damage_taken[0].amount, self._options.shot_damage)
    self.assertEquals(a0.damage_taken[0].description,
                      'Robot(#1) shot Robot(#0)')
    self.assertEquals(a0.lose_reason, None)

    self.assertEquals(a1.starting_health, self._options.robot_health)
    self.assertEquals(a1.ending_health,
                      self._options.robot_health - self._options.shot_damage)
    self.assertEquals(a1.starting_position, position.Position(4,1))
    self.assertEquals(a1.ending_position, position.Position(3,1))
    self.assertEquals(a1.shot_direction, direction.WEST)
    self.assertEquals(a1.shot_distance, 3)
    self.assertEquals(a1.radar_direction, direction.WEST)
    self.assertEquals(a1.radar_return, robot_module.RadarReturn(
        direction.WEST, 1,
        self._options.robot_health - self._options.shot_damage,
        direction.EAST, 1))
    self.assertEquals(a1.move_direction, direction.WEST)
    self.assertEquals(a1.move_distance, 1)
    self.assertEquals(len(a1.damage_dealt), 1)
    self.assertEquals(a1.damage_dealt[0].amount, self._options.shot_damage)
    self.assertEquals(a1.damage_dealt[0].description,
                      'Robot(#1) shot Robot(#0)')
    self.assertEquals(len(a1.damage_taken), 1)
    self.assertEquals(a1.damage_taken[0].amount, self._options.shot_damage)
    self.assertEquals(a1.damage_taken[0].description,
                      'Robot(#0) shot Robot(#1)')
    self.assertEquals(a1.lose_reason, None)


    # Check results of round #2; expect both to have attempted to move but
    # failed (collided), shot, and radared.  Both should be dead due to
    # collision.
    a0 = self._history._rounds[2]._actions[self._r0]
    a1 = self._history._rounds[2]._actions[self._r1]

    self.assertEquals(a0.starting_health,
                      self._options.robot_health - self._options.shot_damage)
    self.assertEquals(a0.ending_health, 0)
    self.assertEquals(a0.starting_position, position.Position(2,1))
    self.assertEquals(a0.ending_position, position.Position(2,1))
    self.assertEquals(a0.shot_direction, direction.EAST)
    self.assertEquals(a0.shot_distance, 1)
    self.assertEquals(a0.radar_direction, None)  # died before radar sent.
    self.assertEquals(a0.radar_return, None)  # died before radar sent.
    self.assertEquals(a0.move_direction, direction.EAST)
    self.assertEquals(a0.move_distance, 0)
    self.assertEquals(len(a0.damage_dealt), 3)
    self.assertEquals(a0.damage_dealt[0].amount, self._options.shot_damage)
    self.assertEquals(a0.damage_dealt[0].description,
                      'Robot(#0) shot Robot(#1)')
    self.assertEquals(a0.damage_dealt[1].amount, self._options.collision_damage)
    self.assertEquals(a0.damage_dealt[1].description,
                      'Robot(#1) drove into Robot(#0)')
    self.assertEquals(a0.damage_dealt[2].amount, self._options.collision_damage)
    self.assertEquals(a0.damage_dealt[2].description,
                      'Robot(#0) drove into Robot(#1)')
    self.assertEquals(len(a0.damage_taken), 3)
    self.assertEquals(a0.damage_taken[0].amount, self._options.shot_damage)
    self.assertEquals(a0.damage_taken[0].description,
                      'Robot(#1) shot Robot(#0)')
    self.assertEquals(a0.damage_taken[1].amount, self._options.collision_damage)
    self.assertEquals(a0.damage_taken[1].description,
                      'Robot(#1) drove into Robot(#0)')
    self.assertEquals(a0.damage_taken[2].amount, self._options.collision_damage)
    self.assertEquals(a0.damage_taken[2].description,
                      'Robot(#0) drove into Robot(#1)')
    self.assertEquals(a0.lose_reason,
                      'Robot(#0) drove into Robot(#1)')

    self.assertEquals(a1.starting_health,
                      self._options.robot_health - self._options.shot_damage)
    self.assertEquals(a1.ending_health, 0)
    self.assertEquals(a1.starting_position, position.Position(3,1))
    self.assertEquals(a1.ending_position, position.Position(3,1))
    self.assertEquals(a1.shot_direction, direction.WEST)
    self.assertEquals(a1.shot_distance, 1)
    self.assertEquals(a1.radar_direction, None)  # died before radar sent.
    self.assertEquals(a1.radar_return, None) # died before radar sent.
    self.assertEquals(a1.move_direction, direction.WEST)
    self.assertEquals(a1.move_distance, 0)
    self.assertEquals(len(a1.damage_dealt), 3)
    self.assertEquals(a1.damage_dealt[0].amount, self._options.shot_damage)
    self.assertEquals(a1.damage_dealt[0].description,
                      'Robot(#1) shot Robot(#0)')
    self.assertEquals(a1.damage_dealt[1].amount, self._options.collision_damage)
    self.assertEquals(a1.damage_dealt[1].description,
                      'Robot(#1) drove into Robot(#0)')
    self.assertEquals(a1.damage_dealt[2].amount, self._options.collision_damage)
    self.assertEquals(a1.damage_dealt[2].description,
                      'Robot(#0) drove into Robot(#1)')
    self.assertEquals(len(a1.damage_taken), 3)
    self.assertEquals(a1.damage_taken[0].amount, self._options.shot_damage)
    self.assertEquals(a1.damage_taken[0].description,
                      'Robot(#0) shot Robot(#1)')
    self.assertEquals(a1.damage_taken[1].amount, self._options.collision_damage)
    self.assertEquals(a1.damage_taken[1].description,
                      'Robot(#1) drove into Robot(#0)')
    self.assertEquals(a1.damage_taken[2].amount, self._options.collision_damage)
    self.assertEquals(a1.damage_taken[2].description,
                      'Robot(#0) drove into Robot(#1)')
    self.assertEquals(a1.lose_reason,
                      'Robot(#0) drove into Robot(#1)')


if __name__ == "__main__":
  unittest.main()
