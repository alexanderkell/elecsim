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

import os
from gym import spaces
from gym.spaces import Tuple, Box
import numpy as np

import ray
from ray.rllib.agents.dqn import DQNTrainer
from ray.rllib.agents.ppo import PPOTrainer
from ray.rllib.agents.pg import PGTrainer
# from ray.rllib.env.external_env import ExternalEnv
from ray.rllib.env.external_multi_agent_env import ExternalMultiAgentEnv
from ray.rllib.utils.policy_server import PolicyServer
from ray.tune.logger import pretty_print
from ray.tune.registry import register_env
from gym.spaces import Tuple, Box, MultiDiscrete, Discrete
from ray import tune
from ray.rllib.env.multi_agent_env import MultiAgentEnv


# SERVER_ADDRESS = "rllibserver"
SERVER_ADDRESS = "localhost"
SERVER_PORT = 9900
CHECKPOINT_FILE = "last_checkpoint.out"

class MarketServing(ExternalMultiAgentEnv):

    def __init__(self):

        lower_bounds = [-1000000]*8
        lower_bounds.extend([-99999999999999999999999999])

        upper_bounds = [1000000]*8
        upper_bounds.extend([99999999999999999999999999])

        ExternalMultiAgentEnv.__init__(
            self,
            MultiDiscrete([16, 10]),
            # Discrete(29, shape=(1, 2)),
            # Box(low=-1, high=1000, shape=(31,), dtype=np.float)
            Box(np.array(lower_bounds), np.array(upper_bounds))
        )

    def run(self):
        print("Starting policy server at {}:{}".format(SERVER_ADDRESS,
                                                       SERVER_PORT))
        server = PolicyServer(self, SERVER_ADDRESS, SERVER_PORT)
        server.serve_forever()


if __name__ == "__main__":

    ray.init(redis_max_memory=10000000000, object_store_memory=3000000000, memory=2000000000)
    # ray.init()

    register_env("srv", lambda _: MarketServing())

    # We use DQN since it supports off-policy actions, but you can choose and
    # configure any agent.
    # dqn = PPOTrainer(
    #     env="srv",
    #     config={
    #         # Use a single process to avoid needing to set up a load balancer
    #         # "num_workers": 0,
    #         "evaluation_num_episodes": 1,
    #         # "sample_batch_size": 40,
    #         # "train_batch_size": 40,
    #         # "horizon": 40,
    #     })
    #
    # # Attempt to restore from checkpoint if possible.
    # # if os.path.exists(CHECKPOINT_FILE):
    # #     checkpoint_path = open(CHECKPOINT_FILE).read()
    # #     print("Restoring from checkpoint path", checkpoint_path)
    # #     dqn.restore(checkpoint_path)
    #
    # # Serving and training loop
    # while True:
    #     print(pretty_print(dqn.train()))
    #     checkpoint_path = dqn.save()
    #     print("Last checkpoint", checkpoint_path)
    #     with open(CHECKPOINT_FILE, "w") as f:
    #         f.write(checkpoint_path)



    tune.run_experiments({
        "my_experiment": {
            "run": "PG",
            "env": "srv",
            'checkpoint_at_end': True,
            'checkpoint_freq': 5,
            #'restore': '../ray_results/my_experiment/PG_srv_0_2019-11-04_14-39-5995j0aobf/checkpoint_220/checkpoint-220',
            "config": {
                # "num_gpus": 0,
                # "num_workers": 1,
                "env": "srv",
                "evaluation_num_episodes": 10,
                # "sgd_stepsize": tune.grid_search([0.01, 0.001, 0.0001])
                "sample_batch_size": 15,
                "train_batch_size": 15,
                # "horizon": 25,
                #'compress_observations':True
            }
        }
    })
