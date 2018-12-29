from constants import KW_TO_MW

from src.role.investment.latest_market_data import LatestMarketData

import pytest
from unittest import mock
from pytest import approx

import logging
logger = logging.getLogger(__name__)
"""
File name: test_latestMarketData
Date created: 29/12/2018
Feature: # Tests for calculating the latest market data.
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"

logging.basicConfig(level=logging.DEBUG)

class TestLatestMarketData:

    @pytest.fixture(scope="function")
    def latest_market_data(self):
        model = mock.Mock()
        model.step_number = 5
        market_data = LatestMarketData(model)
        return market_data

    @pytest.mark.parametrize('value_required, years_to_look_back, expected_output',
                             [
                                 ('co2', 4, 23.665),
                                 ('demand', 4, 1.02),
                                 ('gas', 4, 18.977),
                                 ('coal', 4, 9.06),

                             ])
    def test_demand_data(self, latest_market_data, value_required, years_to_look_back, expected_output):

        market_data = latest_market_data
        assert market_data.agent_forecast_value(value_required, years_to_look_back) == expected_output




    @pytest.mark.parametrize("value_required, years_to_look_back, years_from_start, expected_output",
                             [
                                 ("demand", 4, 3, [1.00, 1.00, 1.00, 1.01]),
                                 ("demand", 6, 3, [1.00, 1.00, 1.00, 1.00, 1.00, 1.01]),
                                 ("demand", 6, 10, [1.01, 1.02, 1.02, 1.03, 1.02, 1.01]),
                                 ("gas", 6, 10, [18.977, 18.977, 18.977, 18.977, 18.977, 18.977]),
                                 ("gas", 6, 2, [18.977, 18.977, 18.977, 18.977, 18.977, 18.977]),
                                 ("gas", 3, 2, [18.977, 18.977, 18.977]),
                                 ("coal", 3, 2, [9.06, 9.06, 9.06]),
                                 ("uranium", 3, 2, [3.9, 3.9, 3.9]),
                                 ("co2", 3, 10, [26.50, 27.92, 29.33]),
                             ])
    def test_get_yearly_demand_change_for_regression(self, value_required, latest_market_data, years_to_look_back, years_from_start, expected_output):
        market_data = latest_market_data
        market_data.demand.years_from_start = years_from_start
        years_for_regression = list(range(market_data.demand.years_from_start-years_to_look_back-1,market_data.demand.years_from_start-1))
        value_data = market_data._get_value_data(value_required)
        assert market_data._get_yearly_demand_change_for_regression(value_data, years_for_regression) == approx(expected_output)


    @pytest.mark.parametrize("value_required, expected_output",
                            [
                                ("GAS", [KW_TO_MW * 0.018977] * 60),
                                ("gas", [KW_TO_MW * 0.018977] * 60),
                                ("coal", [KW_TO_MW * 0.00906] * 60),
                                ("uranium", [KW_TO_MW * 0.0039] * 60),
                                ("co2", [18.00, 19.42, 20.83, 22.25, 23.67, 25.08, 26.50, 27.92, 29.33, 30.75, 32.17, 33.58, 35.00, 43.25, 51.50, 59.75, 68.00, 76.25, 84.50, 92.75, 101.00, 109.25, 117.50, 125.75, 134.00, 142.25, 150.50, 158.75, 167.00, 175.25, 183.50, 191.75, 200.00])
                            ])
    def test_switch_statements_for_value_data(self, latest_market_data, value_required, expected_output):
        assert latest_market_data._switch_statements_for_price_data(value_required) == expected_output

    def test_switch_statements_for_valueerror_for_value_data(self, latest_market_data):
        with pytest.raises(ValueError):
            assert latest_market_data._switch_statements_for_price_data("sdfsf")
        with pytest.raises(ValueError):
            assert latest_market_data._switch_statements_for_price_data(-1)
