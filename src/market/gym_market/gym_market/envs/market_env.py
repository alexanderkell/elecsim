"""
File name: market_env
Date created: 21/12/2018
Feature: #Enter feature description here
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"

import gym
from gym import error, spaces, utils
from gym.utils import seeding
from mesa import Agent
import numpy as np

from src.market.electricity.power_exchange import PowerExchange





class MarketEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    """
    Description:
        A market is created where an agent must maximise revenue from selling electricity. In this simple case,
        a bid is accepted as long as the bid submitted is smaller than 50. Therefore, the agent should learn to
        always bid 49.99

    Observation:
        Type: Discrete(4)
        Num	Observation                 0         1
        0	Bid status                  rejected  accepted


    Actions:
        Type: Box()
        Num	Range
        0	-inf, inf   Bid made to sell electricty

        Note: The amount the velocity is reduced or increased is not fixed as it depends on the angle the pole is pointing. This is because the center of gravity of the pole increases the amount of energy needed to move the cart underneath it
    Reward:
        Reward is 0.1 for every unit of money earned
    Starting State:
        All observations are assigned 0
    Episode Termination:
        Episode length is greater than 200
    Solved Requirements
        Considered solved when the average reward is greater than or equal to 9800.
    """
    def __init__(self, shared, idx):
        self.action_space = spaces.Box(low=-1000, high=1000, shape=(1,), dtype=np.float32)
        self.observation_space = spaces.Discrete(2)
        self.number_of_steps = None
        self.idx = idx
        self.shared = shared

    def step(self, action):
        done = False
        bid_status = False
        reward = 0
        if action > 50:
            bid_status = False
        else:
            bid_status = True
            reward = action
        self.number_of_steps += 1
        if self.number_of_steps >200:
            done = True


        #  the next state, the reward for the current state, done?, additional info on our problem
        return bid_status, reward, False, {}

    def reset(self):
        self.number_of_steps = None

        return False
