#! /bin/env python3
import os

import pytz
import os.path
import sys
from datetime import date, datetime, timedelta
sys.path.append(os.path.join(os.path.dirname(os.path.realpath('__file__')), '../../..'))
ROOT_DIR = os.path.join(os.path.dirname(os.path.realpath('__file__')), '')

import os.path
import sys
import pickle
import ray
from elecsim.model.world import World

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



logging.basicConfig(level=logging.INFO)

MARKET_TIME_SPLICES = 8
YEARS_TO_RUN = 25
number_of_steps = YEARS_TO_RUN * MARKET_TIME_SPLICES

# print("ROOT_DIR: {}".format(ROOT_DIR))

scenario_file = "{}/scenario/scenario_data.py".format(ROOT_DIR)

@ray.remote
def run_world(num_steps=number_of_steps, demand_distribution=None):
    world = World(initialization_year=2018, market_time_splices=MARKET_TIME_SPLICES, data_folder="results", number_of_steps=number_of_steps, scenario_file=scenario_file, demand_distribution=demand_distribution)
    for i in range(num_steps):
        world.step()


# results = []
if __name__ == '__main__':
    ray.init()
    result_distributions_object = pickle.load(open("{}/../run/market_forecasting_comparison/data/distribution_objects/result_distributions_object.p".format(ROOT_DIR), "rb"))
    print(result_distributions_object)
    for resultant_dists in result_distributions_object:
        # print(resultant_dists)

        dist_class = eval(list(result_distributions_object[resultant_dists].fitted_param.keys())[0] + ".rvs")
        dist_object = dist_class(*list(result_distributions_object[resultant_dists].fitted_param.values())[0],
                                 size=10000)
        print(dist_object)
        for j in range(150):

            run_world.remote(number_of_steps, dist_object)

        time.sleep(30)

    os.execv(sys.executable, [sys.executable] + sys.argv)



