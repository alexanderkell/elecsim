"""
File name: test_future_renewable_energy_costs
Date created: 21/12/2018
Feature: #Enter feature description here
"""
import pytest
import unittest
# from scenario.scenario_data import modern_plant_costs
import pandas as pd

from src.plants.plant_costs.estimate_costs.estimate_modern_power_plant_costs.predict_modern_plant_costs import PredictModernPlantParameters
from constants import ROOT_DIR
import logging
logger = logging.getLogger(__name__)


from src.data_manipulation.data_modifications.renewable_learning_rate import future_renewable_energy_costs
import numpy as np


__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"

logging.basicConfig(level=logging.DEBUG)


class TestFuture_renewable_energy_costs:
    @pytest.fixture(scope='function')
    def select_data(self):
        logging.info('Selecting latest power plant data')
        # modern_plant_costs = pd.read_csv('{}/data/processed/power_plants/power_plant_costs/modern_power_plant_costs/power_plant_costs_with_simplified_type.csv'.format(ROOT_DIR))
        #
        # pv = modern_plant_costs[modern_plant_costs.Type=='PV']

        PredictModernPlantParameters("PV", 50, 2020).parameter_estimation()
        return pv

    def test_future_renewable_energy_costs(self, select_data):
        # future_costs = future_renewable_energy_costs(modern_plant_costs)
        logging.info("Testing future renewable energy costs using scenario data")
        logging.debug(select_data.columns)
        assert 1 == 1







