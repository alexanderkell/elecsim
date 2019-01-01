from src.agents.generation_company.gen_co import GenCo

import logging

logger = logging.getLogger(__name__)

"""
File name: plant_capacity
Date created: 30/12/2018
Feature: # Functionality that aggregates all of the power plants in operation.
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"


class WorldPlantCapacity:
    def __init__(self, model):
        self.model = model

    def get_total_capacity(self):
        self.get_power_plants_running_in_current_year()

    def get_power_plants_running_in_current_year(self):
        plant_list = [plant for agent in self.model.schedule.agents if isinstance(agent, GenCo) for plant in
                      agent.plants if plant.is_operating is True]

        return plant_list

    def get_power_plants_running_in_reference_year(self, reference_year):
        plant_list = [plant for agent in self.model.schedule.agents if isinstance(agent, GenCo) for plant in
                      agent.plants if
                      reference_year < plant.construction_year + plant.operating_period + plant.pre_dev_period + plant.construction_period
                      and reference_year > plant.construction_year + plant.pre_dev_period + plant.construction_period]
        return plant_list
