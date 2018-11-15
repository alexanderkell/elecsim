
import pandas as pd
from elecsim.constants import ROOT_DIR

class LcoeToParameters:

    def __init__(self, start_date):

        self.start_date = start_date
        self.hist_costs = pd.read_csv(ROOT_DIR+"/data/Power_Plants/Power_Plant_Costs/historical_costs/historical_plant_costs_adjusted.csv")

    def breakdown_lcoe(self, fuel):
        technology = self.hist_costs[self.hist_costs['Technology']==fuel]
        print(technology.head())


LcoeToParameters(2011).breakdown_lcoe('CCGT')
