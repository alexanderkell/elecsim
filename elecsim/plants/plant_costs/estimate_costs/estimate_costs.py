from functools import lru_cache

from numpy import isnan
from numpy import ndarray
import numpy as np
from sklearn.linear_model import LinearRegression

import logging

import elecsim.scenario.scenario_data
from elecsim.plants.plant_costs.estimate_costs.estimate_modern_power_plant_costs.predict_modern_plant_costs import PredictModernPlantParameters
from elecsim.plants.plant_costs.estimate_costs.estimate_old_plant_cost_params.fuel_plant_calculations.fuel_plants_old_params import FuelOldPlantCosts
from elecsim.plants.plant_costs.estimate_costs.estimate_old_plant_cost_params.non_fuel_plant_calculations.non_fuel_plants_old_params import NonFuelOldPlantCosts
from elecsim.plants.plant_registry import PlantRegistry

logger = logging.getLogger(__name__)
"""
File name: _select_cost_estimator
Date created: 01/12/2018
Feature: # Functionality to estimate costs based on year. If year is past 2018 then use modern data from BEIS file.
         # If data is historic, then predict from historic LCOE values, maintaining same ratios from 2018.
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"

@lru_cache(maxsize=10000)
def create_power_plant(name, start_date, simplified_type, capacity):
    """
    Functionality that estimates the cost of a power plant based solely on year of construction, type of plant and capacity.
    :param name: Name of power plant.
    :param start_date: Starting year of power plant
    :param simplified_type: Type of power plant
    :param capacity: Capacity of power plant
    :return: Power plant object initialized with relevant variables.
    """
    estimated_cost_parameters = _select_cost_estimator(start_year=start_date,
                                                       plant_type=simplified_type,
                                                       capacity=capacity)
    power_plant_obj = PlantRegistry(simplified_type).plant_type_to_plant_object()
    power_plant = power_plant_obj(name=name, plant_type=simplified_type,
                                  capacity_mw=capacity, construction_year=start_date,
                                  **estimated_cost_parameters)
    return power_plant

# def create_power_plant_group(name, money, start_date, simplified_type):
def create_power_plant_group(name, start_date, simplified_type, capacity, number_of_plants_to_purchase):
    # capacity = predict_capacity_from_money(money, simplified_type, capacity, start_date)
    plant_object = create_power_plant(name, start_date=start_date, simplified_type=simplified_type, capacity=capacity*number_of_plants_to_purchase)

    # plant_object = create_power_plant(name, start_date=start_date, simplified_type=simplified_type, capacity=capacity)
    return plant_object




# def predict_capacity_from_money(money, simplified_type, capacity, start_date):
#     test_capacity = [capacity, capacity+0.5]
#     plant_1 = create_power_plant("invested_plant", start_date, simplified_type, test_capacity[0])
#     plant_2 = create_power_plant("invested_plant", start_date, simplified_type, test_capacity[1])
#     y = np.array([plant_1.get_upfront_costs(), plant_2.get_upfront_costs()]).reshape(-1, 1)
#     # test_capacity_array = np.array(test_capacity).reshape(-1, 1)
#     test_capacity_array = test_capacity
#     reg = LinearRegression().fit(y, test_capacity_array)
#     size = reg.predict(np.array(money).reshape(-1, 1))
#     return int(size)


def _select_cost_estimator(start_year, plant_type, capacity):
    earliest_modern_plant_year = min([int(column.split(" _")[1]) for column in elecsim.scenario.scenario_data.modern_plant_costs.filter(regex='Connect_system_cost-Medium _').columns])
    _check_digit(capacity, "capacity")
    _check_digit(start_year, "start_year")
    _check_positive(start_year, "start_year")
    _check_positive(capacity, "capacity")

    hist_costs = elecsim.scenario.scenario_data.power_plant_historical_costs_long
    hist_costs = hist_costs[hist_costs.Technology.map(lambda x: x in plant_type)].dropna()
    if start_year < earliest_modern_plant_year and not hist_costs.empty:
        require_fuel = PlantRegistry(plant_type).check_if_fuel_required()
        cost_parameters = _estimate_old_plant_cost_parameters(capacity, plant_type, require_fuel, start_year)
        _check_parameters(capacity, cost_parameters, plant_type, start_year)
        return cost_parameters
    else:
        cost_parameters = PredictModernPlantParameters(plant_type, capacity, start_year).parameter_estimation()
        _check_parameters(capacity, cost_parameters, plant_type, start_year)
        return cost_parameters


def _check_parameters(capacity, cost_parameters, plant_type, start_year):
    assert not all(value == 0 for value in
                   cost_parameters.values()), "All values are 0 for cost parameters for power plant of year {}, type {}, and capacity {}".format(
        start_year, plant_type, capacity)
    assert not any(isnan(value).any() for value in
                   cost_parameters.values()), "All values are nan for cost parameters for power plant of year {}, type {}, and capacity {}".format(
        start_year, plant_type, capacity)


def _check_digit(value, string):
    if not isinstance(value, int) and not isinstance(value, float) and not isinstance(value, ndarray):
        raise ValueError("{} must be a number".format(string))

def _check_positive(variable, string):
    if variable < 0:
        raise ValueError("{} must be greater than 0. Produced is: {}".format(string, variable))


def _estimate_old_plant_cost_parameters(capacity, plant_type, require_fuel, start_year):
    if require_fuel:
        fuel_plant_parameters = FuelOldPlantCosts(start_year, plant_type, capacity)
        return fuel_plant_parameters.estimate_cost_parameters()
    else:
        non_fuel_plant_parameters = NonFuelOldPlantCosts(start_year, plant_type, capacity)
        return non_fuel_plant_parameters.get_cost_parameters()
