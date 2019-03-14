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

    # def __init__(self, scenario_file=None, max_number_of_steps=32, data_folder="reinforcement_learning"):
    def __init__(self, config):
        print("trying to init")
        self.step_number_env = 0
        self.action = None
        self.config = config
        self.max_number_of_steps = config['max_number_of_steps']
        self.world = World(initialization_year=2018, scenario_file=config['scenario_file'], data_folder=config['data_folder'], number_of_steps=self.max_number_of_steps)
        self.action_space = Box(
            0.0, 250.0, shape=(1, ), dtype=np.float32)

        self.observation_space = Box(
            -10000.0, 0.0, shape=(2, ), dtype=np.float32)

    def reset(self):
        self.step_number_env=0
        self.world = World(initialization_year=2018, scenario_file=self.config['scenario_file'], data_folder=self.config['data_folder'], number_of_steps=self.max_number_of_steps)
        self.world.step_number -= 1
        resultant_observation = self.world.step(17)
        mean_electricity_price = resultant_observation[0]
        carbon_emitted = resultant_observation[1]
        obs = np.array([mean_electricity_price, carbon_emitted]) 
        # obs = -abs(mean_electricity_price)-abs(carbon_emitted)

        # obs = np.random.uniform(low=-100, high=1, size=(2,))
        obs = np.array(obs)
        # return np.expand_dims(obs, axis=0)
        return obs

    def step(self, action):
        self.action = action
        self.step_number_env += 1
        resultant_observation = self.world.step(action)
        mean_electricity_price = resultant_observation[0]
        carbon_emitted = resultant_observation[1]

        ob = -abs(mean_electricity_price)-abs(carbon_emitted)
        reward = ob
        done = self.world.step_number > self.max_number_of_steps
        print("step number: {}, action: {}, reward: {}, mean_electricity_price: {}, carbon_emitted: {}".format(self.world.step_number,action, reward, mean_electricity_price, carbon_emitted))

        ob = np.array([mean_electricity_price, carbon_emitted])

        return ob, reward, done, {}

    def render(self):

        return False
