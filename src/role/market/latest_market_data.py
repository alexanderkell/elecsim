import logging
from src.data_manipulation.data_modifications.linear_regression import linear_regression
from src.plants.fuel.fuel_registry.fuel_registry import plant_type_to_fuel, fuel_registry
from src.plants.plant_costs.estimate_costs.estimate_costs import create_power_plant


import src.scenario.scenario_data as scenario
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

    def agent_forecast_value(self, value_required, years_to_look_back):
        years_for_regression = list(range(self.model.step_number-years_to_look_back-1, self.model.step_number-1))
        value_data = self._get_value_data(value_required)
        regression = self._get_yearly_demand_change_for_regression(value_data, years_for_regression)

        logger.debug(regression)

        next_value = linear_regression(regression, years_to_look_back)
        return next_value


    def get_estimated_marginal_cost(self, plant_type, capacity, look_back_years):

        fuel_type= plant_type_to_fuel(plant_type=plant_type)
        fuel = fuel_registry(fuel_type)

        co2_price = self.agent_forecast_value("co2", look_back_years)
        fuel_price = self.agent_forecast_value(fuel_type, look_back_years)
        demand_level = self.agent_forecast_value("demand", look_back_years)

        logger.debug("predicted co2: {}, fuel price: {}, demand: {}".format(co2_price, fuel_price, demand_level))

        # Get variable cost
        power_plant = create_power_plant("estimate_variable", self.model.year_number, plant_type, capacity)
        variable_o_m_cost = power_plant.variable_o_and_m_per_mwh

        co2_cost = fuel.mwh_to_co2e_conversion_factor * (1 / power_plant.efficiency) * co2_price
        fuel_cost = fuel_price/power_plant.efficiency

        short_run_marginal_cost = variable_o_m_cost + co2_cost + fuel_cost

        return short_run_marginal_cost





    def _get_yearly_demand_change_for_regression(self, value_required, years_for_regression):
        regression = [value_required[i] if i > 0 else value_required[0] for i in years_for_regression]
        return regression


    @staticmethod
    def _get_value_data(values_required):
        try:
            values_required = values_required.lower()
        except:
            raise ValueError("Price required must be a string, not a {}".format(type(values_required)))
        if values_required == "coal":
            return scenario.coal_price
        elif values_required == "gas":
            return scenario.gas_price
        elif values_required == "uranium":
            return scenario.uranium_price
        elif values_required == "co2":
            return scenario.carbon_price_scenario
        elif values_required == "demand":
            return scenario.yearly_demand_change
        else:
            raise ValueError("Could not find {}".format(values_required))



