import logging
from src.data_manipulation.data_modifications.linear_regression import linear_regression

import scenario.scenario_data as scenario
logger = logging.getLogger(__name__)

"""
File name: current_market_data
Date created: 29/12/2018
Feature: # Data which collates market information for generator companies when making decisions about investments.
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"


class LatestMarketData:

    def __init__(self, model):
        self.model = model
        self.demand = self.model.demand

    def agent_forecast_demand(self, years_to_look_back):
        years_for_regression = list(range(self.model.step_number-years_to_look_back-1, self.model.step_number-1))
        regression = self._get_yearly_demand_change_for_regression(years_for_regression)


        logger.debug(regression)

        next_value = linear_regression(regression, years_to_look_back)
        return next_value


    def _get_yearly_demand_change_for_regression(self, years_for_regression):
        regression = [self.demand.yearly_demand_change[i] if i > 0 else self.demand.yearly_demand_change[0] if
        i > len(self.demand.yearly_demand_change) else self.demand.yearly_demand_change[-1] for i in
                      years_for_regression]
        return regression


    def agent_forecast_fuel(self, years_to_look_back):
        pass

    @staticmethod
    def _switch_statements_for_price_data(price_requried):
        try:
            price_requried = price_requried.lower()
        except:
            raise ValueError("Price required must be a string, not a {}".format(type(price_requried)))
        if price_requried == "coal":
            return scenario.coal_price
        elif price_requried == "gas":
            return scenario.gas_price
        elif price_requried == "uranium":
            return scenario.uranium_price
        elif price_requried == "co2":
            return scenario.carbon_price_scenario
        else:
            raise ValueError("Could not find {}".format(price_requried))
