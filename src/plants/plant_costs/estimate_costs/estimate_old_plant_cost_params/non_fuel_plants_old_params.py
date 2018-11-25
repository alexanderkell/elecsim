import numpy as np

from src.plants.plant_costs.estimate_costs.estimate_old_plant_cost_params.old_plant_param_calc import OldPlantCosts


class NonFuelOldPlantCosts(OldPlantCosts):

    def __init__(self, year, plant_type, capacity, discount_rate):
        super().__init__(year=year, plant_type=plant_type, capacity=capacity, discount_rate=discount_rate)

    def estimate_cost_parameters(self):
        """
        Function which estimates the parameters of the non-modern power plant using the LCOE value for the relevant
        year.
        :return: Returns dictionary of the updated parameters for the power plant.
        """
        # List containing parameters to not scale by updated LCOE value. For instance, time taken to build power plant,
        # as they are unrelated.
        params_to_ignore = ['pre_dev_period', 'operating_period', 'construction_period', 'efficiency', 'average_load_factor']

        # Multiply values by updated LCOE scale. Conditional based on whether parameter is in params_to_ignore list or
        # is an np.ndarray (ie. not list).
        params = {key: value*self.lcoe_scaler if type(value) is np.ndarray and key not in params_to_ignore else value
                  for key, value in self.predicted_modern_cost_parameters.items()}
        return params


params = NonFuelOldPlantCosts(2005,"CCGT", 1200, 0.035).estimate_cost_parameters()
print(params)
