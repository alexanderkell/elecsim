from logging import getLogger
import pandas as pd
from inspect import signature

from src.plants.fuel.capacity_factor.capacity_factor_calculations import get_capacity_factor
from src.scenario.scenario_data import modern_plant_costs
from src.role.plants.costs.fuel_plant_cost_calculations import FuelPlantCostCalculations
from src.role.investment.expected_load_duration_prices import LoadDurationPrices
from src.role.market.latest_market_data import LatestMarketData
from src.plants.plant_costs.estimate_costs.estimate_costs import create_power_plant
from src.plants.plant_type.fuel_plant import FuelPlant

logger = getLogger(__name__)

"""
File name: calculate_npv
Date created: 04/01/2019
Feature: # Contains functionality to assess options of investment and return lowest NPV for decision to be made.
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"


class CalculateNPV:

    def __init__(self, model, discount_rate, look_back_years):
        self.model = model
        self.discount_rate = discount_rate
        self.look_back_years = look_back_years

    def compare_npv(self):
        cost_list = []
        for plant_type in ['CCGT','Coal','Nuclear','Onshore', 'Offshore', 'PV']:
            plant_cost_data = modern_plant_costs[modern_plant_costs.Type==plant_type]
            for plant_row in plant_cost_data.itertuples():
                npv = self.calculate_npv(plant_row.Type, plant_row.Plant_Size)
                dict = {"npv_per_mwh":npv, "capacity":plant_row.Plant_Size, "plant_type":plant_row.Type}
                cost_list.append(dict)

        npv_results = pd.DataFrame(cost_list)

        sorted_npv = npv_results.sort_values(by='npv', ascending=False)
        logger.debug("sorted_npv: \n {}".format(sorted_npv))
        return sorted_npv

    def calculate_npv(self, plant_type, plant_size):
        # Forecast segment prices
        forecasted_segment_prices = self._get_load_duration_price_predictions()

        logger.debug("Load duration prices: {}".format(forecasted_segment_prices))

        power_plant = create_power_plant("estimate_variable", self.model.year_number, plant_type, plant_size)

        # Forecast marginal costs
        short_run_marginal_cost = self._get_predicted_marginal_cost(power_plant)
        logger.debug("short run marginal cost: {}".format(short_run_marginal_cost))

        forecasted_segment_prices = self._clean_segment_prices(forecasted_segment_prices)
        logger.debug("forecasted_segment_prices: \n {}".format(forecasted_segment_prices))

        self._get_profit_per_mwh(forecasted_segment_prices, short_run_marginal_cost)

        self._get_profit_per_segment(forecasted_segment_prices, power_plant=power_plant)

        self._get_total_hours_to_run(forecasted_segment_prices, power_plant)

        self._get_total_yearly_income(forecasted_segment_prices, power_plant)

        logger.debug("total_hours_predicted_to_run: \n {}".format(forecasted_segment_prices))

        # total_profit_for_year = sum(forecasted_segment_prices['_total_profit_per_segment'])
        total_running_hours = sum(forecasted_segment_prices['_total_running_hours'])
        total_yearly_income = sum(forecasted_segment_prices['total_income'])

        yearly_capital_cost = self._get_yearly_capital_cost(power_plant)

        yearly_cash_flow = self._calculate_yearly_cash_flow(power_plant, short_run_marginal_cost, total_running_hours,
                                                  total_yearly_income, yearly_capital_cost)



        yearly_cash_flow_per_mwh = yearly_cash_flow/(total_running_hours*power_plant.capacity_mw)
        # yearly_cash_flow_per_mwh = yearly_cash_flow/(power_plant.capacity_mw)

        return yearly_cash_flow_per_mwh

    def _calculate_yearly_cash_flow(self, power_plant, short_run_marginal_cost, total_running_hours, total_yearly_income,
                                    yearly_capital_cost):
        # logger.debug("total_profit_for_year: {}, total running hours: {}".format(total_profit_for_year, _total_running_hours))
        total_costs = yearly_capital_cost + short_run_marginal_cost * total_running_hours * power_plant.capacity_mw
        # logger.debug("yearly_capital_cost: {}".format(yearly_capital_cost))
        # logger.debug("total yearly cost: {}, total yearly _income: {}".format(total_costs, total_yearly_income))
        result = total_yearly_income - total_costs
        logger.debug("result: {}".format(result))
        return result

    def _get_yearly_capital_cost(self, power_plant):
        power_plant_vars = vars(power_plant)
        logger.debug("power_plant_vars: {}".format(power_plant_vars))
        func = FuelPlantCostCalculations
        vars_required = signature(func)._parameters
        logger.debug("vars_required: {}".format(vars_required))
        power_plant_vars = {key: value for key, value in power_plant_vars.items() if key in vars_required}
        yearly_capital_cost = FuelPlantCostCalculations(**power_plant_vars).calculate_yearly_capital_costs()
        return yearly_capital_cost

    def _get_total_yearly_income(self, forecasted_segment_prices, power_plant):
        forecasted_segment_prices['total_income'] = forecasted_segment_prices.apply(
            lambda x: self._income(x, power_plant.capacity_mw), axis=1)

    def _get_total_hours_to_run(self, forecasted_segment_prices, power_plant):
        forecasted_segment_prices['_total_running_hours'] = forecasted_segment_prices.apply(
            lambda x: self._total_running_hours(x, power_plant), axis=1)

    def _get_profit_per_segment(self, forecasted_segment_prices, power_plant):
        forecasted_segment_prices['_total_profit_per_segment'] = forecasted_segment_prices.apply(
            lambda x: self._total_profit_per_segment(x, power_plant.capacity_mw), axis=1)

    def _get_profit_per_mwh(self, forecasted_segment_prices, short_run_marginal_cost):
        forecasted_segment_prices['predicted_profit_per_mwh'] = forecasted_segment_prices[
                                                                    'accepted_price'] - short_run_marginal_cost

    def _clean_segment_prices(self, forecasted_segment_prices):
        forecasted_segment_prices = forecasted_segment_prices.to_frame().reset_index()
        forecasted_segment_prices['num_of_hours'] = abs(forecasted_segment_prices.segment_hour.diff())
        forecasted_segment_prices = forecasted_segment_prices.dropna()
        return forecasted_segment_prices

    def _get_predicted_marginal_cost(self, power_plant):
        market_data = LatestMarketData(model=self.model)
        short_run_marginal_cost = market_data.get_predicted_marginal_cost(power_plant, self.look_back_years)
        return short_run_marginal_cost

    def _get_load_duration_price_predictions(self):
        load_duration_prices = LoadDurationPrices(model=self.model)
        forecasted_segment_prices = load_duration_prices.get_load_curve_price_predictions(
            reference_year=self.model.year_number + 1, look_back_years=self.look_back_years)
        return forecasted_segment_prices

    @staticmethod
    def _total_profit_per_segment(row, capacity):
        if row['predicted_profit_per_mwh'] > 0:
            total_profit = row['num_of_hours']*row['predicted_profit_per_mwh']*capacity
        else:
            total_profit = 0
        return total_profit

    @staticmethod
    def _total_running_hours(row, power_plant):
        if isinstance(power_plant, FuelPlant):
            if row['predicted_profit_per_mwh'] > 0:
                running_hours = row['num_of_hours']
            else:
                running_hours = 0
        else:
            if row['predicted_profit_per_mwh'] > 0:
                capacity_factor = get_capacity_factor(power_plant.plant_type, row.segment_hour)
                logger.debug("Capacity factor for {} of segment hour {} is {}".format(power_plant.plant_type, row.segment_hour, capacity_factor))
                running_hours = capacity_factor*row['num_of_hours']
            else:
                running_hours = 0
        return running_hours

    @staticmethod
    def _income(row, capacity):
        if row['predicted_profit_per_mwh'] > 0:
            running_hours = row['_total_running_hours']*row['accepted_price']*capacity
        else:
            running_hours = 0
        return running_hours
