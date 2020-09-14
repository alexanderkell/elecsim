import os.path
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from mesa.batchrunner import BatchRunnerMP

from elecsim.model.world import World

import logging
import numpy as np
import pandas as pd
import glob
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

    m = 10.96667
    c = 130.889

    y = range(17)

    carbon_tax = [year * m + c for year in y]
    carbon_tax = ["optimal_carbon_policy"] + carbon_tax

    beis_params = [0.00121256259168, 46.850377392563864, 0.0029982421515, 28.9229765616468, 0.00106156336814, 18.370337670063762, 0.00228312539654, 0.0, 0.0024046471141100003, 34.43480109190594, 0.0, -20.88014916953091, 0.0, 8.15032953348701, 0.00200271495761, -12.546185375581802, 0.00155518243668, 39.791132970522796, 0.00027449937576, 8.42878689508516, 0.00111989525697, 19.81640207212787, 0.00224091998324, 5.26288570922149, 0.00209189353332, -5.9117317131295195, 0.00240696026847, -5.0144941135222, 0.00021183142492999999, -1.29658413335784, 0.00039441444392000004, -11.41659250225168, 0.00039441444392000004, -11.41659250225168, 120.21276910611674, 0.0, 0.00059945111227]

    if len(sys.argv) == 1:
        data_folder = "/sensitivity_analysis/data/sensitivity_analysis_results/downpayment/wacc_059"

    else:
        data_folder = sys.argv[1]

    # path = '/Users/alexanderkell/Documents/PhD/Projects/10-ELECSIM/run/sensitivity_analysis/scenario_files/wacc/'  # use your path
    path = '/Users/alexanderkell/Documents/PhD/Projects/10-ELECSIM/run/sensitivity_analysis/scenario_files/upfront_investment_costs'  # use your path
    all_files = glob.glob(path + "/*.py")

    scenario_files = []
    for file in all_files:
        scenario_files.append(file)



    prices_individual = np.array(beis_params[:-3]).reshape(-1, 2).tolist()

    nuclear_subsidy = beis_params[-3]
    future_price_uncertainty_m = beis_params[-2]
    future_price_uncertainty_c = beis_params[-1]

    MARKET_TIME_SPLICES = 8
    YEARS_TO_RUN = 17
    number_of_steps = YEARS_TO_RUN * MARKET_TIME_SPLICES

    fixed_params = {"initialization_year": 2018,
                    "carbon_price_scenario": carbon_tax,
                    "market_time_splices": MARKET_TIME_SPLICES,
                    "data_folder": data_folder,
                    "number_of_steps": number_of_steps,
                    "long_term_fitting_params": prices_individual,
                    "highest_demand": 63910,
                    "nuclear_subsidy": beis_params[-3],
                    "future_price_uncertainty_m": beis_params[-2],
                    "future_price_uncertainty_c": beis_params[-1],
                    "dropbox": False,
                    "demand_change": [0.99]* number_of_steps}



    variable_params = {"scenario_file": scenario_files}




    print(scenario_files)
    batch_run = BatchRunnerMP(World,
                              fixed_parameters=fixed_params,
                              variable_parameters=variable_params,
                              iterations=10,
                              max_steps=number_of_steps, nr_processes=7)

    batch_run.run_all()

