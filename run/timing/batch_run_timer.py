import os.path
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from mesa.batchrunner import BatchRunnerMP
# from src.mesa_addons.BatchRunnerMP_timer import BatchRunnerMP

from src.model.world import World


from src.scenario.scenario_data import power_plants
import logging

logger = logging.getLogger(__name__)

# logging.basicConfig(level=logging.INFO)

"""
File name: batch_run_timer
Date created: 25/01/2019
Feature: # Functionality to time run of model at different sized countries
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"






class DemandTimer:

    def __init__(self):
        self.power_plants = power_plants


    def run_world_with_demand_and_power_plants(self):

        number_of_steps = 40
        data_folder = "minimum_sized_country"

        fixed_params = {
            "initialization_year": 2018,
            "number_of_steps": number_of_steps,
            "demand_change": [1.0] * 50,
            "carbon_price_scenario": [40]*50,
            "data_folder": data_folder,
            "time_run":True
        }

        variable_params = {
            "total_demand": [
                500,
                750,
                1000,
                1250,
                1500,
                1750,
                2000,
                2500,
                3000,
                3500,
                4000,
                4500,
                5000,
                5500,
                6000,
                10000
            ]
        }



        batch_run = BatchRunnerMP(World,
                                  fixed_parameters=fixed_params,
                                  variable_parameters=variable_params,
                                  iterations=5,
                                  max_steps=number_of_steps, nr_processes=3)

        batch_run.run_all()


if __name__ == "__main__":
    DemandTimer().run_world_with_demand_and_power_plants()
