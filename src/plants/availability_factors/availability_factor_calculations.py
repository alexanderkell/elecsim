from src.data_manipulation.data_modifications.extrapolation_interpolate import ExtrapolateInterpolate
from src.scenario.scenario_data import historical_availability_factor, fuel_plant_availability

"""
File name: availability_factor_calculations
Date created: 13/01/2019
Feature: #Enter feature description here
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"


def get_availability_factor(plant_type, construction_year):
    simplified_type = get_plant_type_for_data(plant_type)
    if plant_type in ['CCGT', "OCGT", "Coal", 'CHP']:
        availability_factor_series = historical_availability_factor[(historical_availability_factor.plant_type==simplified_type)][['Year','capacity_factor']]
        availability_factor = ExtrapolateInterpolate(availability_factor_series.Year, availability_factor_series.capacity_factor)(construction_year)
    else:
        availability_factor = fuel_plant_availability
    return availability_factor


def get_plant_type_for_data(plant_type):
    if plant_type == "CCGT":
        plant = 'combined_cycle'
    elif plant_type == "OCGT":
        plant = 'combined_cycle'
    elif plant_type == "Coal":
        plant = 'Coal'
    elif plant_type == "CHP":
        plant = "CHP"
    else:
        return fuel_plant_availability
    return plant

