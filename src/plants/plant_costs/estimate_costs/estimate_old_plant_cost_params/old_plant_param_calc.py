import src.scenario.scenario_data as scenario
from src.plants.plant_costs.estimate_costs.predict_modern_plant_costs import PredictPlantStatistics
from plants.plant_type.plant_registry import plant_type_to_if_fuel, plant_registry
from src.scenario.scenario_data import power_plant_costs

from src.data_manipulation.data_modifications.extrapolation_interpolate import ExtrapolateInterpolate


class OldPlantCosts:
    """
    Class which takes LCOE values and type of power plants from retrospective database and predicts
    more detailed cost parameters using the same proportions as the BEIS Power Plant Cost Database.
    Specifically uses 2018 power plants from BEIS Power Plant Cost Database.
    """
    hist_costs = scenario.power_plant_historical_costs

    def __init__(self, year, plant_type, capacity, discount_rate):

        # Import historical LCOE data for power plants, and use to predict LCOE for current year based on linear
        # interpolation

        self.year = year
        self.plant_type = plant_type
        self.capacity = capacity
        self.discount_rate = discount_rate

        self.hist_costs = self.hist_costs[self.hist_costs.Technology == plant_type].dropna()
        self.lcoe = ExtrapolateInterpolate(self.hist_costs.Year, self.hist_costs.lcoe)(year)

        self.modern_costs = power_plant_costs
        does_plant_use_fuel = plant_type_to_if_fuel(self.plant_type)

        min_year = self.find_smallest_year_available()

        self.predicted_modern_cost_parameters = PredictPlantStatistics(self.plant_type, self.capacity, min_year)()
        self.plant = plant_registry(does_plant_use_fuel)(name="Modern Plant", plant_type=self.plant_type,
                                                         capacity_mw=self.capacity, construction_year=min_year,
                                                         **self.predicted_modern_cost_parameters)

        self.modern_lcoe = self.plant.calculate_lcoe(self.discount_rate)
        self.lcoe_scaler = self.lcoe/self.modern_lcoe

        print("LCOE Scale")
        print(self.lcoe_scaler)

    def find_smallest_year_available(self):
        """
        Method which takes the modern cost BEIS database of power plants, and finds the earliest year
        that data for specified power plant type exists. For example, only returns data on Coal power plants from 2025
        as only this data is provided in the BEIS databais
        :return: Int containing smallest year available.
        """
        available_years = self.modern_costs[self.modern_costs.Type == self.plant_type][['Constr_cost-Medium _2018','Constr_cost-Medium _2020', 'Constr_cost-Medium _2025']]
        columns_with_no_nan = available_years[available_years.columns[~available_years.isnull().all()]].columns
        years_with_no_nan = [s for s in columns_with_no_nan]
        years_with_no_nan = [int(s.split("_")[2]) for s in years_with_no_nan]
        minimum_year_with_data = min(years_with_no_nan)

        return minimum_year_with_data

# OldPlantCosts(2017,"CCGT", 1200, 0.035).estimate_cost_parameters()
