import src.scenario.scenario_data as scenario
import pandas as pd
from scipy.interpolate import interp1d

from src.data_manipulation.data_modifications.value_estimations import closest_row

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 500)


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
        self.cost_data = scenario.power_plant_costs
        self.cost_data = self.cost_data[self.cost_data.Type == self.plant_type].sort_values('Plant_Size')

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

        full_cost_parameters = self._create_parameter_names(initial_stub_cost_parameters)

        parameters_of_plant = {self._change_columns(cost_var): self._extrapolate_interpolate_parameters(cost_var) for cost_var in full_cost_parameters}
        self.check_for_modern_cost_data(parameters_of_plant)

        durations = ['Pre_Dur', 'Operating_Period', 'Constr_Dur', 'Efficiency', 'Average_Load_Factor']
        durations_parameters = {self._change_columns(dur): self._estimate_duration_parameters(dur) for dur in durations}

        yearly_cost_spread = ['Constr', 'Pre']

        yearly_cost_perc = {self._change_columns(spread): self._closest_year_spread(spread) for spread in yearly_cost_spread}

        parameters={**parameters_of_plant, **durations_parameters, **yearly_cost_perc}

        return parameters

    def check_for_modern_cost_data(self, parameters_of_plant):
        if all(value == 0 for value in parameters_of_plant.values()):
            raise ValueError("No cost data for power plant of type:", self.plant_type)

    def _create_parameter_names(self, initial_stub_cost_parameters):
        """
        Function that chooses the names of the parameters to search the data file of modern plant costs. For instance,
        choose Connect_system_cost-Medium _2018 for plant built in 2018 and 2019.
        :param plant_costs: 
        :return:
        """

        if self.start_year in (2018, 2020, 2025):
            cost_parameter_variables = [cost_variable + str(int(self.start_year)) for cost_variable in initial_stub_cost_parameters]
        elif self.start_year > 2025:
            cost_parameter_variables = [cost_variable + str(int(2025)) for cost_variable in initial_stub_cost_parameters]
        elif self.start_year == 2019 or self.start_year<2018:
            cost_parameter_variables = [cost_variable + str(int(2018)) for cost_variable in initial_stub_cost_parameters]
        elif 2020 < self.start_year < 2025:
            cost_parameter_variables = [cost_variable + str(int(2020)) for cost_variable in initial_stub_cost_parameters]

        else:
            raise ValueError("Construction year must be 2018 or higher to estimate parameters for modern plants.")
        return cost_parameter_variables

    def _extrapolate_interpolate_parameters(self, cost_var_wanted):
        """
        Function which extrapolates and interpolates from known data. Use of linear interpolation between known
        points, and last known data point for extrapolation.
        :param cost_var_wanted (str): Cost variable to be extrapolated/interpolated.
        :return (int): Returns extrapolated/interpolated cost of cost variable
        """
        variable_required = self.cost_data[['Plant_Size', cost_var_wanted]].dropna()

        if not variable_required.empty:
            if self.capacity <= min(variable_required.Plant_Size):
                return variable_required[cost_var_wanted].iloc[0]
            elif self.capacity >= max(variable_required.Plant_Size):
                return variable_required[cost_var_wanted].iloc[-1]

            else:
                interp = interp1d(variable_required.Plant_Size, variable_required[cost_var_wanted])
                return interp(self.capacity)
        else:
            return 0

    def _estimate_duration_parameters(self, variable_wanted):
        """
        Estimates parameters time scale required for construction, pre-development and operating period.
        This is done by selecting the operating period, construction and pre-development of the closest sized
        power plant in data
        :param variable_wanted (str): Variable that is required to estimate
        :return (int): Returns estimated duration parameter in years.
        """
        column_required = self.cost_data[['Plant_Size', variable_wanted]].dropna()
        if min(column_required.Plant_Size) <= self.capacity <= max(column_required.Plant_Size):
            interp = interp1d(column_required.Plant_Size, column_required[variable_wanted], kind='nearest')
            return interp(self.capacity)
        elif self.capacity > max(column_required.Plant_Size):
            column_required = column_required.reset_index()
            return column_required.iloc[-1][variable_wanted]
        elif self.capacity < min(column_required.Plant_Size):
            column_required = column_required.reset_index()
            return column_required.iloc[0][variable_wanted]

    def _closest_year_spread(self, var_wanted):
        """
        Function which selects the spread of payments required for construction and pre-development. This is achieved
        by selecting the power plant of the closest size.
        :param var_wanted (str): Variable to estimate spread of payments.
        :return (:obj:`list` of :obj:`str`): Returns list of percentage of cost per year
        """
        # df_sort = self.cost_data.iloc[(self.cost_data['Plant_Size']-self.capacity).abs().argsort()[:1]]
        df_sort = closest_row(self.cost_data, "Plant_Size", self.capacity)
        df_sort = df_sort.filter(regex=var_wanted).filter(regex='^((?!Dur).)*$').filter(regex='^((?!-).)*$').dropna(axis=1).values.tolist()[0]

        return df_sort

    def _change_columns(self, column):
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

