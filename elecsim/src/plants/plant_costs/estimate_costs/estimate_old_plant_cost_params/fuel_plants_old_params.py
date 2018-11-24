from elecsim.src.plants.plant_costs.estimate_costs.estimate_old_plant_cost_params.old_plant_param_calc import OldPlantCosts
import elecsim.src.scenario.scenario_data as scenario
import numpy as np
import pandas as pd
from elecsim.src.plants.plant_type.fuel import plant_type_to_fuel
from elecsim.src.data_manipulation.data_modifications.extrapolation_interpolate import ExtrapolateInterpolate

class FuelOldPlantCosts(OldPlantCosts):

    his_fuel_price = scenario.historical_fuel_prices_long

    def __init__(self, year, plant_type, capacity, discount_rate):
        super().__init__(year=year, plant_type=plant_type, capacity=capacity, discount_rate=discount_rate)
        self.fuel = plant_type_to_fuel(self.plant_type)

    def estimate_fuel_costs(self):
        print(self.his_fuel_price)

    def estimate_cost_parameters(self):
        """
        Function which estimates the parameters of the non-modern fuel power plant using the LCOE value for the relevant
        year.
        :return: Returns dictionary of the updated parameters for the power plant.
        """

        # Functionality that calculates the average fuel price over the lifetime of the power plant
        fuel_price_filtered = self.his_fuel_price[self.his_fuel_price.Fuel == self.fuel]
        extrap_obj = ExtrapolateInterpolate(fuel_price_filtered.Price,fuel_price_filtered.value)

        average_fuel_cost = [float(extrap_obj(x)) for x in range(self.year, self.year+int(self.plant.operating_period)+1)]
        average_fuel_cost = sum(average_fuel_cost)/len(average_fuel_cost)



        # List containing parameters to not scale by updated LCOE value. For instance, time taken to build power plant,
        # as they are unrelated.
        params_to_ignore = ['pre_dev_period', 'operating_period', 'construction_period', 'efficiency', 'average_load_factor']

        # Multiply values by updated LCOE scale. Conditional based on whether parameter is in params_to_ignore list or
        # is an np.ndarray (ie. not list).
        params = {key: value*self.lcoe_scaler if type(value) is np.ndarray and key not in params_to_ignore else value
                  for key, value in self.predicted_modern_cost_parameters.items()}
        return params




FuelOldPlantCosts(2017, "CCGT", 1200, 0.035).estimate_cost_parameters()
