"""fuel.py: Class which specifies the properties of a fuel"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"


class Fuel():

    def __init__(self, fuel_type, fuel_price, energy_density, co2_density, mwh_to_co2e_conversion_factor=0.0):
        """
        Constructor which defines the characteristics of a plant_type
        :param fuel_type: Type of plant_type which is created
        :param fuel_price: List containing price of plant_type per year
        :param energy_density: Energy density of plant_type (GJ per tonne)
        :param co2_density: Carbon density of plant_type (tonnes of CO2 per tonne of gas burnt)
        :param mwh_to_co2e_conversion_factor: Conversion factor to convert MWh to CO2e emissions
        """

        self.fuel_type = fuel_type
        self.fuel_price = fuel_price
        self.energy_density = energy_density
        self.co2_density = co2_density
        self.mwh_to_co2e_conversion_factor = mwh_to_co2e_conversion_factor

