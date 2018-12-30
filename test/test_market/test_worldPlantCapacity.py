from src.role.market.world_plant_capacity import WorldPlantCapacity
from src.plants.plant_costs.estimate_costs.estimate_costs import create_power_plant
from src.agents.generation_company.gen_co import GenCo
from unittest.mock import Mock
import logging
"""
File name: test_worldPlantCapacity
Date created: 30/12/2018
Feature: #Enter feature description here
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"

logging.basicConfig(level=logging.DEBUG)


class TestWorldPlantCapacity:
    def test_get_capacity(self):
        model = Mock()
        agent1 = Mock(spec=GenCo)
        agent2 = Mock(spec=GenCo)
        plant1 = create_power_plant("plant1", 1990, "CCGT", 1200)
        plant2 = create_power_plant("plant2", 2010, "Onshore", 60)
        plant3 = create_power_plant("plant3", 1990, "Offshore", 120)
        plant4 = create_power_plant("plant3", 1980, "Coal", 120)


        agent1.plants = [plant1, plant2, plant3]
        agent2.plants = [plant4]

        schedule = Mock()
        schedule.agents = [agent1, agent2]
        model.schedule = schedule
        calculate_capacity = WorldPlantCapacity(model)
        calculate_capacity.get_total_capacity()
