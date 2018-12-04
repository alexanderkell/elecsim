from scipy.optimize import minimize

import src.scenario.scenario_data as scenario
from plants.plant_type.fuel_plants.fuel_plant import FuelPlant
from src.plants.fuel.fuel_registry.fuel_registry import plant_type_to_fuel
from src.plants.plant_costs.estimate_costs.estimate_old_plant_cost_params.old_plant_param_calc import OldPlantCosts


class FuelOldPlantCosts(OldPlantCosts):

    historic_fuel_price = scenario.historical_fuel_prices_long

    def __init__(self, year, plant_type, capacity):
        super().__init__(year=year, plant_type=plant_type, capacity=capacity)
        self.fuel = plant_type_to_fuel(self.plant_type)

    def estimate_fuel_costs(self):
        # print(self.historic_fuel_price)
        print("TEST")

    def calc_total_expenditure(self, expenditure):
        total_expenditure = sum(expenditure)
        return total_expenditure

    def calc_total_fuel_expenditure(self, mean_fuel_cost):
        """
        Function which takes the mean
        :param mean_fuel_cost:
        :return:
        """
        fuel_costs = self.plant.fuel_costs(self.plant.electricity_generated())
        total_fuel_costs = sum(fuel_costs)
        return total_fuel_costs
        # (mean_fuel_cost*self.plant.average_load_factor*HOURS_IN_DAY*DAYS_IN_YEAR*self.plant.capacity_mw*self.plant.operating_period)/self.plant.efficiency

    def estimate_cost_parameters(self):
        """
        Function which estimates the parameters of the non-modern fuel power plant using the LCOE value for the relevant
        year.
        :return: Returns dictionary of the updated parameters for the power plant.
        """

        # Functionality that calculates the average fuel price over the lifetime of the power plant
        # fuel_price_filtered = self.historic_fuel_price[self.historic_fuel_price.Fuel == self.fuel]
        # extrap_obj = ExtrapolateInterpolate(fuel_price_filtered.Year, fuel_price_filtered.value)
        # average_fuel_cost = [float(extrap_obj(x)) for x in range(self.year, self.year+int(self.plant.operating_period)+1)]
        # average_fuel_cost = sum(average_fuel_cost)/len(average_fuel_cost)
        # List containing parameters to not scale by updated LCOE value. For instance, time taken to build power plant,
        # as they are not related.
        params_to_ignore = ['pre_dev_period', 'operating_period', 'construction_period', 'efficiency',
                            'average_load_factor', 'construction_spend_years', 'pre_dev_spend_years']
        dict_to_ignore = {key: self.estimated_modern_plant_parameters[key] for key in self.estimated_modern_plant_parameters
                          if key in params_to_ignore}

        params_for_scaling = {key: self.estimated_modern_plant_parameters[key] for key in self.estimated_modern_plant_parameters
                              if key not in params_to_ignore}

        parameter_values = list(params_for_scaling.values())

        linear_optimisation_results = self._linear_optimisation(parameter_values, self.estimated_historical_lcoe)
        linear_optimisation_parameters = linear_optimisation_results['x'].tolist()

        scaled_parameters = {key: params for key, params in
                             zip(self.estimated_modern_plant_parameters, linear_optimisation_parameters)
                             if key not in params_to_ignore}
        
        
        # params = {key: value*opex_capex_scaler if type(value) is np.ndarray and key not in params_to_ignore else value
        #           for key, value in self.estimated_modern_plant_parameters.items()}
        scaled_parameters.update(dict_to_ignore)
        return scaled_parameters

    def _linear_optimisation(self, x, lcoe_required):

        connection_cost_per_mw = x[0]
        construction_cost_per_kw = x[1]
        fixed_o_and_m_per_mw = x[2]
        infrastructure = x[3]
        insurance_cost_per_mw = x[4]
        pre_dev_cost_per_kw = x[5]
        variable_o_and_m_per_mwh = x[6]

        cons = [{'type': 'eq', 'fun': lambda x: x[0] / x[1] - connection_cost_per_mw / construction_cost_per_kw},
                {'type': 'eq', 'fun': lambda x: x[1] / x[2] - construction_cost_per_kw / fixed_o_and_m_per_mw},
                {'type': 'eq', 'fun': lambda x: x[2] / x[3] - fixed_o_and_m_per_mw / infrastructure},
                {'type': 'eq', 'fun': lambda x: x[3] / x[4] - infrastructure / insurance_cost_per_mw},
                {'type': 'eq', 'fun': lambda x: x[4] / x[5] - insurance_cost_per_mw / pre_dev_cost_per_kw},
                {'type': 'eq', 'fun': lambda x: x[5] / x[6] - pre_dev_cost_per_kw / variable_o_and_m_per_mwh},
                {'type': 'eq', 'fun': lambda x: self._calculate_lcoe_wrapper(x)-lcoe_required}]

        return minimize(self._calculate_lcoe_wrapper, x0=x, constraints=cons)

    def _calculate_lcoe_wrapper(self, x0):
        """
        Calculates the LCOE class through the use of the FuelPlant class.
        :param params: Dict which contains parameters for the FuelPlant class
        :return: LCOE
        """

        test_params = {key:value for key, value in zip(self.estimated_modern_plant_parameters, x0)}

        holder_plant = FuelPlant(**test_params, name="LinOptim", plant_type=self.plant_type, capacity_mw=self.capacity,
                                 construction_year=2018, average_load_factor=self.plant.average_load_factor,
                                 efficiency=self.plant.efficiency, pre_dev_period=self.plant.pre_dev_period,
                                 construction_period=self.plant.construction_period,
                                 operating_period=self.plant.operating_period,
                                 pre_dev_spend_years=self.plant.pre_dev_spend_years,
                                 construction_spend_years=self.plant.construction_spend_years)

        lcoe = holder_plant.calculate_lcoe(self.discount_rate)

        return lcoe

