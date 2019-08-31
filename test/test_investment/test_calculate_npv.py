from logging import getLogger, basicConfig, DEBUG
from unittest.mock import Mock

import pandas as pd
import pytest

from elecsim.constants import ROOT_DIR
from elecsim.plants.plant_costs.estimate_costs.estimate_costs import create_power_plant
from elecsim.role.investment.calculate_npv import CalculateNPV, select_yearly_payback_payment_for_year
from elecsim.role.investment.calculate_npv import get_yearly_payment

logger = getLogger(__name__)

"""
File name: test_calculate_npv
Date created: 04/01/2019
Feature: # Tests for the calculation of NPV
"""

basicConfig(level=DEBUG)


__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"

class TestCalculate_npv:

    @pytest.fixture(scope='function')
    def calculate_latest_NPV(self):
        DISCOUNT_RATE = 0.001
        LOOK_BACK_YEARS = 4
        model = Mock()
        model.year_number=2018
        model.step_number=5
        model.demand.segment_consumption = [52152, 45209, 42206, 39585, 37480, 35505, 34182, 33188, 32315, 31567, 30721, 29865, 28935, 27888, 26760, 25520, 24327, 23127, 21964, 17568]
        model.PowerExchange.load_duration_curve_prices = pd.read_csv('{}/test/test_investment/dummy_load_duration_prices.csv'.format(ROOT_DIR))
        npv_calculations = CalculateNPV(model, DISCOUNT_RATE, LOOK_BACK_YEARS)
        return npv_calculations

    @pytest.mark.parametrize("year, plant_type, capacity, expected_output",
                             [
                                 # (2018, "CCGT", 1200, 82.55488),
                                 (2018, "Recip_gas", 20, 60)
                             ])
    def test_calculate_expected_cash_flow(self, calculate_latest_NPV, year, plant_type, capacity, expected_output):

        yearly_npv = calculate_latest_NPV.calculate_npv(plant_type, plant_size=capacity)
        logger.debug(yearly_npv)


    @pytest.mark.parametrize("year, plant_type, capacity, expected_output",
                             [
                                 (2018, "Nuclear", 3300, 514111666.67),
                             ])
    def test_calculate_expected_capital_cost(self, calculate_latest_NPV, year, plant_type, capacity, expected_output):
        power_plant = create_power_plant("Test", year, plant_type, capacity)
        yearly_capital_cost = calculate_latest_NPV._get_capital_outflow(power_plant)
        logger.debug(yearly_capital_cost)
        assert yearly_capital_cost == pytest.approx(expected_output)


    @pytest.mark.parametrize("year, plant_type, capacity, expected_output",
                             [
                                 (2018, "Nuclear", 3300, 874963277.93),
                             ])
    def test_calculate_expected_yearly_outflow(self, calculate_latest_NPV, year, plant_type, capacity, expected_output):
        power_plant = create_power_plant("Test", year, plant_type, capacity)
        SHORT_RUN_MARGINAL_COST = 8.9
        TOTAL_RUNNING_HOURS = 8752.42
        TOTAL_YEARLY_INCOME = 1646133520
        YEARLY_CAPITAL_COST = 514111666.67
        yearly_outflow = calculate_latest_NPV._calculate_yearly_operation_cashflow(power_plant, SHORT_RUN_MARGINAL_COST, TOTAL_RUNNING_HOURS, TOTAL_YEARLY_INCOME, YEARLY_CAPITAL_COST)
        assert yearly_outflow == pytest.approx(expected_output)

    @pytest.mark.parametrize("year, plant_type, capacity, expected_output",
                             [
                                 (2018, "Nuclear", 3300, 30.29),
                             ])
    def test_calculate_expected_yearly_profit_per_mwh(self, calculate_latest_NPV, year, plant_type, capacity, expected_output):
        power_plant = create_power_plant("Test", year, plant_type, capacity)
        TOTAL_RUNNING_HOURS = 8752.42
        YEARLY_OUTFLOW = 874963277.93
        yearly_profit_per_mwh = calculate_latest_NPV._get_yearly_profit_per_mwh(power_plant=power_plant, total_running_hours=TOTAL_RUNNING_HOURS, yearly_cash_flow=YEARLY_OUTFLOW)
        assert yearly_profit_per_mwh == pytest.approx(expected_output, abs=0.01)


    def test_overall_npv_calculation(self, calculate_latest_NPV):
        calculate_latest_NPV.get_positive_npv_plants_list()

    def test_npv_calculation_comparison(self, calculate_latest_NPV):
        calculate_latest_NPV.compare_npv()

    @pytest.mark.parametrize("year, plant_type, capacity, expected_output",
                             [
                                 (2018, "Nuclear", 3300, 30.29),
                             ])
    def test_calculate_yearly_loan_payment(self, calculate_latest_NPV, year, plant_type, capacity, expected_output):
        power_plant = create_power_plant("Test", year, plant_type, capacity)
        monthly_rate = get_yearly_payment(power_plant, 0.06)
        logger.debug("monthly_rate: {}".format(monthly_rate))

    @pytest.mark.parametrize("year, plant_type, capacity, expected_output",
                             [
                                 (2018, "Nuclear", 3300, 30.29),
                             ])
    def test_select_yearly_payback_payment_for_year(self, year, plant_type, capacity, expected_output):
        power_plant = create_power_plant("Test", year, plant_type, capacity)
        model = Mock()
        model.year_number=2020
        select_yearly_payback_payment_for_year(power_plant, 0.6, model)


    # @pytest.mark.parametrize("year, plant_type, capacity, expected_output",
    #                          [
    #                              # (2018, "CCGT", 1200, 82.55488),
    #                              (2018, "Recip_gas", 20, 60)
    #                          ])
    # def test_calculate_expected_cash_flow(self, calculate_latest_NPV, year, plant_type, capacity, expected_output):
    #
    #     yearly_npv = calculate_latest_NPV.calculate_npv_costs(plant_type, plant_size=capacity, )
    #     logger.debug(yearly_npv)
