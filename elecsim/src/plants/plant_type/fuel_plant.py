""" fuel_plant.py: Child class of power plant which contains functions for a power plant which consumes fuel"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"

from elecsim.src.plants.power_plant import PowerPlant

class fuel_plant(PowerPlant):

    def __init__(self, efficiency, fuel):
        """
        Power plant which is of type which uses fuel.
        :param efficiency: Efficiency of fuel plant at converting fuel to electrical energy
        :param fuel: 
        """

        self.efficiency = efficiency

        self.fuel = fuel

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
        print(elec_gen)


    def fuel_costs(self, fuel_price, electricity_generated):
        """
        Calculates the fuel costs per year based on plant efficiency, electricity generated, endogenous gas prices, and a conversion rate of
        :param fuel_price: Price of fuel for the operation
        :param electricity_generated:
        :return: Returns estimated cost of fuel per year
        """

        fuel_costs = (fuel_price * electricity_generated)/(self.efficiency*0.029)


        return fuel_costs



