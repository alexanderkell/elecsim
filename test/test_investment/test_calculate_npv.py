from src.role.investment.calculate_npv import CalculateNPV
from src.plants.plant_costs.estimate_costs.estimate_costs import create_power_plant
from constants import ROOT_DIR

import pandas as pd
import pytest
from unittest.mock import Mock

from logging import getLogger, basicConfig, DEBUG
logger = getLogger(__name__)

"""
File name: test_calculate_npv
Date created: 04/01/2019
Feature: #Enter feature description here
"""

basicConfig(level=DEBUG)


__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"

class TestCalculate_npv:

    @pytest.fixture(scope='function')
    def calculate_latest_NPV(self):
        DISCOUNT_RATE = 0.06
        START_YEAR = 2018
        EXPECTED_PRICE = 70
        LOOK_BACK_YEARS = 4
        model = Mock()
        model.year_number=2018
        model.step_number=5
        model.PowerExchange.load_duration_curve_prices = pd.read_csv('{}/test/test_investment/dummy_load_duration_prices.csv'.format(ROOT_DIR))
        npv_calculations = CalculateNPV(model, DISCOUNT_RATE, LOOK_BACK_YEARS)
        return npv_calculations


    @pytest.mark.parametrize("year, plant_type, capacity, expected_output",
                             [
                                 (2018, "CCGT", 1200, 82.55488),
                             ])
    def test_calculate_expected_cash_flow(self, calculate_latest_NPV, year, plant_type, capacity, expected_output):
        load_duration_prices = pd.read_csv('{}/test/test_investment/dummy_load_duration_prices.csv'.format(ROOT_DIR))

        yearly_npv = calculate_latest_NPV.calculate_npv(plant_type, plant_size=capacity)
        logger.debug(yearly_npv)

    def test_npv_calcualtion_comparison(self, calculate_latest_NPV):
        calculate_latest_NPV.compare_npv()
