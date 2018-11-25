'''
File name: test_nonFuelOldPlantCosts
Date created: 25/11/2018
Feature: # Tests for Non Fuel Old Plant Cost Estimation, using LCOE values, mapped to modern plant costs.
'''
from unittest import TestCase
from src.plants.plant_costs.estimate_costs.estimate_old_plant_cost_params.non_fuel_plants_old_params import NonFuelOldPlantCosts

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"


class TestNonFuelOldPlantCosts(TestCase):
    def test_estimate_cost_parameters(self):
        non_fuel_plant = NonFuelOldPlantCosts(2018, "PV", 1200, 0.035)
        assert non_fuel_plant.estimate_cost_parameters() ==
