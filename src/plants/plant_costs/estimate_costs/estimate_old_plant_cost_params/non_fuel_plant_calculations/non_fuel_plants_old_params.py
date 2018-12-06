import numpy as np
from math import isnan

from src.plants.plant_costs.estimate_costs.estimate_old_plant_cost_params.old_plant_param_calc import OldPlantCosts


class NonFuelOldPlantCosts(OldPlantCosts):

    def __init__(self, year, plant_type, capacity):
        super().__init__(year=year, plant_type=plant_type, capacity=capacity)

    def estimate_cost_parameters(self):
        """
        Function which estimates the parameters of the non-modern power plant using the LCOE value for the relevant
        year.
        :return: Returns dictionary of the updated parameters for the power plant.
        """
        # List containing parameters to not scale by updated LCOE value. For instance, time taken to build power plant,
        # as they are unrelated.
        params_to_ignore = ['pre_dev_period', 'operating_period', 'construction_period', 'efficiency', 'average_load_factor']

        dict_to_ignore = {key: self.estimated_modern_plant_parameters[key] for key in self.estimated_modern_plant_parameters
                          if key in params_to_ignore}

        # Multiply values by updated LCOE scale. Conditional based on whether parameter is in params_to_ignore list or
        # is an np.ndarray (ie. not list).
        scaled_params = {key: value*self.lcoe_scaler if type(value) is np.ndarray and key not in params_to_ignore else value
                  for key, value in self.estimated_modern_plant_parameters.items()}

        scaled_params.update(dict_to_ignore)

        # scaled_params = {key:0 if not isinstance(scaled_params[key], (list,)) if isnan(scaled_params[key]) else scaled_params[key] for key in scaled_params}

        # scaled_params = {
        # key: 0 if not isinstance(scaled_params[key], list) else scaled_params[key] if isnan(scaled_params[key]) else
        # scaled_params[key] for key in scaled_params}

        scaled_params = self.convert_nan_to_0(scaled_params)

        return scaled_params

    def convert_nan_to_0(self, scaled_params):
        for key in scaled_params:
            if not isinstance(scaled_params[key], list):
                if isnan(scaled_params[key]):
                    scaled_params[key] = 0
        return scaled_params
