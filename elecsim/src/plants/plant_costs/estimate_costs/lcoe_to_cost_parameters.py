import pandas as pd
from elecsim.src.plants.plant_costs.estimate_costs.cost_estimations import ExtrapolateInterpolate
import elecsim.src.scenario.scenario_data as scenario

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 500)

class LcoeToParameters:
    hist_costs = scenario.power_plant_historical_costs

    def __init__(self, technology, year):
        """
        Class which takes a technology and estimates detailed costing information
        :param technology: type of technology for costing information to be estimated
        """
        self.technology = technology
        self.year = year

        hist_costs = self.hist_costs[self.hist_costs.Technology == technology].dropna()
        print(hist_costs)

        # Uses linear interpolation and extrapolation of historical dataset to predict unknown LCOE costs of a power plant
        self.lcoe = ExtrapolateInterpolate(hist_costs.Year, hist_costs.lcoe)(year)

    def lcoe_to_parameters(self, plant_size):
        pp_cost = scenario.power_plant_costs
        pp_cost = pp_cost[pp_cost['Type'] == self.technology]
        print(pp_cost.head())


print(LcoeToParameters('Coal', 2017).lcoe_to_parameters())
