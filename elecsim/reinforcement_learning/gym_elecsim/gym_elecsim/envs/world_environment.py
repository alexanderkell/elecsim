"""
File name: ElecsimWorld
Date created: 19/02/2019
Feature: #Enter feature description here
"""
from gym.spaces import Box
import numpy as np

from elecsim.model.world import World
from elecsim.scen_error.scenario_data import lost_load

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"

import gym
from gym import error, spaces, utils
from gym.utils import seeding


class WorldEnvironment(gym.Env):

    def __init__(self):
        print("trying to init")
        self.world = World(initialization_year=2018, total_demand=2000, data_folder="reinforcement_learning")
        self.action_space = Box(
            0.0, 250.0, shape=(1, ), dtype=np.float32)

        self.observation_space = Box(
            0.0, lost_load, shape=(1, ), dtype=np.float32)

    def reset(self):
        self.world = World(initialization_year=2018)
        return [-1000]

    def step(self, action):
        print("stepping number: {}".format(self.world.step_number))
        ob = [self.world.step(action)]
        reward = ob[0]

        done = self.world.step_number > 40

        return np.array(ob), reward, done, {}
        # return np.array([1]), reward, done, {}


    def render(self, mode='human', close=False):
        # print("num steps {}".format(self.number_of_steps))
        # print("action")

        return False
