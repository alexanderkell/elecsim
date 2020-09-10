import mysql.connector
from mysql.connector import errorcode

import os.path
import sys
import ray
from pathlib import Path
from multiprocessing import Pool
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from elecsim.model.world import World
import tracemalloc

import pandas as pd
import linecache

from elecsim.constants import ROOT_DIR
import string
from deap import algorithms
from deap import base
from deap import benchmarks
from deap.benchmarks.tools import diversity, convergence, hypervolume
from deap import creator
from deap import tools

import array
import random
import logging
logger = logging.getLogger(__name__)
import numpy as np

from pathlib import Path
project_dir = Path("__file__").resolve().parents[1]



import array


creator.create("FitnessMin", base.Fitness, weights=(-1.0, -1.0))
creator.create("Individual", array.array, typecode='d', fitness=creator.FitnessMin)

beis_params = [0.00121256259168, 46.850377392563864, 0.0029982421515, 28.9229765616468, 0.00106156336814, 18.370337670063762, 0.00228312539654, 0.0, 0.0024046471141100003, 34.43480109190594, 0.0, -20.88014916953091, 0.0, 8.15032953348701, 0.00200271495761, -12.546185375581802, 0.00155518243668, 39.791132970522796, 0.00027449937576, 8.42878689508516, 0.00111989525697, 19.81640207212787, 0.00224091998324, 5.26288570922149, 0.00209189353332, -5.9117317131295195, 0.00240696026847, -5.0144941135222, 0.00021183142492999999, -1.29658413335784, 0.00039441444392000004, -11.41659250225168, 0.00039441444392000004, -11.41659250225168, 120.21276910611674, 0.0, 0.00059945111227]
# beis_params = [0.00121256259168, 46.850377392563864, 0.0029982421515, 28.9229765616468, 0.00106156336814, 18.370337670063762, 0.00228312539654, 0.0, 0.0024046471141100003, 34.43480109190594, 0.0, -20.88014916953091, 0.0, 8.15032953348701, 0.00200271495761, -12.546185375581802, 0.00155518243668, 39.791132970522796, 0.00027449937576, 8.42878689508516, 0.00111989525697, 19.81640207212787, 0.00224091998324, 5.26288570922149, 0.00209189353332, -5.9117317131295195, 0.00240696026847, -5.0144941135222, 0.00021183142492999999, -1.29658413335784, 0.00039441444392000004, -11.41659250225168, 0.0021988838824299997, 12.633572943294599, 120.21276910611674, 0.0, 0.00059945111227]

prices_individual = np.array(beis_params[:-3]).reshape(-1, 2).tolist()

MARKET_TIME_SPLICES = 8
YEARS_TO_RUN = 17
number_of_steps = YEARS_TO_RUN * MARKET_TIME_SPLICES

scenario_2018 = "{}/../run/beis_case_study/scenario/reference_scenario_2018.py".format(ROOT_DIR)


individual = [18.08]*27
print(individual)

def run_scenario(ignore):
    print(ignore)
    world = World(carbon_price_scenario=individual[:-1], initialization_year=2018, scenario_file=scenario_2018, market_time_splices=MARKET_TIME_SPLICES, data_folder="UK_carbon_scenario_data", number_of_steps=number_of_steps, long_term_fitting_params=prices_individual, highest_demand=63910, nuclear_subsidy=beis_params[-3], future_price_uncertainty_m=beis_params[-2], future_price_uncertainty_c=beis_params[-1])
    for _ in range(YEARS_TO_RUN):
        for i in range(MARKET_TIME_SPLICES):
            # try:
            if i/8 == 0:
                print('end of year')

            average_electricity_price, carbon_emitted = world.step()
            # except Exception as e:
            #     print("try catch error: \n{}".format(e))
            #     return 889999999999999999, 889999999999999999
            # if carbon_emitted is bool:
            if isinstance(carbon_emitted, bool):
                print("carbon emitted error")
                # return 999999999999999999, 999999999999999999

            if not isinstance(average_electricity_price, float):
                # print("average_electricity_price {}, type {}".format(average_electricity_price, type(average_electricity_price)))
                print("average_electricity_price")
                average_electricity_price = 779999999999999999
            if not isinstance(carbon_emitted, float):
                print("carbon_emitted {}, type {}".format(carbon_emitted, type(carbon_emitted)))
                carbon_emitted = 779999999999999999

    print("average_electricity_price: {}, carbon_emitted: {}".format(average_electricity_price, carbon_emitted))


pool = Pool(8)

*pool.map(run_scenario, range(0, 100))