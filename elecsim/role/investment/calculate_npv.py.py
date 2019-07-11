from functools import lru_cache
from inspect import signature
from itertools import zip_longest
from logging import getLogger

import pandas as pd
from numpy import npv, pmt, divide

import numpy as np
np.seterr(divide='ignore', invalid='ignore')

from elecsim.plants.fuel.capacity_factor.capacity_factor_calculations import get_capacity_factor
from elecsim.plants.plant_costs.estimate_costs.estimate_costs import create_power_plant
from elecsim.plants.plant_type.fuel_plant import FuelPlant
from elecsim.role.investment.predict_load_duration_prices import get_price_duration_curve
from elecsim.role.market.latest_market_data import LatestMarketData
from elecsim.role.plants.costs.fuel_plant_cost_calculations import FuelPlantCostCalculations
# from elecsim.scen_error.scenario_data import modern_plant_costs
# from elecsim.scen_error.scenario_data import nuclear_wacc, non_nuclear_wacc
import elecsim.scenario.scenario_data
from functools import lru_cache

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
    def __init__(self, model, difference_in_discount_rate, look_back_years):
        self.model = model
        self.difference_in_discount_rate = difference_in_discount_rate
        self.look_back_years = look_back_years

    def get_positive_npv_plants_list(self):
        npv_rows = self.get_positive_npv_plants()
        logger.debug("npv_rows: {}".format(npv_rows))
        result = [(individual_plant_data.capacity, individual_plant_data.plant_type) for individual_plant_data in
                  npv_rows.itertuples()]
        return result

    def get_positive_npv_plants(self):
        npv_data = self.compare_npv()
        logger.debug("predicted npv data: \n {}".format(npv_data))

        npv_positive = npv_data[npv_data.npv_per_mw > 0]
        return npv_positive

<<<<<<< HEAD
    def compare_npv(self):
=======
    def  compare_npv(self):
>>>>>>> 5f3c373861c398621fed06ebb3fe989ceb1733a9
        cost_list = []

        for plant_type in ['CCGT', 'Coal', 'Nuclear', 'Onshore', 'Offshore', 'PV', 'Recip_gas', 'Recip_diesel']:
            plant_cost_data = elecsim.scenario.scenario_data.modern_plant_costs[(elecsim.scenario.scenario_data.modern_plant_costs.Type == plant_type) & (elecsim.scenario.scenario_data.modern_plant_costs.Plant_Size>5)]
            for plant_row in plant_cost_data.itertuples():

                npv = self.calculate_npv(plant_row.Type, plant_row.Plant_Size)
                dict = {"npv_per_mw": npv, "capacity": plant_row.Plant_Size, "plant_type": plant_row.Type}
                cost_list.append(dict)

        npv_results = pd.DataFrame(cost_list)

        sorted_npv = npv_results.sort_values(by='npv_per_mw', ascending=False)
        logger.debug("sorted_npv: \n {}".format(sorted_npv))
        return sorted_npv

    # @lru_cache(maxsize=10000)
    def calculate_npv(self, plant_type, plant_size):
        # Forecast segment prices

<<<<<<< HEAD
=======

>>>>>>> 5f3c373861c398621fed06ebb3fe989ceb1733a9
        forecasted_segment_prices = self._get_price_duration_predictions()
        # logger.info("Forecasted price duration curve: {}".format(forecasted_segment_prices))

        power_plant = create_power_plant("PowerPlantName", self.model.year_number, plant_type, plant_size)

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
        logger.debug("total_yearly_income: {}".format(total_yearly_income))
        yearly_capital_cost = self._get_capital_outflow(power_plant)

        logger.debug("yearly_capital_cost: {}".format(yearly_capital_cost))

        yearly_operating_cash_flow = self._calculate_yearly_operation_cashflow(power_plant, short_run_marginal_cost,
                                                                               total_running_hours,
                                                                               total_yearly_income, yearly_capital_cost)

        total_cash_flow = yearly_capital_cost + yearly_operating_cash_flow

        logger.debug('total_cash_flow: {}'.format(total_cash_flow))

        if power_plant.plant_type == "Nuclear":
            self.weighted_average_cost_capital = elecsim.scenario.scenario_data.nuclear_wacc + self.difference_in_discount_rate
        else:
            self.weighted_average_cost_capital = elecsim.scenario.scenario_data.non_nuclear_wacc + self.difference_in_discount_rate

        # logger.debug("cash_flow_wacc: {}".format(cash_flow_wacc))
        logger.debug("discount rate: {}".format(self.weighted_average_cost_capital))

        npv_power_plant = npv(self.weighted_average_cost_capital, total_cash_flow)

        logger.debug("npv_power_plant: {}".format(npv_power_plant))

        NPVp = divide(npv_power_plant, (power_plant.capacity_mw * total_running_hours))
        return NPVp

    def _get_yearly_profit_per_mwh(self, power_plant, total_running_hours, yearly_cash_flow):
        yearly_cash_flow_per_mwh = yearly_cash_flow / (total_running_hours * power_plant.capacity_mw)
        return yearly_cash_flow_per_mwh

    def _calculate_yearly_operation_cashflow(self, power_plant, short_run_marginal_cost, total_running_hours,
                                             total_yearly_income,
                                             yearly_capital_cost):
        # logger.debug("total_profit_for_year: {}, total running hours: {}".format(total_profit_for_year, _total_running_hours))
        operational_costs = short_run_marginal_cost * total_running_hours * power_plant.capacity_mw
        # logger.debug("yearly_capital_cost: {}".format(yearly_capital_cost))
        # logger.debug("total yearly cost: {}, total yearly _income: {}".format(operational_costs, total_yearly_income))
        result = [total_yearly_income - operational_costs] * int(power_plant.operating_period)
        return result

    def _get_capital_outflow(self, power_plant):
        power_plant_vars = vars(power_plant)
        logger.debug("power_plant_vars: {}".format(power_plant_vars))
        func = FuelPlantCostCalculations
        vars_required = signature(func)._parameters
        logger.debug("vars_required: {}".format(vars_required))
        power_plant_vars = {key: value for key, value in power_plant_vars.items() if key in vars_required}
        # yearly_outflow = FuelPlantCostCalculations(**power_plant_vars).calculate_yearly_outflow()

        capital_costs = FuelPlantCostCalculations(**power_plant_vars)._capex()
        logger.debug("capital_cost_outflow: {}".format(capital_costs))
        capital_costs_outflow = [-x for x in capital_costs]
        return capital_costs_outflow

    def _get_total_yearly_income(self, forecasted_segment_prices, power_plant):
        # forecasted_segment_prices['total_income'] = forecasted_segment_prices.apply(
        #     lambda x: self._income(x, power_plant.capacity_mw), axis=1)
        vectorized_income = np.vectorize(self._income)
        forecasted_segment_prices['total_income'] = vectorized_income(forecasted_segment_prices['predicted_profit_per_mwh'].values, forecasted_segment_prices['_total_running_hours'].values, forecasted_segment_prices['accepted_price'].values, power_plant.capacity_mw)


    def _get_total_hours_to_run(self, forecasted_segment_prices, power_plant):
        # forecasted_segment_prices['_total_running_hours'] = forecasted_segment_prices.apply(
        #     lambda x: self._total_running_hours(x, power_plant), axis=1)

        if isinstance(power_plant, FuelPlant):
            vectorized_total_running_hours_fuel_plant = np.vectorize(self._total_running_hours_fuel_plant)

            forecasted_segment_prices['_total_running_hours'] = vectorized_total_running_hours_fuel_plant(forecasted_segment_prices['predicted_profit_per_mwh'].values, forecasted_segment_prices['num_of_hours'].values)
        else:
            vectorized_total_running_hours_renewable_plant = np.vectorize(self._total_running_hours_renewable_plant)

            forecasted_segment_prices['_total_running_hours'] = vectorized_total_running_hours_renewable_plant(forecasted_segment_prices['predicted_profit_per_mwh'].values, forecasted_segment_prices['num_of_hours'].values, forecasted_segment_prices['segment_hour'].values, power_plant)



    def _get_profit_per_segment(self, forecasted_segment_prices, power_plant):
        # forecasted_segment_prices['_total_profit_per_segment'] = forecasted_segment_prices.apply(
        #     lambda x: self._total_profit_per_segment(x, power_plant.capacity_mw), axis=1)

        vectorized_total_profit_per_segment = np.vectorize(self._total_profit_per_segment)

        forecasted_segment_prices['_total_profit_per_segment'] = vectorized_total_profit_per_segment(forecasted_segment_prices['predicted_profit_per_mwh'].values, forecasted_segment_prices['num_of_hours'].values, power_plant.capacity_mw)

    def _get_profit_per_mwh(self, forecasted_segment_prices, short_run_marginal_cost):
        forecasted_segment_prices['predicted_profit_per_mwh'] = forecasted_segment_prices[
                                                                    'accepted_price'] - short_run_marginal_cost

    def _clean_segment_prices(self, forecasted_segment_prices):
        # forecasted_segment_prices = forecasted_segment_prices.to_frame().reset_index()
        forecasted_segment_prices = forecasted_segment_prices.reset_index()

        forecasted_segment_prices['num_of_hours'] = abs(forecasted_segment_prices.segment_hour.diff())
        forecasted_segment_prices = forecasted_segment_prices.dropna()
        return forecasted_segment_prices

    def _get_predicted_marginal_cost(self, power_plant):
        market_data = LatestMarketData(model=self.model)
        short_run_marginal_cost = market_data.get_predicted_marginal_cost(power_plant, self.look_back_years)
        return short_run_marginal_cost

    def _get_price_duration_predictions(self):
        predicted_price_duration_curve = get_price_duration_curve(self.model, self.look_back_years)

        return predicted_price_duration_curve

    # @staticmethod
    # def _total_profit_per_segment(row, capacity):
    #     if row['predicted_profit_per_mwh'] > 0:
    #         total_profit = row['num_of_hours'] * row['predicted_profit_per_mwh'] * capacity
    #     else:
    #         total_profit = 0
    #     return total_profit

    @staticmethod
    def _total_profit_per_segment(predicted_profit_per_mwh, num_of_hours, capacity):
        if predicted_profit_per_mwh > 0:
            return num_of_hours * predicted_profit_per_mwh * capacity
        else:
            return 0








    # def _total_running_hours(self, row, power_plant):
    #     if isinstance(power_plant, FuelPlant):
    #         if row['predicted_profit_per_mwh'] > 0:
    #             running_hours = row['num_of_hours']
    #         else:
    #             running_hours = 0
    #     else:
    #         if row['predicted_profit_per_mwh'] > 0:
    #             capacity_factor = get_capacity_factor(self.model.market_time_splices, power_plant.plant_type, row.segment_hour)
    #             running_hours = capacity_factor * row['num_of_hours']
    #         else:
    #             running_hours = 0
    #     return running_hours
    #

    def _total_running_hours_fuel_plant(self, predicted_profit_per_mwh, num_of_hours):

        if predicted_profit_per_mwh > 0:
            return num_of_hours
        else:
            return 0

    def _total_running_hours_renewable_plant(self, predicted_profit_per_mwh, num_of_hours, segment_hour, power_plant):
        if predicted_profit_per_mwh > 0:
            capacity_factor = get_capacity_factor(self.model.market_time_splices, power_plant.plant_type, segment_hour)
            return capacity_factor * num_of_hours
        else:
            return 0



    # @staticmethod
    # def _income(row, capacity):
    #     if row['predicted_profit_per_mwh'] > 0:
    #         running_hours = row['_total_running_hours'] * row['accepted_price'] * capacity
    #     else:
    #         running_hours = 0
    #     return running_hours

    @staticmethod
    def _income(predicted_profit_per_mwh, _total_running_hours, accepted_price, capacity):

        if predicted_profit_per_mwh > 0:
            return _total_running_hours * accepted_price * capacity
        else:
            return 0

        #
        # if row['predicted_profit_per_mwh'] > 0:
        #     running_hours = row['_total_running_hours'] * row['accepted_price'] * capacity
        # else:
        #     running_hours = 0
        # return running_hours


<<<<<<< HEAD
=======
# @lru_cache(maxsize=1024)
>>>>>>> 5f3c373861c398621fed06ebb3fe989ceb1733a9
def get_most_profitable_plants_by_npv(model, difference_in_discount_rate, look_back_period):
    npv_calculation = CalculateNPV(model, difference_in_discount_rate, look_back_period)

    potential_plant_data = npv_calculation.get_positive_npv_plants_list()

    return potential_plant_data


def get_yearly_payment(power_plant, interest_rate, down_payment_perc):
    loan_percentage = 1-down_payment_perc
    pre_dev_downpayments = [pre_dev_year * power_plant.pre_dev_cost_per_mw * power_plant.capacity_mw * loan_percentage for pre_dev_year in
                            power_plant.pre_dev_spend_years]

    pre_dev_years_to_pay_back = [
        12 * (power_plant.operating_period + power_plant.construction_period + downpayment_date) for
        downpayment_date in list(reversed(range(1, len(pre_dev_downpayments) + 1)))]

    # logger.debug("pre_dev_years_to_pay_back: {}".format(pre_dev_years_to_pay_back))

    pre_dev_interest = [interest_rate / 12] * int(power_plant.pre_dev_period)

    # logger.debug("pre_dev_interest: {}".format(pre_dev_interest))

    construction_downpayments = [construction_year * power_plant.construction_cost_per_mw * power_plant.capacity_mw * loan_percentage for
                                 construction_year in power_plant.construction_spend_years]

    construction_interest = [interest_rate / 12] * int(power_plant.construction_period)

    construction_years_to_pay_back = [12 * (power_plant.operating_period + downpayment_date) for
                                      downpayment_date in list(reversed(range(1, len(construction_downpayments) + 1)))]

    pre_dev_repayments = pmt(rate=pre_dev_interest, nper=pre_dev_years_to_pay_back, pv=pre_dev_downpayments, fv=0,
                             when=0)

    total_years_to_pay_pre_dev = [power_plant.operating_period + power_plant.construction_period + downpayment_date for
                          downpayment_date in list(reversed(range(1, len(pre_dev_downpayments) + 1)))]

    pre_dev_lumpsums = []
    for years_to_pay, pre_dev_downpayment in zip(total_years_to_pay_pre_dev, pre_dev_repayments):
        # logger.debug('years_to_pay: {}'.format(years_to_pay))
        pre_dev_payback = [pre_dev_downpayment] * int(years_to_pay)
        pre_dev_lumpsums.append(pre_dev_payback)

    # logger.debug("pre_dev_lumpsums: {}".format(pre_dev_lumpsums))
    # logger.debug("len of lumpsums: {}, len of lumpsums[0]: {}, len of lumpsums[1]: {}, len of lumpsums[2]: {}".format(len(pre_dev_lumpsums), len(pre_dev_lumpsums[0]),len(pre_dev_lumpsums[1]), len(pre_dev_lumpsums[2])))

    construction_repayments = pmt(rate=construction_interest, nper=construction_years_to_pay_back,
                                  pv=construction_downpayments, fv=0, when=0)

    construction_lumpsums = []
    total_years_to_pay_construction = [(power_plant.operating_period + downpayment_date) for downpayment_date in list(reversed(range(1, len(construction_downpayments) + 1)))]
    for years_to_pay, construction_downpayment in zip(total_years_to_pay_construction, construction_repayments):
        construction_payback = [construction_downpayment] * int(years_to_pay)
        construction_lumpsums.append(construction_payback)


    total_pre_dev_payments = [sum(i) for i in zip_longest(*reversed(pre_dev_lumpsums), fillvalue=0)][::-1]
    # logger.debug("total_pre_dev_payments:{}".format(total_pre_dev_payments))

    # Join construction and pre-dev payments together
    total_construction_payments = [sum(i) for i in zip_longest(*reversed(construction_lumpsums), fillvalue=0)][::-1]

    # Add construction payments and pre-development payments together
    total_payments = [a+b for a, b in zip_longest(reversed(total_pre_dev_payments), reversed(total_construction_payments), fillvalue=0)][::-1]

    # repayments = pre_dev_repayments + construction_repayments

    return total_payments


def select_yearly_payback_payment_for_year(power_plant, interest, downpayment_percentage, model):
    total_payments = get_yearly_payment(power_plant, interest, downpayment_percentage)
    years_since_construction = model.year_number-power_plant.construction_year
    if years_since_construction > power_plant.operating_period+power_plant.construction_period+power_plant.pre_dev_period:
        payment_in_current_year=0
    else:
        try:
            payment_in_current_year = total_payments[years_since_construction]
        except IndexError:
            payment_in_current_year=0
    return payment_in_current_year
