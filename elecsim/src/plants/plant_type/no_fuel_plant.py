""" no_fuel_plant.py: Child class of power plant which contains functions for a power plant that does not require fuel"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"

from elecsim.src.plants.power_plant import PowerPlant


class NoFuelPlant(PowerPlant):

    def __init__(self, name, plant_type, capacity_mw, average_load_factor, pre_dev_period, construction_period, operating_period, pre_dev_spend_years, construction_spend_years, pre_dev_cost_per_kw, construction_cost_per_kw, infrastructure, fixed_o_and_m_per_mw, variable_o_and_m_per_mwh, insurance_cost_per_kw, connection_cost_per_kw, min_running, efficiency):
        """
        Power plant of type that does not use plant_type.
        """
        super().__init__(name, plant_type, capacity_mw, average_load_factor, pre_dev_period, construction_period, operating_period, pre_dev_spend_years, construction_spend_years, pre_dev_cost_per_kw, construction_cost_per_kw, infrastructure, fixed_o_and_m_per_mw, variable_o_and_m_per_mwh, insurance_cost_per_kw, connection_cost_per_kw, min_running)

        self.efficiency = efficiency

    def calculate_lcoe(self, carbon_price):
        """
        Function which calculates the levelised cost of electricity for this power plant instance
        :return: Returns LCOE value for power plant
        """

        # Calculations to convert into total costs for this power plant instance

        capex = self.capex()
        opex = self.opex()
        elec_gen = self.electricity_generated()

        print(capex)
        print(opex)


