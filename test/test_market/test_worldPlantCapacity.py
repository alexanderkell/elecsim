import logging
from unittest.mock import Mock

import pytest

from elecsim.agents.generation_company.gen_co import GenCo
from elecsim.plants.plant_costs.estimate_costs.estimate_costs import create_power_plant
from elecsim.role.market.world_plant_capacity import WorldPlantCapacity

logger = logging.getLogger(__name__)
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
    @pytest.mark.parametrize("reference_year, expected_output",
                         [
                             (2019, ['plant1', 'plant2', 'plant3']),
                             (2011, ['plant1', 'plant3', 'plant4']),
                             (2080, []),
                             (2030, ['plant2']),
                             (1990, ['plant4'])
                         ])
    def test_get_capacity(self, reference_year, expected_output):
        model = Mock()
        plant1 = create_power_plant("plant1", 1990, "CCGT", 1200)
        plant2 = create_power_plant("plant2", 2010, "Onshore", 60)
        plant3 = create_power_plant("plant3", 1990, "Offshore", 120)
        plant4 = create_power_plant("plant4", 1980, "Coal", 120)

        agent1 = GenCo(1, model, "Test", 0.06, [plant1, plant2, plant3])
        agent2 = GenCo(1, model, "Test", 0.06, [plant4])


        model.year_number = reference_year
        agent1.operate_constructed_plants()
        agent2.operate_constructed_plants()
        agent1.dismantle_old_plants()
        agent2.dismantle_old_plants()
        schedule = Mock()
        schedule.agents = [agent1, agent2]
        model.schedule = schedule


        calculate_capacity = WorldPlantCapacity(model)
        plant_list = calculate_capacity.get_power_plants_running_in_current_year()


        for plant, expected_name in zip(plant_list, expected_output):
            logger.debug("{}, {}".format(plant.name, expected_name))
            assert plant.name == expected_name


    @pytest.mark.parametrize("reference_year, expected_output",
                         [
                             (2019, ['plant1', 'plant2', 'plant3']),
                             (2011, ['plant1', 'plant3', 'plant4']),
                             (2080, []),
                             (2030, ['plant2']),
                             (1990, ['plant4'])
                         ])
    def test_get_power_plants_running_in_reference_year(self, reference_year, expected_output):

        model = Mock()
        plant1 = create_power_plant("plant1", 1990, "CCGT", 1200)
        plant2 = create_power_plant("plant2", 2010, "Onshore", 60)
        plant3 = create_power_plant("plant3", 1990, "Offshore", 120)
        plant4 = create_power_plant("plant4", 1980, "Coal", 120)

        agent1 = GenCo(1, model, "Test", 0.06, [plant1, plant2, plant3])
        agent2 = GenCo(1, model, "Test", 0.06, [plant4])


        model.year_number = 2018
        agent1.operate_constructed_plants()
        agent2.operate_constructed_plants()
        agent1.dismantle_old_plants()
        agent2.dismantle_old_plants()
        schedule = Mock()
        schedule.agents = [agent1, agent2]
        model.schedule = schedule


        calculate_capacity = WorldPlantCapacity(model)
        plant_list = calculate_capacity.get_power_plants_running_in_reference_year(reference_year)
        for plant, expected_name in zip(plant_list, expected_output):
            logger.debug("{}, {}".format(plant.name, expected_name))
            assert plant.name == expected_name

    @pytest.mark.parametrize("reference_year, expected_output",
                         [
                             (2019, 1380),
                             (2011, 1320),
                             (2080, 0),
                             (2030, 60),
                         ])
    def test_get_reference_year_total_capacity(self, reference_year, expected_output):

        model = Mock()
        plant1 = create_power_plant("plant1", 1990, "CCGT", 1200)
        plant2 = create_power_plant("plant2", 2010, "Onshore", 60)
        plant3 = create_power_plant("plant3", 1990, "Offshore", 120)
        plant4 = create_power_plant("plant4", 1980, "Coal", 120)

        agent1 = GenCo(1, model, "Test", 0.06, [plant1, plant2, plant3])
        agent2 = GenCo(1, model, "Test", 0.06, [plant4])

        model.year_number = 2018
        agent1.operate_constructed_plants()
        agent2.operate_constructed_plants()
        agent1.dismantle_old_plants()
        agent2.dismantle_old_plants()
        schedule = Mock()
        schedule.agents = [agent1, agent2]
        model.schedule = schedule

        calculate_capacity = WorldPlantCapacity(model)

        assert calculate_capacity.get_reference_year_total_capacity(reference_year) == expected_output
