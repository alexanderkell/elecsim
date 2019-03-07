"""
File name: ElecsimWorld
Date created: 19/02/2019
Feature: #Enter feature description here
"""
from gym.spaces import Box
import numpy as np

from elecsim.model.world import World
from elecsim.scenario.scenario_data import lost_load

import logging

logger = logging.getLogger(__name__)

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"

import gym
from gym import error, spaces, utils
from gym.utils import seeding


class WorldEnvironment(gym.Env):

    def __init__(self, scenario_file=None, max_number_of_steps=32, data_folder="reinforcement_learning"):
        print("trying to init")
        self.step_number = 0
        self.action = None
        self.max_number_of_steps = max_number_of_steps
        self.world = World(initialization_year=2018, scenario_file=scenario_file, data_folder=data_folder, number_of_steps=self.max_number_of_steps)
        self.action_space = Box(
            0.0, 250.0, shape=(1, ), dtype=np.float32)

        self.observation_space = Box(
            0.0, lost_load, shape=(1, ), dtype=np.float32)

    def reset(self):
        self.world = World(initialization_year=2018)
        return [0]

    def step(self, action):
        print("stepping number: {}".format(self.world.step_number))
        self.action = action
        self.step_number += 1
        ob = [self.world.step(action)]
        reward = ob[0]

        done = self.world.step_number > self.max_number_of_steps

        return np.array(ob), reward, done, {}
        # return np.array([1]), reward, done, {}

    def render(self, mode='human', close=False):
        print("num steps {}".format(self.step_number))
        print("action: {}".format(self.action))

        return False
