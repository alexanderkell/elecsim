import logging
from unittest.mock import Mock

import pytest
from pytest import approx

from elecsim.constants import KW_TO_MW
from elecsim.plants.plant_costs.estimate_costs.estimate_costs import create_power_plant
from elecsim.role.market.latest_market_data import LatestMarketData

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
        model = Mock()
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
        value_data = market_data._get_variable_data(value_required)
        assert market_data._get_yearly_change_for_regression(value_data, years_for_regression) == approx(expected_output)


    @pytest.mark.parametrize("value_required, expected_output",
                            [
                                ("GAS", [KW_TO_MW * 0.018977] * 60),
                                ("gas", [KW_TO_MW * 0.018977] * 60),
                                ("coal", [KW_TO_MW * 0.00906] * 60),
                                ("uranium", [KW_TO_MW * 0.0039] * 60),
                                ("co2", [18.00, 19.42, 20.83, 22.25, 23.67, 25.08, 26.50, 27.92, 29.33, 30.75, 32.17, 33.58, 35.00, 43.25, 51.50, 59.75, 68.00, 76.25, 84.50, 92.75, 101.00, 109.25, 117.50, 125.75, 134.00, 142.25, 150.50, 158.75, 167.00, 175.25, 183.50, 191.75, 200.00])
                            ])
    def test_switch_statements_for_value_data(self, latest_market_data, value_required, expected_output):
        assert latest_market_data._get_variable_data(value_required) == expected_output

    def test_switch_statements_for_valueerror_for_value_data(self, latest_market_data):
        with pytest.raises(ValueError):
            assert latest_market_data._get_variable_data("sdfsf")
        with pytest.raises(ValueError):
            assert latest_market_data._get_variable_data(-1)

    @pytest.mark.parametrize("plant_type, capacity, look_back_years, expected_output",
                             [
                                 ("CCGT", 1200, 5, 46.011651),
                                 ("Coal", 624, 5, 53.77050275),
                                 ('Onshore', 20, 5, 5),
                                 ('Offshore', 844, 5, 4),
                                 ('Offshore', 321, 5, 3),
                                 ('PV', 4, 5, 0),
                                 ('PV', 1, 5, 3),
                                 ('PV', 1, 5, 3),
                                 ('Nuclear', 3300, 5, 8.9),
                             ])
    def test_get_predicted_marginal_cost(self, plant_type, capacity, look_back_years, expected_output):
        model = Mock()
        model.step_number = 5
        model.year_number = 2018

        power_plant = create_power_plant("estimate_variable", model.year_number, plant_type, capacity)


        latest_market_data = LatestMarketData(model)
        assert latest_market_data.get_predicted_marginal_cost(power_plant, look_back_years) == approx(expected_output)
