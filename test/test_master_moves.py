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

class TestOneRobot(unittest.TestCase):

  def setUp(self):
    # Pre-set random seed to get robot #0 at 1,1, and #1 at 1,2.  This makes
    # it simpler to set up shot directions.
    random.seed(1)
    self._options = robotwar.parse_options([])
    self._history = play_history.PlayHistory()
    self._world_map = terrain.TerrainMap('  ', '')
    self._r0 = robot_module.Robot(0, self._world_map)
    self._game = master.Master(
        self._options, [self._r0], self._world_map, self._history)
    self._round = self._game._prepare_round()

  def test_move_east(self):
    self._r0.get_move = lambda : direction.EAST
    self._round = self._game._do_round(self._round)

    self.assertEquals(len(self._history._rounds), 2)
    a0 = self._history._rounds[1]._actions[self._r0]
    self.assertEquals(a0.starting_health, self._options.robot_health)
    self.assertEquals(a0.ending_health, self._options.robot_health)
    self.assertEquals(a0.starting_position, position.Position(1,1))
    self.assertEquals(a0.ending_position, position.Position(2,1))
    self.assertEquals(a0.shot_direction, None)
    self.assertEquals(a0.shot_distance, None)
    self.assertEquals(a0.radar_direction, None)
    self.assertEquals(a0.radar_return, None)
    self.assertEquals(a0.move_direction, direction.EAST)
    self.assertEquals(a0.move_distance, 1)
    self.assertEquals(len(a0.damage_dealt), 0)
    self.assertEquals(len(a0.damage_taken), 0)
    self.assertEquals(a0.lose_reason, None)

  def test_move_south(self):
    self._r0.get_move = lambda : direction.SOUTH
    self._round = self._game._do_round(self._round)

    self.assertEquals(len(self._history._rounds), 2)
    a0 = self._history._rounds[1]._actions[self._r0]
    self.assertEquals(a0.starting_health, self._options.robot_health)
    self.assertEquals(a0.ending_health, self._options.robot_health)
    self.assertEquals(a0.starting_position, position.Position(1,1))
    self.assertEquals(a0.ending_position, position.Position(1,1))
    self.assertEquals(a0.shot_direction, None)
    self.assertEquals(a0.shot_distance, None)
    self.assertEquals(a0.radar_direction, None)
    self.assertEquals(a0.radar_return, None)
    self.assertEquals(a0.move_direction, direction.SOUTH)
    self.assertEquals(a0.move_distance, 0)
    self.assertEquals(len(a0.damage_dealt), 0)
    self.assertEquals(len(a0.damage_taken), 0)
    self.assertEquals(a0.lose_reason, None)


class TestTwoRobots(unittest.TestCase):

  def setUp(self):
    # Pre-set random seed to get robot #0 at 1,1, and #1 at 1,2.  This makes
    # it simpler to set up shot directions.
    random.seed(1)
    self._options = robotwar.parse_options([])
    self._history = play_history.PlayHistory()
    self._world_map = terrain.TerrainMap('  ', '')
    self._r0 = robot_module.Robot(0, self._world_map)
    self._r1 = robot_module.Robot(1, self._world_map)
    self._game = master.Master(
        self._options, [self._r0, self._r1], self._world_map, self._history)
    self._round = self._game._prepare_round()

  def test_r0_moves_into_r1_once(self):
    self._r0.get_move = lambda : direction.EAST
    self._game._do_round(self._round)

    self.assertEquals(len(self._history._rounds), 2)
    a0 = self._history._rounds[1]._actions[self._r0]
    a1 = self._history._rounds[1]._actions[self._r1]
    p0 = position.Position(1,1)
    p1 = position.Position(2,1)

    self.assertEquals(a0.starting_health, self._options.robot_health)
    self.assertEquals(
        a0.ending_health,
        self._options.robot_health - self._options.collision_damage)
    self.assertEquals(a0.starting_position, p0)
    self.assertEquals(a0.ending_position, p0)
    self.assertEquals(a0.shot_direction, None)
    self.assertEquals(a0.shot_distance, None)
    self.assertEquals(a0.radar_direction, None)
    self.assertEquals(a0.radar_return, None)
    self.assertEquals(a0.move_direction, direction.EAST)
    self.assertEquals(a0.move_distance, 0)
    self.assertEquals(len(a0.damage_dealt), 1)
    self.assertEquals(a0.damage_dealt[0].amount, self._options.collision_damage)
    self.assertEquals(a0.damage_dealt[0].description,
                      'Robot(#0) drove into Robot(#1)')
    self.assertEquals(len(a0.damage_taken), 1)
    self.assertEquals(a0.damage_taken[0].amount, self._options.collision_damage)
    self.assertEquals(a0.damage_taken[0].description,
                      'Robot(#0) drove into Robot(#1)')
    self.assertEquals(a0.lose_reason, None)

    self.assertEquals(a1.starting_health, self._options.robot_health)
    self.assertEquals(
        a1.ending_health,
        self._options.robot_health - self._options.collision_damage)
    self.assertEquals(a1.starting_position, p1)
    self.assertEquals(a1.ending_position, p1)
    self.assertEquals(a1.shot_direction, None)
    self.assertEquals(a1.shot_distance, None)
    self.assertEquals(a1.radar_direction, None)
    self.assertEquals(a1.radar_return, None)
    self.assertEquals(a1.move_direction, None)
    self.assertEquals(a1.move_distance, None)
    self.assertEquals(len(a1.damage_dealt), 1)
    self.assertEquals(a1.damage_dealt[0].amount, self._options.collision_damage)
    self.assertEquals(a1.damage_dealt[0].description,
                      'Robot(#0) drove into Robot(#1)')
    self.assertEquals(len(a1.damage_taken), 1)
    self.assertEquals(a1.damage_taken[0].amount, self._options.collision_damage)
    self.assertEquals(a1.damage_taken[0].description,
                      'Robot(#0) drove into Robot(#1)')
    self.assertEquals(a1.lose_reason, None)

  def test_mutual_collision(self):
    self._r0.get_move = lambda : direction.EAST
    self._r1.get_move = lambda : direction.WEST
    self._game._do_round(self._round)

    self.assertEquals(len(self._history._rounds), 2)
    a0 = self._history._rounds[1]._actions[self._r0]
    a1 = self._history._rounds[1]._actions[self._r1]
    p0 = position.Position(1,1)
    p1 = position.Position(2,1)


    self.assertEquals(a0.starting_health, self._options.robot_health)
    self.assertEquals(
        a0.ending_health,
        self._options.robot_health - self._options.collision_damage * 2)
    self.assertEquals(a0.starting_position, p0)
    self.assertEquals(a0.ending_position, p0)
    self.assertEquals(a0.shot_direction, None)
    self.assertEquals(a0.shot_distance, None)
    self.assertEquals(a0.radar_direction, None)
    self.assertEquals(a0.radar_return, None)
    self.assertEquals(a0.move_direction, direction.EAST)
    self.assertEquals(a0.move_distance, 0)
    self.assertEquals(len(a0.damage_dealt), 2)
    self.assertEquals(a0.damage_dealt[0].amount, self._options.collision_damage)
    self.assertEquals(a0.damage_dealt[0].description,
                      'Robot(#0) drove into Robot(#1)')
    self.assertEquals(a0.damage_dealt[1].amount, self._options.collision_damage)
    self.assertEquals(a0.damage_dealt[1].description,
                      'Robot(#1) drove into Robot(#0)')
    self.assertEquals(len(a0.damage_taken), 2)
    self.assertEquals(a0.damage_taken[0].amount, self._options.collision_damage)
    self.assertEquals(a0.damage_taken[0].description,
                      'Robot(#0) drove into Robot(#1)')
    self.assertEquals(a0.damage_taken[1].amount, self._options.collision_damage)
    self.assertEquals(a0.damage_taken[1].description,
                      'Robot(#1) drove into Robot(#0)')
    self.assertEquals(a0.lose_reason, None)

    self.assertEquals(a1.starting_health, self._options.robot_health)
    self.assertEquals(
        a1.ending_health,
        self._options.robot_health - self._options.collision_damage * 2)
    self.assertEquals(a1.starting_position, p1)
    self.assertEquals(a1.ending_position, p1)
    self.assertEquals(a1.shot_direction, None)
    self.assertEquals(a1.shot_distance, None)
    self.assertEquals(a1.radar_direction, None)
    self.assertEquals(a1.radar_return, None)
    self.assertEquals(a1.move_direction, direction.WEST)
    self.assertEquals(a1.move_distance, 0)
    self.assertEquals(len(a1.damage_dealt), 2)
    self.assertEquals(a1.damage_dealt[0].amount, self._options.collision_damage)
    self.assertEquals(a1.damage_dealt[0].description,
                      'Robot(#0) drove into Robot(#1)')
    self.assertEquals(a1.damage_dealt[1].amount, self._options.collision_damage)
    self.assertEquals(a1.damage_dealt[1].description,
                      'Robot(#1) drove into Robot(#0)')
    self.assertEquals(len(a1.damage_taken), 2)
    self.assertEquals(a1.damage_taken[0].amount, self._options.collision_damage)
    self.assertEquals(a1.damage_taken[0].description,
                      'Robot(#0) drove into Robot(#1)')
    self.assertEquals(a1.damage_taken[1].amount, self._options.collision_damage)
    self.assertEquals(a1.damage_taken[1].description,
                      'Robot(#1) drove into Robot(#0)')
    self.assertEquals(a1.lose_reason, None)


  def mutual_assured_collision(self):
    self._r0.get_shot = lambda : direction.EAST
    self._r1.get_move = lambda : direction.WEST

    num_rounds = 1
    for move in range(0, self._options.robot_health,
                      self._options.collision_damage * 2):
      self._round = self._game._do_round(self._round)
      num_rounds += 1


    self.assertEquals(len(self._history._rounds), num_rounds)
    a0 = self._history._rounds[num_rounds - 1]._actions[self._r0]
    a1 = self._history._rounds[num_rounds - 1]._actions[self._r1]

    self.assertEquals(a0.ending_health, 0)
    self.assertEquals(a0.lose_reason,
                      'Robot(#0) drove into Robot(#1)')

    self.assertEquals(a1.ending_health, 0)
    self.assertEquals(a1.lose_reason,
                      'Robot(#0) drove into Robot(#1)')

if __name__ == "__main__":
  unittest.main()
