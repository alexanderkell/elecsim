"""
File name: investor_gym.py
Date created: 17/07/2019
Feature: #Enter feature description here
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"

from ray.rllib.env.multi_agent_env import MultiAgentEnv
from gym.spaces import Tuple, Box, MultiDiscrete

import numpy as np

class InvestorGym(MultiAgentEnv):

    action_space = MultiDiscrete([19,1000])
    observation_space = Box(low=-1, high=1000, shape=(1,), dtype=np.float)

    def __init__(self, gen_cos):
        self.gen_cos = gen_cos


    def step(self, action_dict):

    def reset(self):
        return {"{}".format(gen_co.name): 0 for gen_co in self.gen_cos}
