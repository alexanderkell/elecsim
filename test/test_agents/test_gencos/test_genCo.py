from src.agents.generation_company.gen_co import GenCo

from unittest.mock import Mock
import pytest
import logging

logger = logging.getLogger(__name__)

"""
File name: test_genCo
Date created: 30/12/2018
Feature: #Enter feature description here
"""


__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"

logging.basicConfig(level=logging.DEBUG)


class TestGenCo:



    @pytest.mark.parametrize("year_number, expected_name, expected_output",
                             [
                                 (2020, ["Plant_1", "Plant_2"], 2),
                                 (2080, [], 0),
                                 (2037, ['Plant_1'], 1),
                             ])
    def test_check_plants_end_of_life(self, year_number, expected_name, expected_output):
        model = Mock()
        model.year_number = year_number

        plant = Mock()
        plant.name = "Plant_1"
        plant.construction_year = 2015
        plant.operating_period = 25
        plant.construction_period = 1
        plant.pre_dev_period = 1
        plant.in_service = True

        plant2 = Mock()
        plant2.name = "Plant_2"
        plant2.construction_year = 2015
        plant2.operating_period = 18
        plant2.construction_period = 1
        plant2.pre_dev_period = 1
        plant2.in_service = True

        UNIQUE_ID = 1
        DISCOUNT_RATE = 0.06
        genco = GenCo(UNIQUE_ID, model, "test_genco", DISCOUNT_RATE, [plant, plant2])
        genco.check_plants_end_of_life()
        assert len(genco.plants)==expected_output
        for plant, name in zip(genco.plants, expected_name):
            assert plant.name == name