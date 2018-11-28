"""fuel.py: Class which specifies the properties of a fuel"""

import src.scenario.scenario_data as scenario


__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"


class Fuel():

    def __init__(self, fuel_type, fuel_price, energy_density, co2_density):
        """
        Constructor which defines the characteristics of a plant_type
        :param fuel_type: Type of plant_type which is created
        :param fuel_price: List containing price of plant_type per year
        :param energy_density: Energy density of plant_type (GJ per tonne)
        :param co2_density: Carbon density of plant_type (tonnes of CO2 per tonne of gas burnt)
        """

        self.fuel_type = fuel_type
        self.fuel_price = fuel_price
        self.energy_density = energy_density
        self.co2_density = co2_density


def fuel_registry(fuel_type, fuel_price=None, energy_density=None, co2_density=None):
    """
    Method which creates a Fuel object. Presets are defined for different fuels, and new fuels can be added
    based upon their name, carbon density and energy density
    :param fuel_type: Name of plant_type. Preset fuels are "Gas", "Coal", "Biomass_wood",
        "Biomass_poultry_litter", "Oil", "Diesel", "Straw", "Meat"
    :param fuel_price: Price of plant_type per year ()
    :param energy_density: Energy density of plant_type (GJ per tonne)
    :param co2_density: Carbon density of plant_type (tonnes of CO2 per tonne of gas burnt)
    :return: Returns a Fuel object with characteristics of the plant_type in question
    """

    fuel_prices = scenario.total_fuel_prices

    if energy_density is None and co2_density is None:
        if fuel_type == "Gas":
            return Fuel(fuel_type, fuel_prices[fuel_prices.Fuel == fuel_type], 35.8, 2.03)
        if fuel_type == "Coal":
            return Fuel(fuel_type, fuel_prices[fuel_prices.Fuel == fuel_type], 24.1, 2.23)
        if fuel_type == "Uranium" or "Nuclear":
            return Fuel(fuel_type, fuel_prices[fuel_prices.Fuel == fuel_type], 1296000, 0)
        if fuel_type == "Wind" or "Wind (offshore)":
            return Fuel(fuel_type, 0, 0, 0)
        if fuel_type == "Solar":
            return Fuel(fuel_type, 0, 0, 0)
        if fuel_type == "Hydro":
            return Fuel(fuel_type, 0, 0, 0)
        if fuel_type == "Biomass_wood":
            return Fuel(fuel_type, fuel_prices[fuel_prices.Fuel == fuel_type], 19.0, 0)
        if fuel_type == "Biomass_poultry_litter":
            return Fuel(fuel_type, fuel_prices[fuel_prices.Fuel == fuel_type], 7.9, 0)
        if fuel_type == "Oil":
            return Fuel(fuel_type, fuel_prices[fuel_prices.Fuel == fuel_type], 40.7, 3.2)
        if fuel_type == "Diesel" or "Gas oil":
            return Fuel(fuel_type, fuel_prices[fuel_prices.Fuel == fuel_type], 42.6, 3.19)
        if fuel_type == "Straw":
            return Fuel(fuel_type, fuel_prices[fuel_prices.Fuel == fuel_type], 13.1, 0)
        if fuel_type == "Meat":
            return Fuel(fuel_type, fuel_prices[fuel_prices.Fuel == fuel_type], 16.2, 0)
        if fuel_type == "Waste_post_2000":
            return Fuel(fuel_type, fuel_prices[fuel_prices.Fuel == fuel_type], 13, 0)
        if fuel_type == "Waste_pre_2000":
            return Fuel(fuel_type, fuel_prices[fuel_prices.Fuel == fuel_type], 13, 0)
        else:
            raise ValueError("Must provide energy and carbon densities as plant_type is not preset.")
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



    # if energy_density is None and co2_density is None:
    #     if fuel_type == "Gas":
    #         return Fuel(fuel_type, scenario.gas_price, 35.8, 2.03)
    #     if fuel_type == "Coal":
    #         return Fuel(fuel_type, scenario.coal_price, 24.1, 2.23)
    #     if fuel_type == "Uranium" or "Nuclear":
    #         return Fuel(fuel_type, scenario.uranium_price, 1296000, 0)
    #     if fuel_type == "Wind" or "Wind (offshore)":
    #         return Fuel(fuel_type, 0, 0, 0)
    #     if fuel_type == "Solar":
    #         return Fuel(fuel_type, 0, 0, 0)
    #     if fuel_type == "Hydro":
    #         return Fuel(fuel_type, 0, 0, 0)
    #     if fuel_type == "Biomass_wood":
    #         return Fuel(fuel_type, scenario.woodchip_price, 19.0, 0)
    #     if fuel_type == "Biomass_poultry_litter":
    #         return Fuel(fuel_type, scenario.poultry_litter_price, 7.9, 0)
    #     if fuel_type == "Oil":
    #         return Fuel(fuel_type, scenario.oil_price, 40.7, 3.2)
    #     if fuel_type == "Diesel" or "Gas oil":
    #         return Fuel(fuel_type, scenario.diesel_price, 42.6, 3.19)
    #     if fuel_type == "Straw":
    #         return Fuel(fuel_type, scenario.straw_price, 13.1, 0)
    #     if fuel_type == "Meat":
    #         return Fuel(fuel_type, scenario.meat_price, 16.2, 0)
    #     if fuel_type == "Waste_post_2000":
    #         return Fuel(fuel_type, scenario.waste_price_post_2000, 13, 0)
    #     if fuel_type == "Waste_pre_2000":
    #         return Fuel(fuel_type, scenario.waste_price_pre_2000, 13, 0)
    #     else:
    #         raise ValueError("Must provide energy and carbon densities as plant_type is not preset.")
    # elif co2_density is None:
    #     if energy_density > 0:
    #         return Fuel(fuel_type, fuel_price, energy_density,0)
    #     else:
    #         raise ValueError("Energy Density must be greater than 0")
    # else:
    #     if energy_density > 0 & co2_density > 0:
    #         return Fuel(fuel_type,fuel_price, energy_density,co2_density)
    #     else:
    #         raise ValueError("Both energy density and co2 density must be larger than 0")


def plant_type_to_fuel(plant_type):
    """
    Function which infers fuel type from plant type.
    :return: String detailing fuel type
    """
    if plant_type == "CCGT":
        return "Gas"
    elif plant_type == "Meat":
        return "Meat"
    elif plant_type == "Wind (offshore)":
        return None
    elif plant_type == "Offshore":
        return None
    elif plant_type == "Biomass_poultry_litter":
        return "Biomass_poultry_litter"
    elif plant_type == "Straw":
        return "Straw"
    elif plant_type == "Diesel":
        return "Diesel"
    elif plant_type == "Biomass_wood":
        return "Biomass_wood"
    elif plant_type == "Gas":
        return "Gas"
    elif plant_type == "Nuclear":
        return "Uranium"
    elif plant_type == "Coal":
        return "Coal"
    elif plant_type == "Solar":
        return None
    elif plant_type == "OCGT":
        return "Gas"
    elif plant_type == "Gas oil":
        return "Gas oil"
    elif plant_type == "Waste":
        return "Waste"
    elif plant_type == "Pumped storage":
        return None
    elif plant_type == "Wind":
        return None


