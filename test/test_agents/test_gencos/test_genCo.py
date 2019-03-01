import logging

import pandas as pd

from elecsim.agents.generation_company.gen_co import GenCo
from elecsim.constants import ROOT_DIR
from elecsim.model.world import World
from elecsim.plants.plant_costs.estimate_costs.estimate_costs import create_power_plant

logger = logging.getLogger(__name__)

import pytest

"""
File name: test_genCo
Date created: 31/12/2018
Feature: # Tests for generation companies
"""
from unittest.mock import Mock

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"

logging.basicConfig(level=logging.DEBUG)

# class TestGenCo:
#
#     @pytest.mark.parametrize("year_number, expected_output",
#                              [
#                                  (2010, [True, False, True, True]),
#                                  (2020, [True, True, True, True]),
#                                  (1993, [False, False, False, True]),
#                                  (1970, [False, False, False, False]),
#                              ])
#     def test_operate_constructed_plants(self, year_number, expected_output):
#         model = Mock()
#         model.year_number = year_number
#         plant1 = create_power_plant("plant1", 1990, "CCGT", 1200)
#         plant2 = create_power_plant("plant2", 2010, "Onshore", 60)
#         plant3 = create_power_plant("plant3", 1990, "Offshore", 120)
#         plant4 = create_power_plant("plant4", 1980, "Coal", 120)
#
#         genco = GenCo(1, model, "Test", 0.06, [plant1, plant2, plant3, plant4])
#
#
#
#         genco.operate_constructed_plants()
#         for plant, expected_result in zip(genco.plants, expected_output):
#             assert plant.is_operating == expected_result
#
#
#     @pytest.mark.parametrize("year_number, expected_name, expected_output",
#                              [
#                                  (2020, ["Plant_1", "Plant_2"], 2),
#                                  (2080, [], 0),
#                                  (2037, ['Plant_1'], 1),
#                              ])
#     def test_check_plants_end_of_life(self, year_number, expected_name, expected_output):
#         model = Mock()
#         model.year_number = year_number
#
#         plant = Mock()
#         plant.name = "Plant_1"
#         plant.construction_year = 2015
#         plant.operating_period = 25
#         plant.construction_period = 1
#         plant.pre_dev_period = 1
#         plant.in_service = True
#
#         plant2 = Mock()
#         plant2.name = "Plant_2"
#         plant2.construction_year = 2015
#         plant2.operating_period = 18
#         plant2.construction_period = 1
#         plant2.pre_dev_period = 1
#         plant2.in_service = True
#
#         UNIQUE_ID = 1
#         DISCOUNT_RATE = 0.06
#         genco = GenCo(UNIQUE_ID, model, "test_genco", DISCOUNT_RATE, [plant, plant2])
#         genco.dismantle_old_plants()
#         assert len(genco.plants)==expected_output
#         for plant, name in zip(genco.plants, expected_name):
#             assert plant.name == name
#
#
#     def test_genco_investment(self):
#         model = Mock()
#         model.year_number = 2021
#         model.step_number = 5
#         model.PowerExchange.load_duration_curve_prices = pd.read_csv('{}/test/test_investment/dummy_load_duration_prices.csv'.format(ROOT_DIR))
#
#
#         plant = Mock()
#         plant.name = "Plant_1"
#         plant.construction_year = 2015
#         plant.operating_period = 25
#         plant.construction_period = 1
#         plant.pre_dev_period = 1
#         plant.in_service = True
#
#         plant2 = Mock()
#         plant2.name = "Plant_2"
#         plant2.construction_year = 2015
#         plant2.operating_period = 18
#         plant2.construction_period = 1
#         plant2.pre_dev_period = 1
#         plant2.in_service = True
#
#         UNIQUE_ID = 1
#         DISCOUNT_RATE = 0.06
#         genco = GenCo(UNIQUE_ID, model, "test_genco", DISCOUNT_RATE, [plant, plant2])
#
#         genco.invest()


