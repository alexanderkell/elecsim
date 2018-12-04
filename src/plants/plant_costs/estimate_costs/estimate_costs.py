from src.plants.plant_costs.estimate_costs.estimate_modern_power_plant_costs.predict_modern_plant_costs import PredictModernPlantParameters
from src.plants.plant_costs.estimate_costs.estimate_old_plant_cost_params.non_fuel_plants_old_params import NonFuelOldPlantCosts
from src.plants.plant_costs.estimate_costs.estimate_old_plant_cost_params.fuel_plants_old_params import FuelOldPlantCosts
from src.plants.plant_type.plant_registry import PlantRegistry
"""
File name: estimate_costs
Date created: 01/12/2018
Feature: # Functionality to estimate costs based on year. If year is past 2018 then use modern data from BEIS file.
         # If data is historic, then predict from historic LCOE values, maintaining same ratios from 2018.
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"

EARLIEST_MODERN_PLANT_YEAR = 2018

def estimate_costs(start_year, plant_type, capacity):
    if start_year < EARLIEST_MODERN_PLANT_YEAR:
        require_fuel = PlantRegistry(plant_type).fuel_or_no_fuel()
        if require_fuel:
            fuel_plant_parameters = FuelOldPlantCosts(start_year, plant_type, capacity)
            return fuel_plant_parameters.estimate_cost_parameters()
        else:
            non_fuel_plant_parameters = NonFuelOldPlantCosts(start_year, plant_type, capacity)
            return non_fuel_plant_parameters.estimate_cost_parameters()
    else:
        return PredictModernPlantParameters(plant_type, capacity, start_year).parameter_estimation()
