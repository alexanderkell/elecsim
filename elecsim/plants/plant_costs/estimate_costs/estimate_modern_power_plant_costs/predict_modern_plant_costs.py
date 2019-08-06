import logging
import math
from random import uniform
from functools import lru_cache

from scipy.interpolate import interp1d

import elecsim.scenario.scenario_data
from elecsim.data_manipulation.data_modifications.extrapolation_interpolate import ExtrapolateInterpolate
from elecsim.plants.fuel.fuel_registry.fuel_registry import plant_type_to_fuel

logger = logging.getLogger(__name__)

from elecsim.data_manipulation.data_modifications.value_estimations import closest_row



class PredictModernPlantParameters:
    def __init__(self, plant_type, capacity, start_year):
        """
        Class which provides calculations to provide costing data for power plants based on plant_type, capacity and start year
        :param plant_type (str): Type of plant_type that plant runs on
        :param capacity (int): Capacity of plant in MW
        :param start_year (int): Year that power plant begun construction
        """
        self.plant_type = plant_type
        self.capacity = float(capacity)
        self.start_year = float(start_year)

        # Import UK power plant cost data
        self.cost_data = elecsim.scenario.scenario_data.modern_plant_costs
        self.year_data = [int(sub.split(" _")[1]) for sub in self.cost_data.filter(regex="Connect_system_cost-Medium ").columns]
        # self.cost_data = self.cost_data[self.cost_data.Type == self.plant_type].sort_values('Plant_Size')
        self.cost_data = self.cost_data[self.cost_data.apply(lambda x: x['Type'] in self.plant_type, axis=1)].sort_values('Plant_Size')

    def parameter_estimation(self):
        """
        Function which estimates costs of power plant based on capacity, plant_type and start year. Use of linear interpolation
        for plants of capacity that fall within known range of costing variables. If plant capacity to be calculated
        falls out of range of known values, the highest or lowest capacity value is chosen.
        :return (:obj:`dict`:obj:`str`): Returns dictionary containing variables for PowerPlant cost
        """

        # Iterates through each type of plant cost to predict parameters.
        initial_stub_cost_parameters = ['Connect_system_cost-Medium _', 'Constr_cost-Medium _', 'Fixed_cost-Medium _',
                                        'Infra_cost-Medium _', 'Insurance_cost-Medium _', 'Pre_dev_cost-Medium _',
                                        'Var_cost-Medium _']

        condition = True
        while condition:
            full_cost_parameters = self._create_parameter_names(initial_stub_cost_parameters)

            parameters_of_plant = {
                self._change_columns(cost_variable_required): ExtrapolateInterpolate(self.cost_data['Plant_Size'],
                                                                                     self.cost_data[
                                                                                         cost_variable_required])(self.capacity)
                for cost_variable_required in full_cost_parameters}
            self.check_plant_exists(parameters_of_plant)

            if all(math.isnan(value) for value in parameters_of_plant.values()):
                self.start_year += 1
            else:
                condition = False

        durations = ['Pre_Dur', 'Operating_Period', 'Constr_Dur', 'Efficiency', 'Average_Load_Factor']
        durations_parameters = {self._change_columns(dur): self._estimate_non_interpolatable_parameters(dur) for dur in durations}
        # logger.info(self._estimate_non_interpolatable_parameters.cache_info())
        yearly_cost_spread = ['Constr', 'Pre']

        yearly_cost_perc = {self._change_columns(spread): self._payment_spread_estimator(spread) for spread in
                            yearly_cost_spread}

        parameters = {**parameters_of_plant, **durations_parameters, **yearly_cost_perc}
        parameters = self.check_pre_dev_spend(parameters)
        parameters['variable_o_and_m_per_mwh'] *= uniform(elecsim.scenario.scenario_data.o_and_m_multiplier[0], elecsim.scenario.scenario_data.o_and_m_multiplier[1])
        self._use_historical_efficiency_data(parameters)

        return parameters

    def _use_historical_efficiency_data(self, parameters):
        if self.plant_type in ['CCGT', 'Coal'] and self.start_year < 2018:
            fuel_used = plant_type_to_fuel(self.plant_type)
            historical_efficiency_measure = elecsim.scenario.scenario_data.historical_fuel_plant_efficiency[
                elecsim.scenario.scenario_data.historical_fuel_plant_efficiency.fuel_type == fuel_used]

            historical_efficiency_measure = historical_efficiency_measure.reset_index()
            efficiency = ExtrapolateInterpolate(historical_efficiency_measure.Year,
                                                historical_efficiency_measure.efficiency).min_max_extrapolate(
                self.start_year)
            parameters['efficiency'] = efficiency

    @staticmethod
    def check_pre_dev_spend(parameters):
        if not parameters['pre_dev_spend_years']:
            parameters['pre_dev_cost_per_mw'] = 0
        if not parameters['construction_spend_years']:
            parameters['construction_cost_per_mw'] = 0
        return parameters

    def check_plant_exists(self, parameters_of_plant):
        """
        Function which checks that there is data for specified power plant in the modern costs database.
        :param parameters_of_plant: Dictionary of plant which contains all of the values of the estimated power plant.
        """
        if all(value == 0 for value in parameters_of_plant.values()):
            raise ValueError("No cost data for power plant of type: " + self.plant_type)

    def _create_parameter_names(self, initial_stub_cost_parameters):
        """
        Function that chooses the names of the parameters to search the data file of modern plant costs. For instance,
        choose Connect_system_cost-Medium _2018 for plant built in 2018 and 2019.
        :param plant_costs: 
        :return:
        """


        if self.start_year in self.year_data:
            cost_parameter_variables = [cost_variable + str(int(self.start_year)) for cost_variable in
                                        initial_stub_cost_parameters]
        elif self.start_year > self.year_data[-1]:
            cost_parameter_variables = [cost_variable + str(self.year_data[-1]) for cost_variable in
                                        initial_stub_cost_parameters]
        elif self.year_data[0] < self.start_year < self.year_data[1]:
            cost_parameter_variables = [cost_variable + str(self.year_data[0]) for cost_variable in
                                        initial_stub_cost_parameters]
        elif self.year_data[1] < self.start_year < self.year_data[2]:
            cost_parameter_variables = [cost_variable + str(self.year_data[1]) for cost_variable in
                                        initial_stub_cost_parameters]
        elif self.start_year < self.year_data[0]:
            cost_parameter_variables = [cost_variable + str(self.year_data[0]) for cost_variable in
                                        initial_stub_cost_parameters]

        return cost_parameter_variables

    # @lru_cache(maxsize=10000)
    def _estimate_non_interpolatable_parameters(self, variable_wanted):
        """
        Estimates parameters time scale required for construction, pre-development and operating period.
        This is done by selecting the operating period, construction and pre-development of the closest sized
        power plant in data
        :param variable_wanted (str): Variable that is required to estimate
        :return (int): Returns estimated duration parameter in years.
        """
        column_required = self.cost_data[['Plant_Size', variable_wanted]].dropna()
        if min(column_required.Plant_Size) < self.capacity < max(column_required.Plant_Size):
            interp = interp1d(column_required.Plant_Size, column_required[variable_wanted], kind='nearest')
            return interp(self.capacity)
        elif self.capacity >= max(column_required.Plant_Size):
            column_required = column_required.reset_index()
            return column_required.iloc[-1][variable_wanted]
        elif self.capacity <= min(column_required.Plant_Size):
            column_required = column_required.reset_index()
            return column_required.iloc[0][variable_wanted]

    def _payment_spread_estimator(self, var_wanted):
        """
        Function which selects the spread of payments required for construction and pre-development. This is achieved
        by selecting the power plant of the closest size.
        :param var_wanted (str): Variable to estimate spread of payments.
        :return (:obj:`list` of :obj:`str`): Returns list of percentage of cost per year
        """
        # df_sort = self.cost_data.iloc[(self.cost_data['Plant_Size']-self.capacity).abs().argsort()[:1]]
        df_sort = closest_row(self.cost_data, "Plant_Size", self.capacity)
        df_sort = df_sort.filter(regex=var_wanted).filter(regex='^((?!Dur).)*$').filter(regex='^((?!-).)*$').dropna(
            axis=1).values.tolist()[0]

        return df_sort

    @staticmethod
    def _change_columns(column):
        """
        Function which converts variable names from UK power plant data, to PowerPlant instance variable names for easy
        conversion
        :param column (str): String name of variable from UK power plant data
        :return (str): Name in PowerPlant instance variable name format
        """
        if 'Connect_system_cost' in column:
            return 'connection_cost_per_mw'
        elif 'Constr_cost' in column:
            return 'construction_cost_per_mw'
        elif 'Fixed_cost' in column:
            return 'fixed_o_and_m_per_mw'
        elif 'Infra_cost' in column:
            return 'infrastructure'
        elif 'Insurance_cost' in column:
            return 'insurance_cost_per_mw'
        elif 'Pre_dev_cost' in column:
            return 'pre_dev_cost_per_mw'
        elif 'Var_cost' in column:
            return 'variable_o_and_m_per_mwh'
        elif 'Pre_Dur' in column:
            return 'pre_dev_period'
        elif 'Operating_Period' in column:
            return 'operating_period'
        elif 'Constr_Dur' in column:
            return 'construction_period'
        elif 'Constr' in column:
            return 'construction_spend_years'
        elif 'Pre' in column:
            return 'pre_dev_spend_years'
        elif 'Efficiency' in column:
            return 'efficiency'
        elif 'Average_Load_Factor' in column:
            return 'average_load_factor'
        else:
            raise ValueError('Plant cost data not found')
