from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

"""
File name: investor_server
Date created: 17/07/2019
Feature: #Enter feature description here
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"

"""Example of running a policy server. Copy this file for your use case.
To try this out, in two separate shells run:
    $ python cartpole_server.py
    $ python cartpole_client.py
"""

import sys
import os
from multiprocessing import Process
import time

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))


import os
from gym import spaces
from gym.spaces import Tuple, Box
import numpy as np

import ray
from ray.rllib.agents.dqn import DQNTrainer
from ray.rllib.agents.ppo import PPOTrainer
from ray.rllib.agents.pg import PGTrainer
from ray.rllib.env.external_env import ExternalEnv
from ray.rllib.env.external_multi_agent_env import ExternalMultiAgentEnv
from ray.rllib.utils.policy_server import PolicyServer
from ray.tune.logger import pretty_print
from ray.tune.registry import register_env
from gym.spaces import Tuple, Box, MultiDiscrete, Discrete
from ray import tune
from ray.rllib.env.multi_agent_env import MultiAgentEnv

# SERVER_ADDRESS = "rllibserver"
SERVER_ADDRESS = "localhost"
SERVER_PORT = 9920
CHECKPOINT_FILE = "last_checkpoint.out"


class MarketServing(ExternalEnv):

    def __init__(self, number_of_plants):

        self.number_of_plants = number_of_plants
        lower_bounds = [-100000] * 7
        # lower_bounds.extend([-99999])

        upper_bounds = [10000000] * 7
        # upper_bounds.extend([99999])

        ExternalEnv.__init__(
            self,
            # MultiDiscrete([16, 10]),
            # Discrete(159),
            # action_space=Box(shape=37),
            # action_space=Box(low=0, high=200, shape=(37,), dtype=np.float),
            action_space=Box(low=0, high=600, shape=(self.number_of_plants,), dtype=np.float),
            observation_space=Box(np.array(lower_bounds), np.array(upper_bounds))
        )

    def run(self):
        print("Starting policy server at {}:{}".format(SERVER_ADDRESS,
                                                       SERVER_PORT))
        server = PolicyServer(self, SERVER_ADDRESS, SERVER_PORT)
        server.serve_forever()


# if __name__ == "__main__":
def run_agent():
    # ray.init(redis_max_memory=10000000000, object_store_memory=3000000000, memory=2000000000)
    print("Starting agent")
    ray.init()
    number_of_plants = 25
    # number_of_plants = 37

    register_env("srv", lambda _: MarketServing(number_of_plants))

    tune.run_experiments({
        "rl_bidding_{}".format(number_of_plants): {
            # "run": "PG",
            "run": "DDPG",
            "env": "srv",
            'checkpoint_at_end': True,
            'checkpoint_freq': 5,
            # 'restore': '../../../../../../../ray_results/rl_bidding/DDPG_srv_0_2020-05-25_16-11-377wk6ln6z/checkpoint_30/checkpoint-30',
            "config": {
                # "num_gpus": 0,
                # "num_workers": 1,
                "env": "srv",
                "evaluation_num_episodes": 1,
                # "sgd_stepsize": tune.grid_search([0.01, 0.001, 0.0001])
                "sample_batch_size": 100,
                "train_batch_size": 200,
                # "horizon": 25,
                # "exploration_config": {
                #     # The Exploration class to use.
                #     "type": "EpsilonGreedy",
                #     # Config for the Exploration class' constructor:
                #     "initial_epsilon": 1.0,
                #     "final_epsilon": 0.1,
                    # "epsilon_timesteps": 10000,  # Timesteps over which to anneal epsilon.

                    # For soft_q, use:
                    # "exploration_config" = {
                    #   "type": "SoftQ"
                    #   "temperature": [float, e.g. 1.0]
                    # }
                },
            }
        # }
    })

# if __name__ == "__main__":
#     run_agent()