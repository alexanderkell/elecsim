""" fuel_plant.py: Child class of power plant which contains functions for a power plant which consumes fuel"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"

from elecsim.src.plants.power_plant import PowerPlant
from elecsim.src.plants.plant_type.fuel import fuel_registry


class FuelPlant(PowerPlant):
    #
    #     super().__init__(self,  name, plant_type, capacity_mw, load_factor, pre_dev_period, construction_period, operating_period, pre_dev_spend_years, construction_spend_years, pre_dev_cost_per_kw, construction_cost_per_kw, infrastructure, fixed_o_and_m_per_mw, variable_o_and_m_per_mwh, insurance_cost_per_kw, connection_cost_per_kw, min_running)
    #
    #     self.efficiency = efficiency
    #     self.fuel = fuel_registry(fuel_type, fuel_price, energy_density, co2_density)

    def __init__(self, name, fuel, capacity_mw):
        """
        Initialisation of power plant object
        :param name: Name of power plant
        :param fuel: Fuel type
        :param capacity_mw: Capacity of power plant in MW
        """

        super().__init__()

        self.name = name
        self.fuel = fuel
        self.capacity_mw = capacity_mw

    def calculate_lcoe(self):
        """
        Function which calculates the levelised cost of electricity for this power plant instance
        :return: Returns LCOE value for power plant
        """

        # Calculations to convert into total costs for this power plant instance

        capex = self.capex()
        opex = self.opex()
        elec_gen = self.electricity_generated()
        fuel_costs = self.fuel_costs(elec_gen)

        print("---CAPEX----")
        print(capex)
        print("---OPEX----")
        print(opex)
        print("---ELEC GEN----")
        print(elec_gen)
        print("---FUEL----")
        print(fuel_costs)

    def fuel_costs(self, electricity_generated):
        """
        Calculates the fuel costs per year based on plant efficiency, electricity generated, endogenous gas prices, and a conversion rate of

        :return: Returns estimated cost of fuel per year
        """

        fuel_costs = (self.fuel.fuel_price[0] * electricity_generated[0])/(self.efficiency*0.029)


        return fuel_costs



