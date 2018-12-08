""" no_fuel_plant.py: Child class of power plant which contains functions for a power plant that does not require fuel"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"

from src.plants.plant_type.power_plant import PowerPlant
from itertools import zip_longest

class NonFuelPlant(PowerPlant):

    def __init__(self, name, plant_type, construction_year, capacity_mw, average_load_factor, pre_dev_period, construction_period, operating_period, pre_dev_spend_years, construction_spend_years, pre_dev_cost_per_mw, construction_cost_per_mw, infrastructure, fixed_o_and_m_per_mw, variable_o_and_m_per_mwh, insurance_cost_per_mw, connection_cost_per_mw, efficiency):
        """
        Power plant of type that does not use plant_type.
        """
        super().__init__(name, plant_type, capacity_mw, construction_year, average_load_factor, pre_dev_period, construction_period, operating_period, pre_dev_spend_years, construction_spend_years, pre_dev_cost_per_mw, construction_cost_per_mw, infrastructure, fixed_o_and_m_per_mw, variable_o_and_m_per_mwh, insurance_cost_per_mw, connection_cost_per_mw)

        self.efficiency = efficiency

    def calculate_lcoe(self, discount_rate):
        """
        Function which calculates the levelised cost of electricity for this power plant instance
        :return: Returns LCOE value for power plant
        """

        # Calculations to convert into total costs for this power plant instance

        capex = self.capex()
        opex = self.opex()
        elec_gen = self.electricity_generated()

        total_costs = self.total_costs(capex, opex)

        # Discount data
        discounted_total_costs = self.discount_data(total_costs, discount_rate)
        discounted_electricity_generated = self.discount_data(elec_gen, discount_rate)

        # Sum total costs over life time of plant
        discounted_costs_sum = sum(discounted_total_costs)
        discounted_electricity_sum = sum(discounted_electricity_generated)

        lcoe = discounted_costs_sum/discounted_electricity_sum
        return lcoe

    def total_costs(self, capex, opex):
        """
        Calculates total costs of plant by adding capital expenses plus operating expenses.
        :return: Total costs over lifetime of plant
        """

        total_costs = [x + y for x, y in zip_longest(capex, opex, fillvalue=0)]
        # capex.extend(opex)
        return total_costs
