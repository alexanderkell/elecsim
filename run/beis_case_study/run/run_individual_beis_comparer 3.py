import sys

from multiprocessing import Pool, cpu_count
import pickle
sys.path.insert(0, '/home/alexkell/elecsim/')

from elecsim.model.world import World

import pandas as pd

from elecsim.constants import ROOT_DIR
import logging
logger = logging.getLogger(__name__)
import numpy as np


"""
File name: run_individual_beis_comparer
Date created: 23/10/2019
Feature: #Enter feature description here
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"

# ga_results = pd.read_csv('run/beis_case_study/data/GA_optimisation_results/GA_results.csv')
# ga_results = pd.read_csv('/Users/b1017579/Documents/PhD/Projects/10. ELECSIM/run/beis_case_study/data/GA_optimisation_results/GA_results.csv')

# ga_results_small = ga_results[ga_results.reward < 10].iloc[:,7:-5]
# params_list = ga_results_small.values.tolist()
#
#
# params_repeated = np.repeat(params_list, 100, axis=0)
#
# params_repeated_list = params_repeated.tolist()
#
# params_repeated_list = np.array([0]*74).reshape(2,-1).tolist()


# ray.init()

# @ray.remote
def eval_world_parallel(individual):
    prices_individual = np.array(individual[:-3]).reshape(-1, 2).tolist()
    # print(prices_individual)
    MARKET_TIME_SPLICES = 8
    YEARS_TO_RUN = 18
    number_of_steps = YEARS_TO_RUN * MARKET_TIME_SPLICES

    scenario_2018 = "{}/../run/beis_case_study/scenario/reference_scenario_2018.py".format(ROOT_DIR)
    world = World(initialization_year=2018, scenario_file=scenario_2018, market_time_splices=MARKET_TIME_SPLICES, data_folder="best_run_beis_comparison", number_of_steps=number_of_steps, long_term_fitting_params=prices_individual, highest_demand=63910, nuclear_subsidy=individual[-3], future_price_uncertainty_m=individual[-2], future_price_uncertainty_c=individual[-1])

    for j in range(YEARS_TO_RUN):
        for i in range(MARKET_TIME_SPLICES):
            try:
                # print("j:{}, i: {}".format(j, i))
                results_df, over_invested = world.step()
            except:
                return 99999, 0
    del world
    return individual, results_df


#
# results_id = []
# for param_list in params_repeated_list:
#     results_id.append(eval_world_parallel.remote(param_list))
#
# results = ray.get(results_id)
#
# with open('results.pkl', 'wb') as f:
#     pickle.dump(results, f)


params_repeated_list = np.repeat([[0.00121256259168, 46.850377392563864, 0.0029982421515, 28.9229765616468, 0.00106156336814, 18.370337670063762, 0.00228312539654, 0.0, 0.0024046471141100003, 34.43480109190594, 0.0, -20.88014916953091, 0.0, 8.15032953348701, 0.00200271495761, -12.546185375581802, 0.00155518243668, 39.791132970522796, 0.00027449937576, 8.42878689508516, 0.00111989525697, 19.81640207212787, 0.00224091998324, 5.26288570922149, 0.00209189353332, -5.9117317131295195, 0.00240696026847, -5.0144941135222, 0.00021183142492999999, -1.29658413335784, 0.00039441444392000004, -11.41659250225168, 0.0021988838824299997, 12.633572943294599, 120.21276910611674, 0.0, 0.00059945111227]]
                                 , 500, axis=0)

pool = Pool(cpu_count())
out1, out2 = zip(*pool.map(eval_world_parallel, params_repeated_list))

# with open('out1.pkl', 'wb') as f:
#     pickle.dump(out1, f)
#
# with open('out2.pkl', 'wb') as f:
#     pickle.dump(out2, f)
