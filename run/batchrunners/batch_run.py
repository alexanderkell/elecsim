import os.path
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from mesa.batchrunner import BatchRunnerMP
from mesa.datacollection import DataCollector
import pandas as pd

from src.scenario import scenario_data
from src.model.world import World

import logging



"""
File name: batch_run
Date created: 19/01/2019
Feature: # Enables world to be run multiple times based on different parameter sweeps.
"""
logging.basicConfig(level=logging.INFO)

# logging.basicConfig(level=logging.INFO, filename="logfile_no_dismantling", filemode="a+",
#                         format="%(asctime)-15s %(levelname)-8s %(message)s")

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"


if __name__ == '__main__':
    if len(sys.argv) == 1:
        data_folder = "run"
    else:
        data_folder = sys.argv[1]
    number_of_steps = 38

    fixed_params = {"initialization_year": 2013,
                    "number_of_steps": number_of_steps,
                    "data_folder": data_folder}

    # variable_params = {"carbon_price_scenario": [[20]*50,[30]*50, [40]*50, [45]*50 ,[50]*50, [55]*50,[65]*50, [75]*50, [85]*50,[95]*50, [100]*50, [200]*50, list(range(17, 177, 4)) , list(range(101, 21, -2))],
    #               "demand_change": [[1.01]*50, [0.990]*50]
    #                }
    # variable_params = {"carbon_price_scenario": [[0]*50, [10]*50 ,[20]*50, [30]*50, [40]*50, [50]*50, [60]*50, [70]*50, [80]*50,[90]*50, [100]*50, [150]*50,[200]*50 ,list(range(18, 174, 4)), list(range(174, 18, -4)) ],
    #               "demand_change": [[1.01]*50, [0.99]*50]
    #                }


    variable_params = {"carbon_price_scenario": [[30] * 50],
    "demand_change": [[1.01] * 50]
    }



    batch_run = BatchRunnerMP(World,
                              fixed_parameters=fixed_params,
                              variable_parameters=variable_params,
                              iterations=1,
                              max_steps=number_of_steps, nr_processes=1)

    batch_run.run_all()

