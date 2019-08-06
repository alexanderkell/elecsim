import logging

from scipy.optimize import minimize

import elecsim.scenario.scenario_data
from elecsim.plants.fuel.fuel_registry.fuel_registry import plant_type_to_fuel
from elecsim.plants.plant_costs.estimate_costs.estimate_old_plant_cost_params.old_plant_param_calc import OldPlantCosts
from elecsim.plants.plant_type.fuel_plant import FuelPlant

logger = logging.getLogger(__name__)



class FuelOldPlantCosts(OldPlantCosts):

    historic_fuel_price = elecsim.scenario.scenario_data.historical_fuel_prices_long

    def __init__(self, year, plant_type, capacity):
        super().__init__(year=year, plant_type=plant_type, capacity=capacity)
        self.fuel = plant_type_to_fuel(self.plant_type, self.year)

    def estimate_cost_parameters(self):
        """
        Function which estimates the parameters of the non-modern fuel power plant using the LCOE value for the relevant
        year.
        :return: Returns dictionary of the updated parameters for the power plant.
        """

        params_for_scaling = self.estimate_modern_parameters()

        parameter_values = list(params_for_scaling.values())

        linear_optimisation_results = self._linear_optimisation(parameter_values, self.estimated_historical_lcoe)
        linear_optimisation_parameters = linear_optimisation_results['x'].tolist()

        scaled_parameters = {key: params for key, params in
                             zip(self.estimated_modern_plant_parameters, linear_optimisation_parameters)
                             if key not in self.params_to_ignore}

        # logger.debug("scaled_params: {}".format(scaled_parameters))
        # scaled_parameters['variable_o_and_m_per_mwh'] += uniform(-20,20)
        # scaled_parameters['variable_o_and_m_per_mwh'] *= uniform(0.3,2)
        scaled_parameters.update(self.dict_to_ignore)
        return scaled_parameters

    def estimate_modern_parameters(self):
        # self.params_to_ignore = ['pre_dev_period', 'operating_period', 'construction_period', 'efficiency',
        #                          'average_load_factor', 'construction_spend_years', 'pre_dev_spend_years']
        # self.dict_to_ignore = {key: self.estimated_modern_plant_parameters[key] for key in
        #                        self.estimated_modern_plant_parameters
        #                        if key in self.params_to_ignore}

        self.get_params_to_scale()

        params_for_scaling = {key: self.estimated_modern_plant_parameters[key] for key in
                              self.estimated_modern_plant_parameters
                              if key not in self.dict_to_ignore}
        return params_for_scaling

    def _linear_optimisation(self, x, lcoe_required):

        # x = [0.00001 if param == 0 else param for param in x]
        connection_cost_per_mw = x[0]
        construction_cost_per_mw = x[1]
        fixed_o_and_m_per_mw = x[2]
        infrastructure = x[3]
        insurance_cost_per_mw = x[4]
        pre_dev_cost_per_mw = x[5]
        variable_o_and_m_per_mwh = x[6]
        cons = [{'type': 'eq', 'fun': lambda x: x[0] / x[1] - connection_cost_per_mw / construction_cost_per_mw},
                {'type': 'eq', 'fun': lambda x: x[1] / x[2] - construction_cost_per_mw / fixed_o_and_m_per_mw},
                {'type': 'eq', 'fun': lambda x: x[2] / x[3] - fixed_o_and_m_per_mw / infrastructure},
                {'type': 'eq', 'fun': lambda x: x[3] / x[4] - infrastructure / insurance_cost_per_mw},
                {'type': 'eq', 'fun': lambda x: x[4] / x[5] - insurance_cost_per_mw / pre_dev_cost_per_mw},
                {'type': 'eq', 'fun': lambda x: x[5] / x[6] - pre_dev_cost_per_mw / variable_o_and_m_per_mwh},
                {'type': 'ineq', 'fun': lambda x: x[0]},
                {'type': 'ineq', 'fun': lambda x: x[1]},
                {'type': 'ineq', 'fun': lambda x: x[2]},
                {'type': 'ineq', 'fun': lambda x: x[3]},
                {'type': 'ineq', 'fun': lambda x: x[4]},
                {'type': 'ineq', 'fun': lambda x: x[5]},
                {'type': 'eq', 'fun': lambda x: self._calculate_lcoe_wrapper(x)-lcoe_required}]
        result = minimize(self._calculate_lcoe_wrapper, x0=x, constraints=cons)
        return result

    def _calculate_lcoe_wrapper(self, x0):
        """
        Calculates the LCOE class through the use of the FuelPlant class.
        :param params: Dict which contains parameters for the FuelPlant class
        :return: LCOE
        """
        test_params = {key:value for key, value in zip(self.estimated_modern_plant_parameters, x0)}

        holder_plant = FuelPlant(**test_params, name="LinOptim", plant_type=self.plant_type, capacity_mw=self.capacity,
                                 construction_year=self.plant.construction_year,
                                 average_load_factor=self.plant.average_load_factor,
                                 efficiency=self.plant.efficiency, pre_dev_period=self.plant.pre_dev_period,
                                 construction_period=self.plant.construction_period,
                                 operating_period=self.plant.operating_period,
                                 pre_dev_spend_years=self.plant.pre_dev_spend_years,
                                 construction_spend_years=self.plant.construction_spend_years,
                                 )
        lcoe = holder_plant.calculate_lcoe(self.discount_rate)

        return lcoe







#
# class FuelOldPlantCosts(OldPlantCosts):
#
#     historic_fuel_price = scenario.historical_fuel_prices_long
#
#     def __init__(self, year, plant_type, capacity):
#         super().__init__(year=year, plant_type=plant_type, capacity=capacity)
#         self.fuel = plant_type_to_fuel(self.plant_type, self.year)
#
#     def estimate_cost_parameters(self):
#         """
#         Function which estimates the parameters of the non-modern fuel power plant using the LCOE value for the relevant
#         year.
#         :return: Returns dictionary of the updated parameters for the power plant.
#         """
#
#         params_for_scaling = self.estimate_modern_parameters()
#
#         parameter_values = list(params_for_scaling.values())
#
#         linear_optimisation_results = self._linear_optimisation(parameter_values, self.estimated_historical_lcoe)
#         linear_optimisation_parameters = linear_optimisation_results['x'].tolist()
#
#         scaled_parameters = {key: params for key, params in
#                              zip(self.estimated_modern_plant_parameters, linear_optimisation_parameters)
#                              if key not in self.params_to_ignore}
#
#         # logger.debug("scaled_params: {}".format(scaled_parameters))
#         # scaled_parameters['variable_o_and_m_per_mwh'] += uniform(-20,20)
#         # scaled_parameters['variable_o_and_m_per_mwh'] *= uniform(0.3,2)
#         scaled_parameters.update(self.dict_to_ignore)
#         return scaled_parameters
#
#     def estimate_modern_parameters(self):
#         # self.params_to_ignore = ['pre_dev_period', 'operating_period', 'construction_period', 'efficiency',
#         #                          'average_load_factor', 'construction_spend_years', 'pre_dev_spend_years']
#         # self.dict_to_ignore = {key: self.estimated_modern_plant_parameters[key] for key in
#         #                        self.estimated_modern_plant_parameters
#         #                        if key in self.params_to_ignore}
#
#         self.get_params_to_scale()
#
#         params_for_scaling = {key: self.estimated_modern_plant_parameters[key] for key in
#                               self.estimated_modern_plant_parameters
#                               if key not in self.dict_to_ignore}
#         return params_for_scaling
#
#     def _linear_optimisation(self, x, lcoe_required):
#         connection_cost_per_mw = x[0]
#         construction_cost_per_mw = x[1]
#         fixed_o_and_m_per_mw = x[2]
#         infrastructure = x[3]
#         insurance_cost_per_mw = x[4]
#         pre_dev_cost_per_mw = x[5]
#         variable_o_and_m_per_mwh = x[6]
#         cons = [{'type': 'eq', 'fun': lambda x: x[0] / x[1] - connection_cost_per_mw / construction_cost_per_mw},
#                 {'type': 'eq', 'fun': lambda x: x[1] / x[2] - construction_cost_per_mw / fixed_o_and_m_per_mw},
#                 {'type': 'eq', 'fun': lambda x: x[2] / x[3] - fixed_o_and_m_per_mw / infrastructure},
#                 {'type': 'eq', 'fun': lambda x: x[3] / x[4] - infrastructure / insurance_cost_per_mw},
#                 {'type': 'eq', 'fun': lambda x: x[4] / x[5] - insurance_cost_per_mw / pre_dev_cost_per_mw},
#                 {'type': 'eq', 'fun': lambda x: x[5] / x[6] - pre_dev_cost_per_mw / variable_o_and_m_per_mwh},
#                 {'type': 'ineq', 'fun': lambda x: x[0]},
#                 {'type': 'ineq', 'fun': lambda x: x[1]},
#                 {'type': 'ineq', 'fun': lambda x: x[2]},
#                 {'type': 'ineq', 'fun': lambda x: x[3]},
#                 {'type': 'ineq', 'fun': lambda x: x[4]},
#                 {'type': 'ineq', 'fun': lambda x: x[5]},
#                 {'type': 'eq', 'fun': lambda x: self._calculate_lcoe_wrapper(x)-lcoe_required}]
#         result = minimize(self._calculate_lcoe_wrapper, x0=x, constraints=cons)
#         return result
#
#     def _calculate_lcoe_wrapper(self, x0):
#         """
#         Calculates the LCOE class through the use of the FuelPlant class.
#         :param params: Dict which contains parameters for the FuelPlant class
#         :return: LCOE
#         """
#         test_params = {key:value for key, value in zip(self.estimated_modern_plant_parameters, x0)}
#
#         holder_plant = FuelPlant(**test_params, name="LinOptim", plant_type=self.plant_type, capacity_mw=self.capacity,
#                                  construction_year=self.plant.construction_year,
#                                  average_load_factor=self.plant.average_load_factor,
#                                  efficiency=self.plant.efficiency, pre_dev_period=self.plant.pre_dev_period,
#                                  construction_period=self.plant.construction_period,
#                                  operating_period=self.plant.operating_period,
#                                  pre_dev_spend_years=self.plant.pre_dev_spend_years,
#                                  construction_spend_years=self.plant.construction_spend_years,
#                                  )
#         lcoe = holder_plant.calculate_lcoe(self.discount_rate)
#
#         return lcoe
#
