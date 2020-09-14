from itertools import zip_longest

from elecsim.role.plants.costs.plant_cost_calculation import PlantCostCalculations

"""
File name: non_fuel_lcoe_calculation
Date created: 18/12/2018
Feature: # Calculates the costs of non fuel plants such as LCOE and marginal cost.
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"

class NonFuelCostCalculation(PlantCostCalculations):

    def __init__(self, construction_year, capacity_mw, average_load_factor, pre_dev_period, construction_period, operating_period, pre_dev_spend_years, construction_spend_years, pre_dev_cost_per_mw, construction_cost_per_mw, infrastructure, fixed_o_and_m_per_mw, variable_o_and_m_per_mwh, insurance_cost_per_mw, connection_cost_per_mw, efficiency):
        """
        Power plant of plant_type that does not use plant_type.
        """
        super().__init__(capacity_mw, construction_year, average_load_factor, pre_dev_period, construction_period, operating_period, pre_dev_spend_years, construction_spend_years, pre_dev_cost_per_mw, construction_cost_per_mw, infrastructure, fixed_o_and_m_per_mw, variable_o_and_m_per_mwh, insurance_cost_per_mw, connection_cost_per_mw)


    def calculate_lcoe(self, discount_rate):
        """
        Function which calculates the levelised cost of electricity for this power plant instance
        :return: Returns LCOE value for power plant
        """

        # Calculations to convert into total costs for this power plant instance

        elec_gen, total_costs = self.calculate_total_costs()

        # Discount data
        discounted_total_costs = self._discount_data(total_costs, discount_rate)
        discounted_electricity_generated = self._discount_data(elec_gen, discount_rate)

        # Sum total costs over life time of plant
        discounted_costs_sum = sum(discounted_total_costs)
        discounted_electricity_sum = sum(discounted_electricity_generated)

        lcoe = discounted_costs_sum/discounted_electricity_sum
        return lcoe

    def calculate_total_costs(self):
        capex = self._capex()
        opex = self._opex_cost()
        elec_gen = self._electricity_generated()
        total_costs = self._total_costs(capex, opex)
        return elec_gen, total_costs

    def calculate_short_run_marginal_cost(self, model):
        return self.variable_o_and_m_per_mwh


    def _total_costs(self, capex, opex):
        """
        Calculates total costs of plant by adding capital expenses plus operating expenses.
        :return: Total costs over lifetime of plant
        """

        total_costs = [x + y for x, y in zip_longest(capex, opex, fillvalue=0)]
        return total_costs


