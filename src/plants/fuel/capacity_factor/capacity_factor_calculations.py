from src.scenario.scenario_data import wind_capacity_factor, solar_capacity_factor, historical_hourly_demand, segment_demand
import logging
import pandas as pd
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)
"""
File name: solar_capacity_factor
Date created: 27/12/2018
Feature: # Calculates the average capacity factor per demand segment
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"


class DemandFactor():

    def __init__(self, renewable_type):
        self.historical_demand = historical_hourly_demand
        self.renewable_type = renewable_type.lower()
        if self.renewable_type in ["onshore", 'offshore']:
            self.capacity_data = wind_capacity_factor[['time',self.renewable_type]]
        elif self.renewable_type == "pv":
            self.capacity_data = solar_capacity_factor
        else:
            raise ValueError("Calculating demand factor can only be done for Onshore, Offshore or PV power generators.")

    def calculate_demand_factor_for_segment(self):
        demand_capacity = self.capacity_data.join(self.historical_demand, how='inner').dropna()

        demand_capacity = demand_capacity[segment_demand[-1] < demand_capacity.demand]
        demand_capacity = demand_capacity[segment_demand[0] > demand_capacity.demand]

        capacity_factor_by_demand = demand_capacity.groupby(pd.cut(demand_capacity.demand, 20))[self.renewable_type].mean()
        logger.debug(capacity_factor_by_demand)
        return capacity_factor_by_demand
