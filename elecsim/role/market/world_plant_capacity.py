import logging

from elecsim.agents.generation_company.gen_co import GenCo
from elecsim.plants.plant_type.non_fuel_plant import NonFuelPlant

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

    def get_current_total_plant_capacity(self):
        plant_list = self.get_power_plants_running_in_current_year()
        total_capacity = self._calculate_total_capacity(plant_list)
        return total_capacity

    def get_renewable_plants(self):
        all_plants = self.get_power_plants_running_in_current_year()
        renewable_plants = [plant for plant in all_plants if isinstance(plant, NonFuelPlant)]
        return renewable_plants

    def get_renewable_by_type(self, type):
        renewable_plants = self.get_renewable_plants()
        renewable_type = [onshore_plant for onshore_plant in renewable_plants if onshore_plant.plant_type == type]
        return renewable_type

    def get_reference_year_total_capacity(self, reference_year):
        plant_list = self.get_power_plants_running_in_reference_year(reference_year)
        for i in plant_list:
            logger.debug(i.name)
        total_capacity = self._calculate_total_capacity(plant_list)
        return total_capacity

    def _calculate_total_capacity(self, plant_list):
        sumation = sum(plant.capacity_mw for plant in plant_list)
        return sumation

    def get_power_plants_running_in_current_year(self):
        plant_list = [plant for agent in self.model.schedule.agents if isinstance(agent, GenCo) for plant in
                      agent.plants if plant.is_operating is True]

        return plant_list

    def get_power_plants_running_in_reference_year(self, reference_year):
        plant_list = [plant for agent in self.model.schedule.agents if isinstance(agent, GenCo) for plant in
                      agent.plants if
                      plant.construction_year + plant.pre_dev_period + plant.construction_period < reference_year < plant.construction_year + plant.operating_period + plant.pre_dev_period + plant.construction_period]
        return plant_list
