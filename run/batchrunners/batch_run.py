from mesa.batchrunner import BatchRunner
from mesa.datacollection import DataCollector
import pandas as pd

from src.model.world import World
"""
File name: batch_run
Date created: 19/01/2019
Feature: # Enables world to be run multiple times based on different parameter sweeps.
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"


br_params = {"carbon_tax": [25, 100, 150, 200],
             "demand": [5, 10, 15, 20],
            }


batch_run = BatchRunner(World,
                 br_params,
                 iterations=1,
                 max_steps=32,
                 model_reporters={"Data Collector": lambda m: m.datacollector})

if __name__ == '__main__':
    batch_run.run_all()
    br_df = batch_run.get_model_vars_dataframe()
    br_step_data = pd.DataFrame()
    for i in range(len(br_df["Data Collector"])):
        if isinstance(br_df["Data Collector"][i], DataCollector):
            i_run_data = br_df["Data Collector"][i].get_model_vars_dataframe()
            br_step_data = br_step_data.append(i_run_data, ignore_index=True)
    br_step_data.to_csv("BankReservesModel_Step_Data.csv")
