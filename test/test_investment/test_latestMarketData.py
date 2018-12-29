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
        # demand = mock.Mock()
        model = mock.Mock()
        model.demand.yearly_demand_change = [1.00, 1.01, 1.02, 1.01, 1.02, 1.02, 1.03, 1.02, 1.01, 1.02, 0.99, 1, 1, 1, 1.01, 1.02, 1.01, 1.01, 1, 1]
        model.demand.years_from_start = 3
        market_data = LatestMarketData(model)
        return market_data

    def test_demand_data(self, latest_market_data):

        market_data = latest_market_data
        logger.debug("regression: {}".format(market_data.demand_data(4)))


    @pytest.mark.parametrize("years_to_look_back, years_from_start, expected_output",
                             [
                                 (4, 3, [1.00, 1.00, 1.00, 1.01]),
                                 (6, 3, [1.00, 1.00, 1.00, 1.00, 1.00, 1.01]),
                                 (6, 10, [1.01, 1.02, 1.02, 1.03, 1.02, 1.01]),
                             ])
    def test_get_yearly_demand_change_for_regression(self, latest_market_data, years_to_look_back, years_from_start, expected_output):
        market_data = latest_market_data
        years_to_look_back = years_to_look_back
        market_data.demand.years_from_start = years_from_start
        years_for_regression = list(range(market_data.demand.years_from_start-years_to_look_back-1,market_data.demand.years_from_start-1))

        assert market_data._get_yearly_demand_change_for_regression(years_for_regression) == approx(expected_output)
