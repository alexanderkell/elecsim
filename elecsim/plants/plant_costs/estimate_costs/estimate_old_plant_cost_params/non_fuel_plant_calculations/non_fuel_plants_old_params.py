from elecsim.plants.plant_costs.estimate_costs.estimate_old_plant_cost_params.old_plant_param_calc import OldPlantCosts


class NonFuelOldPlantCosts(OldPlantCosts):

    def __init__(self, year, plant_type, capacity):
        super().__init__(year=year, plant_type=plant_type, capacity=capacity)

    def get_cost_parameters(self):
        """
        Function which estimates the parameters of the non-modern power plant using the LCOE value for the relevant
        year.
        :return: Returns dictionary of the updated parameters for the power plant.
        """
        # List containing parameters to not scale by updated LCOE value. For instance, time taken to build power plant,
        # as they are unrelated to LCOE value.
        self.get_params_to_scale()

        # Multiply values by updated LCOE scale. Conditional based on whether parameter is in params_to_ignore list
        scaled_params = {
            key: (value * self.lcoe_scaler) if key not in self.dict_to_ignore else value
            for key, value in self.estimated_modern_plant_parameters.items()}

        scaled_params.update(self.dict_to_ignore)

        return scaled_params

