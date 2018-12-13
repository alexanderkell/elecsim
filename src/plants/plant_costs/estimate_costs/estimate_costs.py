from src.plants.plant_costs.estimate_costs.estimate_old_plant_cost_params.fuel_plant_calculations.fuel_plants_old_params import FuelOldPlantCosts
from src.plants.plant_costs.estimate_costs.estimate_old_plant_cost_params.non_fuel_plant_calculations.non_fuel_plants_old_params import NonFuelOldPlantCosts
from src.plants.plant_costs.estimate_costs.estimate_modern_power_plant_costs.predict_modern_plant_costs import PredictModernPlantParameters
from src.plants.plant_type.plant_registry import PlantRegistry
import src.scenario.scenario_data as scenario

from numpy import isnan

"""
File name: select_cost_estimator
Date created: 01/12/2018
Feature: # Functionality to estimate costs based on year. If year is past 2018 then use modern data from BEIS file.
         # If data is historic, then predict from historic LCOE values, maintaining same ratios from 2018.
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"

EARLIEST_MODERN_PLANT_YEAR = 2018


def select_cost_estimator(start_year, plant_type, capacity):
    check_digit(capacity, "capacity")
    check_digit(start_year, "start_year")
    check_positive(start_year, "start_year")
    check_positive(capacity, "start_year")

    hist_costs = scenario.power_plant_historical_costs_long
    # hist_costs = hist_costs[hist_costs.Technology == plant_type].dropna()
    hist_costs = hist_costs[hist_costs.Technology.map(lambda x: x in plant_type)].dropna()
    # hist_costs = hist_costs.filter(like=plant_type, axis=0).dropna
    # hist_costs = hist_costs[hist_costs.Technology.str.contains("Biomass")].dropna()

    if start_year < EARLIEST_MODERN_PLANT_YEAR and not hist_costs.empty:
        require_fuel = PlantRegistry(plant_type).check_if_fuel_required()
        cost_parameters = estimate_old_plant_cost_parameters(capacity, plant_type, require_fuel, start_year)
        print('cost_parameters: {}'.format(cost_parameters))
        check_parameters(capacity, cost_parameters, plant_type, start_year)
        return cost_parameters
    else:
        cost_parameters = PredictModernPlantParameters(plant_type, capacity, start_year).parameter_estimation()
        check_parameters(capacity, cost_parameters, plant_type, start_year)
        return PredictModernPlantParameters(plant_type, capacity, start_year).parameter_estimation()


def check_parameters(capacity, cost_parameters, plant_type, start_year):
    assert not all(value == 0 for value in
                   cost_parameters.values()), "All values are 0 for cost parameters for power plant of year {}, type {}, and capacity {}".format(
        start_year, plant_type, capacity)
    assert not any(isnan(value).any() for value in
                   cost_parameters.values()), "All values are nan for cost parameters for power plant of year {}, type {}, and capacity {}".format(
        start_year, plant_type, capacity)


def check_digit(value, string):
    if not isinstance(value, int) and not isinstance(value, float):
        raise ValueError("{} must be a number".format(string))

def check_positive(variable, string):
    if variable < 0:
        raise ValueError("{} must be greater than 0".format(string))


def estimate_old_plant_cost_parameters(capacity, plant_type, require_fuel, start_year):
    if require_fuel:
        fuel_plant_parameters = FuelOldPlantCosts(start_year, plant_type, capacity)
        return fuel_plant_parameters.estimate_cost_parameters()
    else:
        non_fuel_plant_parameters = NonFuelOldPlantCosts(start_year, plant_type, capacity)
        return non_fuel_plant_parameters.get_cost_parameters()
