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
        plant_list = []
        for agent in self.model.schedule.agents:
            if isinstance(agent, GenCo):
                for plants in agent.plants:
                    plant_list.append(plants)
                    
        logger.debug("Plant list: {}".format(len(plant_list)))
