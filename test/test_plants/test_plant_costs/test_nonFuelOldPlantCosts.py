'''
File name: test_nonFuelOldPlantCosts
Date created: 25/11/2018
Feature: # Tests for Non Fuel Old Plant Cost Estimation, using LCOE values, mapped to modern plant costs.
'''
from unittest import TestCase

from elecsim.plants.plant_costs.estimate_costs.estimate_old_plant_cost_params.non_fuel_plant_calculations.non_fuel_plants_old_params import NonFuelOldPlantCosts

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"


class TestNonFuelOldPlantCosts(TestCase):
    def test_estimate_cost_parameters(self):
        non_fuel_plant = NonFuelOldPlantCosts(2015, "PV", 1200)
        parameters = non_fuel_plant.get_cost_parameters()
        # assert parameters['connection_cost_per_mw'] == pytest.approx(6292.8209054998)
        # assert parameters['construction_cost_per_mw'] == pytest.approx(953.457712954515)

