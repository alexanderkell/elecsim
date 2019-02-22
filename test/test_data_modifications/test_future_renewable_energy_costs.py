import logging

import pytest
from pytest import approx

from elecsim.data_manipulation.data_modifications.renewable_learning_rate import future_renewable_energy_costs
from elecsim.plants.plant_costs.estimate_costs.estimate_modern_power_plant_costs.predict_modern_plant_costs import PredictModernPlantParameters
from elecsim.plants.plant_registry import PlantRegistry

logger = logging.getLogger(__name__)

"""
File name: test_future_renewable_energy_costs
Date created: 21/12/2018
Feature: # Test for future renewable energy costs.
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"

logging.basicConfig(level=logging.DEBUG)

class TestFuture_renewable_energy_costs:
    @pytest.fixture(scope='function')
    def calculate_latest_lcoe(self):
        logging.info('Selecting latest power plant data')

        estimated_cost_parameters = PredictModernPlantParameters("PV", 50, 2020).parameter_estimation()

        power_plant_obj = PlantRegistry("PV").plant_type_to_plant_object()
        power_plant = power_plant_obj(name="Test", plant_type="PV",
                                      capacity_mw=50, construction_year=2020,
                                      **estimated_cost_parameters)

        lcoe = power_plant.calculate_lcoe(0.05)

        return lcoe

    def test_future_renewable_energy_costs(self, calculate_latest_lcoe):
        logging.info("Testing future renewable energy costs using scenario data")

        starting_lcoe = calculate_latest_lcoe
        logging.debug("Starting LCOE is: {}".format(calculate_latest_lcoe))

        learning_rate = 0.5
        total_capacity = 5
        future_pv_lcoe = future_renewable_energy_costs(starting_lcoe, learning_rate, total_capacity)

        assert future_pv_lcoe == approx(11.073375565720812)







