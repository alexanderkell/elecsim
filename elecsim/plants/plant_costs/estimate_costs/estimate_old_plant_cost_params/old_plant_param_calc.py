import pandas as pd

import elecsim.scenario.scenario_data
from elecsim.data_manipulation.data_modifications.extrapolation_interpolate import ExtrapolateInterpolate
from elecsim.plants.plant_costs.estimate_costs.estimate_modern_power_plant_costs.predict_modern_plant_costs import PredictModernPlantParameters
from elecsim.plants.plant_registry import PlantRegistry
# from elecsim.scen_error.scenario_data import modern_plant_costs


class OldPlantCosts:
    """
    Class which takes LCOE values and plant_type of power plants from retrospective database and predicts
    more detailed cost parameters using the same proportions as the BEIS Power Plant Cost Database.
    Specifically uses 2018 power plants from BEIS Power Plant Cost Database.
    """
    hist_costs = elecsim.scenario.scenario_data.power_plant_historical_costs_long

    def __init__(self, year, plant_type, capacity):

        # Import historical LCOE data for power plants, and use to predict LCOE for current year based on linear
        # interpolation
        self.year = year
        self.plant_type = plant_type
        self.capacity = capacity
        self.hist_costs = self.hist_costs[self.hist_costs['Technology'].map(lambda x: x in plant_type)].dropna()

        if not all(self.hist_costs.capacity_range.str.contains(">0")):
            self.hist_costs = self.hist_costs[[pd.eval(f"{self.capacity}{j}") for j in self.hist_costs['capacity_range']]]

        self.estimated_historical_lcoe = ExtrapolateInterpolate(self.hist_costs.Year, self.hist_costs.lcoe)(year)
        self.discount_rate = self.hist_costs.Discount_rate.iloc[0]

        self.modern_costs = elecsim.scenario.scenario_data.modern_plant_costs[elecsim.scenario.scenario_data.modern_plant_costs['Type'].map(lambda x: x in plant_type)]
        minimum_year = self.find_smallest_year_available()

        self.estimated_modern_plant_parameters = PredictModernPlantParameters(self.plant_type, self.capacity, minimum_year).parameter_estimation()

        plant_object = PlantRegistry(self.plant_type).plant_type_to_plant_object()

        self.plant = plant_object(name="Modern Plant", plant_type=self.plant_type,
                                                         capacity_mw=self.capacity, construction_year=self.year,
                                                         **self.estimated_modern_plant_parameters)
        self.modern_lcoe = self.plant.calculate_lcoe(self.discount_rate)
        self.lcoe_scaler = self.estimated_historical_lcoe / self.modern_lcoe

    def find_smallest_year_available(self):
        """
        Method which takes the modern cost BEIS database of power plants, and finds the earliest year
        that data for specified power plant type exists. For example, only returns data on Coal power plants from 2025
        as only this data is provided in the BEIS datafile
        :return: Int containing smallest year available.
        """
        # available_years = self.modern_costs[['Constr_cost-Medium _2018','Constr_cost-Medium _2020', 'Constr_cost-Medium _2025']]
        available_years = self.modern_costs.filter(regex="Constr_cost-Medium _")
        columns_with_no_nan = available_years[available_years.columns[~available_years.isnull().all()]].columns
        years_with_no_nan = [s for s in columns_with_no_nan]
        years_with_no_nan = [int(s.split("_")[2]) for s in years_with_no_nan]
        minimum_year_with_data = min(years_with_no_nan)

        return minimum_year_with_data

    def get_params_to_scale(self):
        self.params_to_ignore = ['pre_dev_period', 'operating_period', 'construction_period', 'efficiency',
                            'average_load_factor', 'construction_spend_years', 'pre_dev_spend_years']
        self.dict_to_ignore = {key: self.estimated_modern_plant_parameters[key] for key in
                          self.estimated_modern_plant_parameters
                          if key in self.params_to_ignore}

