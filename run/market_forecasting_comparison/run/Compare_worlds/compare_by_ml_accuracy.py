#! /bin/env python3
import os

# import pytz
import os.path
import sys
from datetime import date, datetime, timedelta
# sys.path.append(os.path.join(os.path.dirname(os.path.realpath('__file__')), '../../..'))
# sys.path.insert(0, 'home/alexkell/elecsim3')
# ROOT_DIR = os.path.join(os.path.dirname(os.path.realpath('__file__')), '')
ROOT_DIR = "~/elecsim3/elecsim/"
from joblib import Parallel, delayed
import os.path
import sys
import pickle
import ray
from elecsim.model.world import World

from tqdm import tqdm
import multiprocessing

import sys

import numpy as np
# import multiprocessing
import tracemalloc
from elecsim.constants import ROOT_DIR

import pandas as pd
import pickle
import seaborn as sns
import matplotlib.pyplot as plt
from fitter import Fitter
import fitter
from scipy import stats
import importlib
from scipy.stats import johnsonsb, skewnorm, dgamma, genlogistic, dweibull, johnsonsu


import time
import logging

"""
File name: compare_by_ml_accuracy
Date created: 19/04/2020
Feature: #Enter feature description here
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"

import warnings
warnings.filterwarnings("ignore")


logging.basicConfig(level=logging.INFO)

MARKET_TIME_SPLICES = 8
YEARS_TO_RUN = 25
number_of_steps = YEARS_TO_RUN * MARKET_TIME_SPLICES

# print("ROOT_DIR: {}".format(ROOT_DIR))

scenario_file = "{}/scenario/reference_scenario_beis_2018.py".format(ROOT_DIR)

# scenario_file = "{}/../run/beis_case_study/scenario/reference_scenario_2018.py".format(ROOT_DIR)

# @ray.remote

def run_world(optimal_carbon_tax=None, distribution_name = None, demand_distribution=None):
    beis_params = [0.00121256259168, 46.850377392563864, 0.0029982421515, 28.9229765616468, 0.00106156336814, 18.370337670063762, 0.00228312539654, 0.0, 0.0024046471141100003, 34.43480109190594, 0.0, -20.88014916953091, 0.0, 8.15032953348701, 0.00200271495761, -12.546185375581802, 0.00155518243668, 39.791132970522796, 0.00027449937576, 8.42878689508516, 0.00111989525697, 19.81640207212787, 0.00224091998324, 5.26288570922149, 0.00209189353332, -5.9117317131295195, 0.00240696026847, -5.0144941135222, 0.00021183142492999999, -1.29658413335784, 0.00039441444392000004, -11.41659250225168, 0.00039441444392000004, -11.41659250225168, 120.21276910611674, 0.0, 0.00059945111227]
    # beis_params = [0.00121256259168, 46.850377392563864, 0.0029982421515, 28.9229765616468, 0.00106156336814, 18.370337670063762, 0.00228312539654, 0.0, 0.0024046471141100003, 34.43480109190594, 0.0, -20.88014916953091, 0.0, 8.15032953348701, 0.00200271495761, -12.546185375581802, 0.00155518243668, 39.791132970522796, 0.00027449937576, 8.42878689508516, 0.00111989525697, 19.81640207212787, 0.00224091998324, 5.26288570922149, 0.00209189353332, -5.9117317131295195, 0.00240696026847, -5.0144941135222, 0.00021183142492999999, -1.29658413335784, 0.00039441444392000004, -11.41659250225168, 0.0021988838824299997, 12.633572943294599, 120.21276910611674, 0.0, 0.00059945111227]

    prices_individual = np.array(beis_params[:-3]).reshape(-1, 2).tolist()

    MARKET_TIME_SPLICES = 8
    YEARS_TO_RUN = 25
    number_of_steps = YEARS_TO_RUN * MARKET_TIME_SPLICES

    scenario_2018 = "{}/scenario/reference_scenario_beis_2018.py".format(ROOT_DIR)

    # if individual[0] == 1:
    #     individual = [individual[1]*i + individual[2] for i in range(1, 20)]
    # else:
    #     individual = [individual[3]*i ** individual[4] + individual[2] for i in range(1, 20)]
    # individual = [individual[0]*i + individual[1] for i in range(1, 20)]
    # print(individual)


    world = World(demand_distribution=demand_distribution, distribution_name = distribution_name, carbon_price_scenario=optimal_carbon_tax, initialization_year=2018, scenario_file=scenario_2018, market_time_splices=MARKET_TIME_SPLICES, data_folder="compare_ml_accuracy", number_of_steps=number_of_steps, long_term_fitting_params=prices_individual, highest_demand=63910, nuclear_subsidy=beis_params[-3], future_price_uncertainty_m=beis_params[-2], future_price_uncertainty_c=beis_params[-1])
    for _ in range(YEARS_TO_RUN):
        for i in range(MARKET_TIME_SPLICES):
            # try:
            if i/8 == 0:
                print('end of year')

            world.step()
    # return None


# @ray.remote
# def run_world(num_steps=number_of_steps, demand_distribution=None, long_term_fitting_params=None, optimal_carbon_tax = None):
#     world = World(initialization_year=2018, market_time_splices=MARKET_TIME_SPLICES, data_folder="results", number_of_steps=number_of_steps, scenario_file=scenario_file, demand_distribution=demand_distribution, long_term_fitting_params=long_term_fitting_params, carbon_price_scenario=optimal_carbon_tax)
#     for i in range(num_steps):
#         world.step()


# results = []
if __name__ == '__main__':
    # ray.init(num_cpus=7)

    beis_params = [0.00121256259168, 46.850377392563864, 0.0029982421515, 28.9229765616468, 0.00106156336814, 18.370337670063762, 0.00228312539654, 0.0, 0.0024046471141100003, 34.43480109190594, 0.0, -20.88014916953091, 0.0, 8.15032953348701, 0.00200271495761, -12.546185375581802, 0.00155518243668, 39.791132970522796, 0.00027449937576, 8.42878689508516, 0.00111989525697, 19.81640207212787, 0.00224091998324, 5.26288570922149, 0.00209189353332, -5.9117317131295195, 0.00240696026847, -5.0144941135222, 0.00021183142492999999, -1.29658413335784, 0.00039441444392000004, -11.41659250225168, 0.00039441444392000004, -11.41659250225168, 120.21276910611674, 0.0, 0.00059945111227]

    prices_individual = np.array(beis_params[:-3]).reshape(-1, 2).tolist()

    MARKET_TIME_SPLICES = 8
    YEARS_TO_RUN = 17
    number_of_steps = YEARS_TO_RUN * MARKET_TIME_SPLICES

    scenario_2018 = "reference_scenario_2018.py".format(ROOT_DIR)

    prices_individual = np.array(beis_params[:-3]).reshape(-1, 2).tolist()

    carbon_df = pd.read_csv('linear_data_exploded.csv'.format(ROOT_DIR))
    carbon_list = carbon_df.x.tolist()

    result_distributions_object = pickle.load(open("result_distributions_object.p".format(ROOT_DIR), "rb"))
    # print(result_distributions_object)
    for resultant_dists in result_distributions_object:
        # print(resultant_dists)

        dist_class = eval(list(result_distributions_object[resultant_dists].fitted_param.keys())[0] + ".rvs")
        dist_object = dist_class(*list(result_distributions_object[resultant_dists].fitted_param.values())[0], size=50000).tolist()

        # print(dist_object))
        # run_world(carbon_list, resultant_dists, dist_object)
        Parallel(n_jobs=multiprocessing.cpu_count()-1)(delayed(run_world)(carbon_list, resultant_dists, dist_object) for i in tqdm(range(0, 100)))
        # Parallel(n_jobs=7)(delayed(run_world)(carbon_list, resultant_dists, dist_object) for i in tqdm(range(0, 100)))
        # pool.map(run_world(number_of_steps, dist_object, prices_individual, carbon_list), list(range(0, 150)))

        # time.sleep(30)

    os.execv(sys.executable, [sys.executable] + sys.argv)



