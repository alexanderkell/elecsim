import sys
import os
from multiprocessing import Process
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
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

# from run.intelligent_bidding.run.run import run_scenario
# from run.intelligent_bidding.RL_server.intelligent_bidding_rl_server import run_agent
import multiprocessing as mp

import logging
logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

import pandas as pd
import os.path
import sys
import numpy as np
import pickle
from fitter import Fitter
import fitter

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from elecsim.model.world import World
import tracemalloc

import pandas as pd
import linecache
import time
from elecsim.constants import ROOT_DIR
import logging
logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)
from scipy.stats import johnsonsb, skewnorm, dgamma, genlogistic, dweibull, johnsonsu
import ray

from concurrent import futures


@ray.remote
def run_scenario(gencos_rl_bidding, port_number):
    print("Running scenario with: {}".format(gencos_rl_bidding))

    time.sleep(180)
    beis_params = [0.00121256259168, 46.850377392563864, 0.0029982421515, 28.9229765616468, 0.00106156336814,
                   18.370337670063762, 0.00228312539654, 0.0, 0.0024046471141100003, 34.43480109190594, 0.0,
                   -20.88014916953091, 0.0, 8.15032953348701, 0.00200271495761, -12.546185375581802, 0.00155518243668,
                   39.791132970522796, 0.00027449937576, 8.42878689508516, 0.00111989525697, 19.81640207212787,
                   0.00224091998324, 5.26288570922149, 0.00209189353332, -5.9117317131295195, 0.00240696026847,
                   -5.0144941135222, 0.00021183142492999999, -1.29658413335784, 0.00039441444392000004,
                   -11.41659250225168, 0.00039441444392000004, -11.41659250225168, 120.21276910611674, 0.0,
                   0.00059945111227]

    prices_individual = np.array(beis_params[:-3]).reshape(-1, 2).tolist()

    MARKET_TIME_SPLICES = 8
    YEARS_TO_RUN = 1
    number_of_steps = YEARS_TO_RUN * MARKET_TIME_SPLICES

    scenario_2018 = "../scenario/reference_scenario_2018.py".format(ROOT_DIR)


    carbon_df = pd.read_csv('linear_data_exploded.csv'.format(ROOT_DIR))
    carbon_list = carbon_df.x.tolist()

    # result_distributions_object = pickle.load(open(
    #     "{}/run/market_forecasting_comparison/run/Compare_worlds/result_distributions_object.p".format(ROOT_DIR),
    #     "rb"))
    #
    # resultant_dist = '{}'
    #
    # dist_class = eval(list(result_distributions_object[resultant_dist].fitted_param.keys())[0] + ".rvs")
    # dist_object = dist_class(*list(result_distributions_object[resultant_dist].fitted_param.values())[0],
    #                          size=50000).tolist()

    while True:
        world = World(carbon_price_scenario=carbon_list, initialization_year=2018, scenario_file=scenario_2018,
                      market_time_splices=MARKET_TIME_SPLICES, data_folder="compare_ml_accuracy",
                      number_of_steps=number_of_steps, long_term_fitting_params=prices_individual, highest_demand=63910,
                      nuclear_subsidy=beis_params[-3], future_price_uncertainty_m=beis_params[-2],
                      future_price_uncertainty_c=beis_params[-1], dropbox=False, gencos_rl=gencos_rl_bidding,
                      write_data_to_file=True, rl_port_number=port_number)

        for _ in range(YEARS_TO_RUN):
            for i in range(MARKET_TIME_SPLICES):
                # try:
                if i / 8 == 0:
                    print('end of year')
                world.step()

# SERVER_ADDRESS = "rllibserver"
# SERVER_ADDRESS = "localhost"
# SERVER_PORT = 9920
# CHECKPOINT_FILE = "last_checkpoint.out"

class MarketServing(ExternalEnv):

    def __init__(self, number_of_plants, server_port=9920, max_bid=600):
        self.SERVER_ADDRESS = "localhost"
        # SERVER_PORT = 9920
        self.CHECKPOINT_FILE = "last_checkpoint.out"
        self.server_port = server_port
        self.max_bid = max_bid

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
            action_space=Box(low=0, high=self.max_bid, shape=(self.number_of_plants,), dtype=np.float),
            observation_space=Box(np.array(lower_bounds), np.array(upper_bounds)))

    def run(self):
        print("Starting policy server at {}:{}".format(self.SERVER_ADDRESS,
                                                       self.server_port))
        server = PolicyServer(self, self.SERVER_ADDRESS, self.server_port)
        server.serve_forever()


# if __name__ == "__main__":
@ray.remote
def run_agent(port_number, number_of_plants=14, max_bid=600):
    # ray.init(redis_max_memory=10000000000, object_store_memory=3000000000, memory=2000000000)
    print("Starting agent")
    # ray.init()
    # number_of_plants = 25
    # number_of_plants = 37

    register_env("srv_{}".format(port_number), lambda _: MarketServing(number_of_plants, port_number, max_bid))

    tune.run_experiments({
        "rl_bidding_{}_{}_max_bid_{}".format(number_of_plants, port_number, max_bid): {
            # "run": "PG",
            "run": "DDPG",
            "env": "srv_{}".format(port_number),
            # 'checkpoint_at_end': True,
            # 'checkpoint_freq': 5,
            # 'restore': '../../../../../../../ray_results/rl_bidding/DDPG_srv_0_2020-05-25_16-11-377wk6ln6z/checkpoint_30/checkpoint-30',
            "config": {
                # "num_gpus": 0,
                # "num_workers": 1,
                "env": "srv_{}".format(port_number),
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

@ray.remote
def run_agent_and_server_parallel(port_number, gencos_rl_bidding, number_of_plants, max_bid):

    print(port_number)
    print(gencos_rl_bidding)

    ray.get([run_agent.remote(port_number, number_of_plants, max_bid), run_scenario.remote(gencos_rl_bidding, port_number)])
    # p1 = Process(target=run_agent, args=(port_number,))
    # p1.start()
    #
    # p2 = Process(target=run_scenario, args=(gencos_rl_bidding, port_number))
    # p2.start()
    #
    # p1.join()
    # p2.join()


if __name__ == "__main__":
    ray.init(num_cpus=mp.cpu_count()-1)
    # gencos_rl_bidding = ['EDF Energy', 'RWE Generation SE', 'test']

    # gencos_rl_bidding = [["EDF Energy"],
    #                      ["EDF Energy", "RWE Generation SE"],
    #                      ["EDF Energy", "RWE Generation SE", "SSE"],
    #                      ["EDF Energy", "RWE Generation SE", "SSE", "Uniper UK Limited"],
    #                      ["EDF Energy", "RWE Generation SE", "SSE", "Uniper UK Limited", "Scottish power"],
    #                      ["EDF Energy", "RWE Generation SE", "SSE", "Uniper UK Limited", "Scottish power",
    #                       "Drax Power Ltd"], ['Orsted'], ['RWE Generation SE'], ['SSE'], ['Uniper UK Limited'],
    #                      ['Scottish power'], ['Drax Power Ltd'], ["Magnox Ltd"]]

    gencos_rl_bidding = ["EDF Energy", "RWE Generation SE", "SSE", "Uniper UK Limited", "Scottish power", "Drax Power Ltd"]

    # number_of_plants = [14, 25, 155, 164, 213, 216, 11, 11, 130, 9, 49, 3]

    number_of_plants = 216

    # plant_names = [["EDF Energy"],
    #              ["EDF Energy", "RWE Generation SE"],
    #              ["EDF Energy", "RWE Generation SE", "SSE"],
    #              ["EDF Energy", "RWE Generation SE", "SSE", "Uniper UK Limited"],
    #              ["EDF Energy", "RWE Generation SE", "SSE", "Uniper UK Limited", "Scottish power"],
    #              ["EDF Energy", "RWE Generation SE", "SSE", "Uniper UK Limited", "Scottish power",
    #               "Drax Power Ltd"], ['Orsted'], ['RWE Generation SE'], ['SSE'], ['Uniper UK Limited'],
    #              ['Scottish power'], ['Drax Power Ltd'], ["Magnox Ltd"]]

    # max_bid = 150
    # max_bids = [100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200]
    max_bids = [120, 140, 160, 180, 190]
    # max_bid = 600

    # for genco_group in gencos_rl_bidding:
    #     print(genco_group)

    results = []
    # for port_number, gencos, plant_number in zip(range(9951, 9951+len(gencos_rl_bidding)), gencos_rl_bidding, number_of_plants):
    for port_number, max_bid in zip(range(9951, 9951+len(max_bids)), max_bids):
        print(port_number)
        print(max_bid)
        # result = run_agent_and_server_parallel.remote(port_number, gencos)
        result = run_agent_and_server_parallel.remote(port_number, gencos_rl_bidding, number_of_plants, max_bid)
        results.append(result)

    ray.get(results)








