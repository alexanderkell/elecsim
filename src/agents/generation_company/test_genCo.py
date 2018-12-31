from src.agents.generation_company.gen_co import GenCo
from src.plants.plant_costs.estimate_costs.estimate_costs import create_power_plant

import logging
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

class TestGenCo:

    @pytest.mark.parametrize("year_number, expected_output",
                             [
                                 (2010, [True, False, True, True]),
                                 (2020, [True, True, True, True]),
                                 (1993, [False, False, False, True]),
                                 (1970, [False, False, False, False]),
                             ])
    def test_operate_constructed_plants(self, year_number, expected_output):
        model = Mock()
        model.year_number = year_number
        plant1 = create_power_plant("plant1", 1990, "CCGT", 1200)
        plant2 = create_power_plant("plant2", 2010, "Onshore", 60)
        plant3 = create_power_plant("plant3", 1990, "Offshore", 120)
        plant4 = create_power_plant("plant4", 1980, "Coal", 120)

        genco = GenCo(1, model, "Test", 0.06, [plant1, plant2, plant3, plant4])
        genco.operate_constructed_plants()
        for plant, expected_result in zip(genco.plants, expected_output):
            assert plant.is_operating == expected_result

