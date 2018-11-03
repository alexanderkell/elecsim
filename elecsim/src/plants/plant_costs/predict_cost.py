from scipy.interpolate import interp1d
import pandas as pd
import elecsim.src.scenario.scenario_data as scenario
pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 500)


class PredictPlantStatistics:

    def __init__(self, fuel, capacity, start_year):
        """
        Class which provides calculations to provide costing data for power plants based on fuel, capacity and start year
        :param fuel (str): Type of fuel that plant runs on
        :param capacity (int): Capacity of plant in MW
        :param start_year (int): Year that power plant begun construction
        """
        self.fuel = fuel
        self.capacity = float(capacity)
        self.start_year = float(start_year)

        # Import UK power plant cost data
        self.cost_data = scenario.power_plant_costs
        self.cost_data = self.cost_data[self.cost_data.Type == self.fuel].sort_values('Plant_Size')

        # print(self.cost_data)

    def __call__(self):
        """
        Function which estimates costs of power plant based on capacity, fuel and start year. Use of linear interpolation
        for plants of capacity that fall within known range of costing variables. If plant capacity to be calculated
        falls out of range of known values, the highest or lowest capacity value is chosen.
        :return (:obj:`dict`:obj:`str`): Returns dictionary containing variables for PowerPlant cost
        """

        # Iterates through each type of plant cost to predict parameters.
        plant_costs = ['Connect_system_cost-Medium _', 'Constr_cost-Medium _', 'Fixed_cost-Medium _',
                       'Infra_cost-Medium _', 'Insurance_cost-Medium _', 'Pre_dev_cost-Medium _',
                       'Var_cost-Medium _']


        # Functionality that selects data from UK plant costing data based on year of plant construction.
        # If power plant is built in year 2018, 2020 or 2025 then use provided data. If plant is not built on these dates
        # then use last known data point.
        if self.start_year in (2018, 2020, 2025):
            plant_costs = [cost_variable+str(int(self.start_year)) for cost_variable in plant_costs]
        elif self.start_year < 2018:
            plant_costs = [cost_variable+str(int(2018)) for cost_variable in plant_costs]
        elif self.start_year > 2025:
            plant_costs = [cost_variable+str(int(2025)) for cost_variable in plant_costs]
        elif self.start_year == 2019:
            plant_costs = [cost_variable+str(int(2018)) for cost_variable in plant_costs]
        elif 2020 < self.start_year < 2025:
            plant_costs = [cost_variable+str(int(2020)) for cost_variable in plant_costs]

        # print("start year: ", self.start_year)
        # print("fuel: ", self.fuel)
        # print("plant costs: ", plant_costs)

        parameters_of_plant = {self._change_columns(cost_var): self._extrap_interp_parameters(cost_var) for cost_var in plant_costs}
        durations = ['Pre_Dur', 'Operating_Period', 'Constr_Dur']
        durations_parameters = {self._change_columns(dur): self._estimate_duration_parameters(dur) for dur in durations}

        yearly_cost_spread = ['Constr', 'Pre']

        yearly_cost_perc = {self._change_columns(spread): self._closest_year_spread(spread) for spread in yearly_cost_spread}

        parameters={**parameters_of_plant, **durations_parameters, **yearly_cost_perc}

        return parameters


    def _estimate_duration_parameters(self, var_wanted):
        """
        Estimates parameters time scale required for construction, pre-development and operating period.
        This is done by selecting the operating period, construction and pre-development of the closest sized
        power plant in data
        :param var_wanted (str): Variable that is required to estimate
        :return (int): Returns estimated duration parameter in years.
        """
        var_req = self.cost_data[['Plant_Size',var_wanted]].dropna()
        if min(var_req.Plant_Size) < self.capacity < max(var_req.Plant_Size):
            interp = interp1d(var_req.Plant_Size, var_req[var_wanted], kind='nearest')
            return interp(self.capacity)
        elif self.capacity > max(var_req.Plant_Size):
            var_req = var_req.reset_index()

        elif self.capacity < min(var_req.Plant_Size):
            var_req = var_req.reset_index()

    def _closest_year_spread(self, var_wanted):
        """
        Function which selects the spread of payments required for construction and pre-development. This is achieved
        by selecting the power plant of the closest size.
        :param var_wanted (str): Variable to estimate spread of payments.
        :return (:obj:`list` of :obj:`str`): Returns list of percentage of cost per year
        """
        df_sort = self.cost_data.iloc[(self.cost_data['Plant_Size']-self.capacity).abs().argsort()[:1]]
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
            return 'connection_cost_per_kw'
        elif 'Constr_cost' in column:
            return 'construction_cost_per_kw'
        elif 'Fixed_cost' in column:
            return 'fixed_o_and_m_per_mw'
        elif 'Infra_cost' in column:
            return 'infrastructure'
        elif 'Insurance_cost' in column:
            return 'insurance_cost_per_kw'
        elif 'Pre_dev_cost' in column:
            return 'pre_dev_cost_per_kw'
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
        else:
            raise ValueError('Plant cost data not found')

pps = PredictPlantStatistics("CCGT", 10, 2018)
pps()
