"""fuel.py: Class which specifies the properties of a fuel"""

import pandas as pd
import elecsim.src.scenario.scenario_data as scenario

pd.melt

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"


class Fuel():

    def __init__(self, fuel_type, fuel_price, energy_density, co2_density):
        """
        Constructor which defines the characteristics of a fuel
        :param fuel_type: Type of fuel which is created
        :param fuel_price: List containing price of fuel per year
        :param energy_density: Energy density of fuel (GJ per tonne)
        :param co2_density: Carbon density of fuel (tonnes of CO2 per tonne of gas burnt)
        """

        self.fuel_type = fuel_type
        self.fuel_price = fuel_price
        self.energy_density = energy_density
        self.co2_density = co2_density


def fuel_registry(fuel_type, fuel_price, energy_density=None, co2_density=None):
    """
    Method which creates a Fuel object. Presets are defined for different fuels, and new fuels can be added
    based upon their name, carbon density and energy density
    :param fuel_type: Name of fuel. Preset fuels are "Gas", "Coal", "Biomass_wood",
        "Biomass_poultry_litter", "Oil", "Diesel", "Straw", "Meat"
    :param energy_density: Energy density of fuel (GJ per tonne)
    :param co2_density: Carbon density of fuel (tonnes of CO2 per tonne of gas burnt)
    :return: Returns a Fuel object with characteristics of the fuel in question
    """
    if energy_density is None and co2_density is None:
        if fuel_type == "Gas":
            return Fuel(fuel_type, scenario.gas_prices, 35.8, 2.03)
        if fuel_type == "Coal":
            return Fuel(fuel_type, scenario.coal_price, 24.1, 2.23)
        if fuel_type == "Biomass_wood":
            return Fuel(fuel_type, scenario.woodchip_price, 19.0, 0)
        if fuel_type == "Biomass_poultry_litter":
            return Fuel(fuel_type, scenario.poultry_litter_price, 7.9, 0)
        if fuel_type == "Oil":
            return Fuel(fuel_type, scenario.oil_price, 40.7, 3.2)
        if fuel_type == "Diesel":
            return Fuel(fuel_type, scenario.diesel_price, 42.6, 3.19)
        if fuel_type == "Straw":
            return Fuel(fuel_type, scenario.straw_price, 13.1, 0)
        if fuel_type == "Meat":
            return Fuel(fuel_type, scenario.meat_price, 16.2, 0)
        if fuel_type == "Waste_post_2000":
            return Fuel(fuel_type, scenario.waste_price_post_2000, 13, 0)
        if fuel_type == "Waste_pre_2000":
            return Fuel(fuel_type, scenario.waste_price_pre_2000, 13, 0)
        else:
            raise ValueError("Must provide energy and carbon densities as fuel is not preset.")
    elif co2_density is None:
        if energy_density > 0:
            return Fuel(fuel_type, fuel_price, energy_density,0)
        else:
            raise ValueError("Energy Density must be greater than 0")
    else:
        if energy_density > 0 & co2_density > 0:
            return Fuel(fuel_type,fuel_price, energy_density,co2_density)
        else:
            raise ValueError("Both energy density and co2 density must be larger than 0")
