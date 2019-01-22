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

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"


if __name__ == '__main__':

    number_of_steps = 40

    fixed_params = {"initialization_year": 2018,
                "number_of_steps": number_of_steps}
    # variable_params = {"carbon_price_scenario": [[20]*50,[30]*50, [40]*50, [45]*50 ,[50]*50, [55]*50,[65]*50, [75]*50, [85]*50,[95]*50, [100]*50, [200]*50, list(range(17, 177, 4)) , list(range(101, 21, -2))],
    #               "demand_change": [[1.01]*50, [0.990]*50]
    #                }
    variable_params = {"carbon_price_scenario": [[20]*50,[90]*50],
                  "demand_change": [[1.01]*50]
                   }

    batch_run = BatchRunnerMP(World,
                          fixed_parameters=fixed_params,
                          variable_parameters=variable_params,
                          iterations=5,
                          max_steps=number_of_steps, nr_processes=2)



    batch_run.run_all()
    # br_df = batch_run.get_model_vars_dataframe()
    # br_step_data = pd.DataFrame()
    # for i in range(len(br_df["Data Collector"])):
    #     if isinstance(br_df["Data Collector"][i], DataCollector):
    #         i_run_data = br_df["Data Collector"][i].get_model_vars_dataframe()
    #         br_step_data = br_step_data.append(i_run_data, ignore_index=True)
    # br_step_data.to_csv("BankReservesModel_Step_Data.csv")
