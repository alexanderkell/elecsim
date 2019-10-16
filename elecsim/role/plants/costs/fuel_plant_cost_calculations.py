import logging
from itertools import zip_longest
from math import isnan
from functools import lru_cache

import pandas as pd
import numpy as np
import elecsim.scenario.scenario_data
from elecsim.constants import ROOT_DIR
from elecsim.data_manipulation.data_modifications.extrapolation_interpolate import ExtrapolateInterpolate
from elecsim.plants.fuel.fuel_registry.fuel_registry import fuel_registry, plant_type_to_fuel
from elecsim.role.plants.costs.plant_cost_calculation import PlantCostCalculations

logger = logging.getLogger(__name__)

"""
File name: fuel_lcoe_calculation
Date created: 18/12/2018
Feature: #Enter feature description here
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"


class FuelPlantCostCalculations(PlantCostCalculations):
    def __init__(self, plant_type, capacity_mw, construction_year, average_load_factor, efficiency, pre_dev_period,
                 construction_period, operating_period, pre_dev_spend_years, construction_spend_years,
                 pre_dev_cost_per_mw, construction_cost_per_mw, infrastructure, fixed_o_and_m_per_mw,
                 variable_o_and_m_per_mwh, insurance_cost_per_mw, connection_cost_per_mw):
        super().__init__(capacity_mw=capacity_mw, construction_year=construction_year,
                         average_load_factor=average_load_factor, pre_dev_period=pre_dev_period,
                         construction_period=construction_period, operating_period=operating_period,
                         pre_dev_spend_years=pre_dev_spend_years, construction_spend_years=construction_spend_years,
                         pre_dev_cost_per_mw=pre_dev_cost_per_mw, construction_cost_per_mw=construction_cost_per_mw,
                         infrastructure=infrastructure, fixed_o_and_m_per_mw=fixed_o_and_m_per_mw,
                         variable_o_and_m_per_mwh=variable_o_and_m_per_mwh, insurance_cost_per_mw=insurance_cost_per_mw,
                         connection_cost_per_mw=connection_cost_per_mw)
        self.plant_type = plant_type
        self.efficiency = efficiency
        # Finds fuel plant_type of power plant eg. CCGT power plant plant_type returns gas.
        fuel_string = plant_type_to_fuel(plant_type, self.construction_year)
        # Fuel object, containing information on fuel.
        self.fuel = fuel_registry(fuel_string)
        self.fuel_string = fuel_string

    def calculate_lcoe(self, discount_rate):
        """
        Function which calculates the levelised cost of electricity for this power plant instance at a
        specified discount rate.

        :param discount_rate: The discount rate that is used for the calculation of the levelised cost of electricity.
        :return: Returns LCOE value for power plant
        """

        # Calculations of capital expenditure, operating expenditure, total expected electricity expenditure and plant_type cost
        # This is used to estimate a LCOE price.
        elec_gen, total_costs = self.calculate_total_costs()
        # Costs discounted using discount_rate variable.
        disc_costs = self._discount_data(total_costs, discount_rate)
        disc_elec = self._discount_data(elec_gen, discount_rate)

        # Sum total costs over life time of plant
        disc_total_costs = sum(disc_costs)
        disc_total_elec = sum(disc_elec)

        # LCOE calculated
        lcoe = disc_total_costs / disc_total_elec

        return lcoe

    def calculate_total_costs(self, estimated_fuel_prices=None, estimated_carbon_prices=None):
        capex = self._capex()
        opex = self._opex_cost()
        elec_gen = self._electricity_generated()
        fuel_costs = self._fuel_costs(elec_gen)
        carbon_costs = self._carbon_costs()
        total_costs = self._total_costs(capex, opex, fuel_costs, carbon_costs)

        return elec_gen, total_costs

    def _total_costs(self, capex, opex, fuel_costs, carbon_costs):
        """
        Function which uses addition to calculate total costs from capital expenditure, operating expenditure, fuel costs,
        and carbon costs for plant_type costs over the lifetime of the power plant.

        :param capex: Capital expenditure per year
        :param opex: Operating expenditure per year
        :param fuel_costs: _fuel_costs per year
        :return: Total costs over lifetime of power plant
        """

        # Addition of operating expenditure and plant_type costs, followed by operating expenditure, plant_type costs and capital expenditure.
        opex_fuel = [sum(x) for x in zip_longest(opex, fuel_costs, fillvalue=0)]

        opex_fuel_remove_0 = opex_fuel[int(self.construction_period + self.pre_dev_period):]
        capex.extend(opex_fuel_remove_0)
        sum_of_opex_fuel_capex = capex.copy()
        sum_of_carbon_opex_fuel_capex = [sum(x) for x in zip(sum_of_opex_fuel_capex, carbon_costs)]

        return sum_of_carbon_opex_fuel_capex

    def _fuel_costs(self, electricity_generated, fuel_price=None):
        """
        Calculates the plant_type costs per year based on plant efficiency, electricity generated and endogenous gas prices
        :param electricity_generated: Electricity generated per year
        :return: Returns estimated cost of plant_type per year
        """
        beginning_year_operation = self.construction_year
        end_of_lifetime_year = int(beginning_year_operation) + int(self.operating_period) + int(
            self.pre_dev_period + self.construction_period)
        years_of_plant_operation = range(int(beginning_year_operation), end_of_lifetime_year)

        if fuel_price is None:
            this_fuel_price = self.fuel.fuel_price[self.fuel.fuel_price.Fuel == self.fuel.fuel_type].dropna()
        else:
            this_fuel_price = fuel_price

        fuel_extrapolation = ExtrapolateInterpolate(this_fuel_price.Year, this_fuel_price.value)
        fuel_price = [(float(fuel_extrapolation(i)) * elec_gen) / self.efficiency for i, elec_gen in
                      zip(years_of_plant_operation, electricity_generated)]

        return fuel_price

    def _carbon_emitted(self):
        """
        Calculates projected tonnes of CO2 emitted by power plant per year
        :return: A list containing tonnes of CO2 emitted per year
        """
        carbon_emitted = [self.fuel.mwh_to_co2e_conversion_factor * (elec_gen / self.efficiency) for elec_gen in
                          self._electricity_generated()]
        return carbon_emitted

    def _carbon_costs(self, carbon_price=None):
        """
        Costs of carbon emissions based on carbon tax
        :return: Projected carbon costs per year in a list.
        """

        # if carbon_price is not None:
        #     carbon_taxation_years = carbon_price
        # else:
        #     carbon_cost = self.get_BEIS_carbon_price()

        carbon_cost = elecsim.scenario.scenario_data.carbon_price_all_years

        year_of_beginning_operation = self.construction_year + self.pre_dev_period + self.construction_period
        carbon_taxation_years = carbon_cost[carbon_cost.year.between(int(self.construction_year), int(
                year_of_beginning_operation + self.operating_period - 1))]

        carbon_emitted = self._carbon_emitted()

        carbon_costs = [carbon_tax * carb_emit for carbon_tax, carb_emit in
                        zip(list(carbon_taxation_years.price), carbon_emitted)]

        return carbon_costs



    def _carbon_cost_total(self, carbon_costs):
        """
        Calculates the total cost of carbon over the lifetime of the power plant.
        :return: total carbon costs
        """
        carbon_costs_total = sum(carbon_costs)

        return carbon_costs_total

    def calculate_short_run_marginal_cost(self, model, genco, fuel_price=None, co2_price=None):
        """
        Calculates the short run marginal cost for a fuel power plant
        :param model: Model containing information such as current year
        :param genco: Generation company object that requires short run marginal cost. Used to use genco price of fuel.
        :return: returns marginal cost to burn 1MWh of fuel.
        """

        modifier = 0
        if self.plant_type == 'CCGT':
            modifier = genco.gas_price_modifier
        elif self.plant_type == 'Coal':
            modifier = genco.coal_price_modifier

        fuel_cost = self.get_fuel_price(fuel_price, model.year_number, modifier)
        co2_cost = self.get_co2_price(co2_price, model)
        marginal_cost = self.variable_o_and_m_per_mwh + fuel_cost + co2_cost
        if isnan(marginal_cost):
            logger.debug("Marginal cost is nan. Variable cost: {}, Fuel cost: {}, CO2 Cost: {}, plant type: {}".format(
                self.variable_o_and_m_per_mwh, fuel_cost, co2_cost, self.plant_type))
            raise ValueError("Marginal cost is nan. Variable cost: {}, Fuel cost: {}, CO2 Cost: {}, plant type: {}".format(
                self.variable_o_and_m_per_mwh, fuel_cost, co2_cost, self.plant_type))

        return marginal_cost

    def get_co2_price(self, co2_price, model):
        if co2_price is None:
            # co2_cost = self.fuel.mwh_to_co2e_conversion_factor * (1 / self.efficiency) * \
            #            carbon_cost[carbon_cost.year == model.year_number - 1].price.iloc[0]

            co2_cost = self.fuel.mwh_to_co2e_conversion_factor * (1 / self.efficiency) * get_carbon_cost_in_year(
                model.year_number)
        else:
            co2_cost = self.fuel.mwh_to_co2e_conversion_factor * (1 / self.efficiency) * co2_price
        return co2_cost

    def get_fuel_price(self, fuel_price, year_number, modifier):
        if fuel_price is None:
            # logger.debug("fuel_price_is_none calculating from data")
            # fuel_cost = (self.fuel.fuel_price[self.fuel.fuel_price.Year == model.year_number - 1].value.iloc[
            #                  0] + modifier) / self.efficiency


            # fuel_price = self.fuel.fuel_price[self.fuel.fuel_price.Year == model.year_number - 1].value.iloc[0] + modifier
            fuel_price = _query_fuel_price_for_year(self.fuel_string, year_number) + modifier
            logger.debug("_query_fuel_price_for_year: {}".format(_query_fuel_price_for_year.cache_info()))

            fuel_cost = fuel_price / self.efficiency
        else:
            # logger.debug("fuel_price_is_given calculating from parenthesis")
            fuel_cost = fuel_price / self.efficiency
        return fuel_cost

    def get_BEIS_carbon_price(self):
        carbon_price_scenario = [18.00, 19.42, 20.83, 22.25, 23.67, 25.08, 26.50, 27.92, 29.33, 30.75, 32.17, 33.58,
                                 35.00, 43.25, 51.50, 59.75, 68.00, 76.25, 84.50, 92.75, 101.00, 109.25, 117.50,
                                 125.75, 134.00, 142.25, 150.50, 158.75, 167.00, 175.25, 183.50, 191.75,
                                 200.00]  # Forecast used from BEIS Electricity Generation Report - Page 10 - Includes forecast for carbon tax and EU ETS
        carbon_data = {'year': [str(i) for i in range(2019, (2019 + len(carbon_price_scenario)))],
                       'price': carbon_price_scenario}
        carbon_price_scenario_df = pd.DataFrame(carbon_data)
        historical_carbon_price = pd.read_csv(
            ROOT_DIR + '/data/processed/carbon_price/uk_carbon_tax_historical.csv')
        carbon_cost = historical_carbon_price.append(carbon_price_scenario_df, sort=True)
        carbon_cost.year = pd.to_numeric(carbon_cost.year)
        return carbon_cost


# lru_cache(maxsize=128)
def calculate_year_carbon_price():
    # carbon_price_scenario = elecsim.scenario.scenario_data.carbon_price_scenario
    # # logger.debug("Calculating short_run_marginal_cost")
    # # Join historical and future carbon prices into dataframe for simulation purposes
    # carbon_data = {'year': [str(i) for i in range(2019, (2019 + len(carbon_price_scenario)))],
    #                 'price': carbon_price_scenario}
    # carbon_price_scenario_df = pd.DataFrame(carbon_data)
    # historical_carbon_price = pd.read_csv(ROOT_DIR + '/data/processed/carbon_price/uk_carbon_tax_historical.csv')
    # carbon_cost = historical_carbon_price.append(carbon_price_scenario_df, sort=True)
    # carbon_cost.year = pd.to_numeric(carbon_cost.year)
    carbon_cost = elecsim.scenario.scenario_data.carbon_price_all_years
    return carbon_cost


@lru_cache(maxsize=1000)
def get_carbon_cost_in_year(year_number):
    # carbon_cost = carbon_cost[carbon_cost.year == year_number - 1].price.iloc[0]
    carbon_cost = elecsim.scenario.scenario_data.carbon_price_all_years

    carbon_cost = carbon_cost.loc[np.in1d(carbon_cost['year'], [year_number]), 'price'].iloc[0]
    return carbon_cost

@lru_cache(1024)
def _query_fuel_price_for_year(fuel_string, year_number):
    fuel = fuel_registry(fuel_string)
    fuel_price = fuel.fuel_price.loc[np.in1d(fuel.fuel_price['Year'], [year_number]), 'value'].iloc[0]
    return fuel_price
