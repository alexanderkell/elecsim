from functools import lru_cache

import elecsim.scenario.scenario_data
from elecsim.constants import GJ_TO_MW
from elecsim.plants.fuel.fuel import Fuel

"""
File name: fuel_registry
Date created: 29/11/2018
Feature: #Enter feature description here
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"


@lru_cache()
def fuel_registry(fuel_type, fuel_price=None, energy_density=None, co2_density=None, mwh_to_co2e_conversion_factor=None):
    """
    Method which creates a Fuel object. Presets are defined for different fuels, and new fuels can be added
    based upon their name, carbon density and energy density
    :param fuel_type: Name of plant_type. Preset fuels are "Gas", "Coal", "Biomass_wood",
        "Biomass_poultry_litter", "Oil", "Diesel", "Straw", "Meat"
    :param fuel_price: Average price of fuel per year
    :param energy_density: Energy density of fuel (MWh per tonne)
    :param co2_density: Carbon density of fuel (tonnes of CO2 per tonne of fuel burnt)
    :param mwh_to_co2e_conversion_factor: Conversion factor to convert MWh to CO2e emissions. Source: Department for business, energy and industrial strategy: UK Government GHG Conversion Factors for Company Reporting,
    :return: Returns a Fuel object with characteristics of the plant_type in question
    """

    fuel_prices = elecsim.scenario.scenario_data.fuel_prices

    if energy_density is None and co2_density is None:
        if fuel_type == "Gas":
            return Fuel(fuel_type, fuel_prices[fuel_prices.Fuel == fuel_type], 35.8*GJ_TO_MW, 0.00203, 0.18396)
        if fuel_type == "Coal":
            return Fuel(fuel_type, fuel_prices[fuel_prices.Fuel == fuel_type], 24.1*GJ_TO_MW, 0.002231398, 0.31112)
        if fuel_type == "Uranium" or "Nuclear":
            return Fuel(fuel_type, fuel_prices[fuel_prices.Fuel == fuel_type], 1296000*GJ_TO_MW, 0, 0)
        if fuel_type == "Wind" or "Wind (offshore)":
            return Fuel(fuel_type, 0, 0, 0, 0)
        if fuel_type == "Solar":
            return Fuel(fuel_type, 0, 0, 0, 0)
        if fuel_type == "Hydro":
            return Fuel(fuel_type, 0, 0, 0, 0)
        if fuel_type == "Biomass_wood":
            return Fuel(fuel_type, fuel_prices[fuel_prices.Fuel == 'Woodchip'], 19.0*GJ_TO_MW, 0, 0.01506)
        if fuel_type == "Biomass_poultry_litter":
            return Fuel(fuel_type, fuel_prices[fuel_prices.Fuel == fuel_type], 7.9*GJ_TO_MW, 0, 0)
        if fuel_type == "Oil":
            return Fuel(fuel_type, fuel_prices[fuel_prices.Fuel == fuel_type], 40.7*GJ_TO_MW, 0.003200345, 0.26831)
        if fuel_type == "Diesel" or "Gas oil":
            return Fuel(fuel_type, fuel_prices[fuel_prices.Fuel == fuel_type], 42.6*GJ_TO_MW, 0.00319, 0.27652)
        if fuel_type == "Straw":
            return Fuel(fuel_type, fuel_prices[fuel_prices.Fuel == fuel_type], 13.1*GJ_TO_MW, 0, 0.01314)
        if fuel_type == "Meat":
            return Fuel(fuel_type, fuel_prices[fuel_prices.Fuel == fuel_type], 16.2*GJ_TO_MW, 0, 0)
        if fuel_type == "Waste_post_2000":
            return Fuel(fuel_type, fuel_prices[fuel_prices.Fuel == fuel_type], 13*GJ_TO_MW, 0.00033777, 0.001215972) # Taken average carbon emissions per tonne of mixture, and converted to conversion factor using tonne of CO2 emitted per tonne of waste. CO2 per tonne of waste taken from: Energy recovery for residual waste, a carbon based modelling approach. 11918_WR1910Energyrecoveryforresidualwaste-Acarbonbasedmodellingapporach.pdf
        if fuel_type == "Waste_pre_2000":
            return Fuel(fuel_type, fuel_prices[fuel_prices.Fuel == fuel_type], 13*GJ_TO_MW, 0.00033777, 0.001215972)
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


def plant_type_to_fuel(plant_type, construction_year=None):
    """
    Function which infers fuel type from plant plant_type.
    :return: String detailing fuel type
    """
    if plant_type == "CCGT":
        return "Gas"
    elif plant_type == "Recip_gas":
        return "Gas"
    elif plant_type == "Meat":
        return "Meat"
    elif plant_type == "Wind (offshore)":
        return None
    elif plant_type == "Offshore":
        return None
    elif plant_type == "Biomass_poultry_litter":
        return "Poultry_litter"
    elif plant_type == "Biomass_meat":
        return "Meat"
    elif plant_type == "Biomass_straw":
        return "Straw"
    elif plant_type == "Diesel":
        return "Diesel"
    elif plant_type == "Biomass_wood":
        return "Woodchip"
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
    elif plant_type == "Recip_diesel":
        return "Diesel"
    elif plant_type == "Gas oil":
        return "Diesel"
    elif plant_type == "EfW" and construction_year<=2000:
        return "Waste_pre_2000"
    elif plant_type == "EfW" and construction_year>2000:
        return "Waste_pre_2000"
    elif plant_type == "Pumped storage":
        return None
    elif plant_type == "Onshore":
        return None
    elif plant_type == "Offshore":
        return None
    elif plant_type == "Wind":
        return None
    elif plant_type == "PV":
        return None
    elif plant_type == "Pumped_storage":
        return None
    elif plant_type == "Hydro":
        return None
    elif plant_type == "Hydro_Store":
        return None
    else:
        raise ValueError("No fuel data for {}".format(plant_type))


