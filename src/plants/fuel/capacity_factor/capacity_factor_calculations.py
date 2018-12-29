from src.scenario.scenario_data import wind_capacity_factor, solar_capacity_factor, historical_hourly_demand, \
    segment_demand, load_duration_curve_diff
import logging
import pandas as pd

import functools

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


# class CapacityFactorCalculations:
#     def __init__(self, renewable_type):
#         self.historical_demand = historical_hourly_demand
#         self.renewable_type = renewable_type.lower()
#         if self.renewable_type in ["onshore", 'offshore']:
#             self.capacity_data = wind_capacity_factor[['time', self.renewable_type]]
#         elif self.renewable_type == "pv":
#             self.capacity_data = solar_capacity_factor
#         else:
#             raise ValueError("Calculating demand factor can only be done for Onshore, Offshore or PV power generators.")
#
    # def _calculate_demand_factors(self):
    #     demand_capacity = self.capacity_data.join(self.historical_demand, how='inner').dropna()
    #
    #     demand_capacity = demand_capacity[segment_demand[-1] < demand_capacity.demand]
    #     demand_capacity = demand_capacity[segment_demand[0] > demand_capacity.demand]
    #
    #     capacity_factor_by_demand = demand_capacity.groupby(pd.cut(demand_capacity.demand, 20))[
    #         self.renewable_type].mean()
    #
    #     return capacity_factor_by_demand

    # @functools.lru_cache(maxsize=128)
    # def get_capacity_factor(self, demand_value):
    #     capacity_factor =self._calculate_demand_factors()
    #     value = capacity_factor[[demand_value in index for index in capacity_factor.index]].values
    #     return value


@functools.lru_cache(maxsize=128)
def get_capacity_factor(renewable_type, demand_hour):
        historical_demand = historical_hourly_demand
        renewable_type = renewable_type.lower()
        capacity_data = get_capacity_data(renewable_type)

        capacity_factor = segment_capacity_data_by_load_curve(capacity_data, historical_demand, renewable_type)
        capacity_factor_value = get_capacity_factor_value_for_segment(capacity_factor, demand_hour,
                                                                      renewable_type)


        # logger.debug("cfv: {}".format(capacity_factor_value))
        return capacity_factor_value

def get_capacity_data(renewable_type):
    if renewable_type in ["onshore", 'offshore']:
        capacity_data = wind_capacity_factor[['time', renewable_type]]
    elif renewable_type == "pv":
        capacity_data = solar_capacity_factor
    else:
        raise ValueError("Calculating demand factor can only be done for Onshore, Offshore or PV power generators.")
    return capacity_data

def segment_capacity_data_by_load_curve(capacity_data, historical_demand, renewable_type):
    demand_capacity = capacity_data.join(historical_demand, how='inner').dropna()
    demand_capacity = demand_capacity[segment_demand[-1] < demand_capacity.demand]
    demand_capacity = demand_capacity[segment_demand[0] > demand_capacity.demand]
    capacity_factor = demand_capacity.groupby(pd.cut(demand_capacity.demand, 20))[
        renewable_type].mean()
    capacity_factor = capacity_factor.to_frame()
    capacity_factor['diff'] = load_duration_curve_diff['hours'].sort_values(ascending=False).values
    return capacity_factor

def get_capacity_factor_value_for_segment(capacity_factor, demand_hour, renewable_type):
    subsetted_dataframe = capacity_factor[capacity_factor['diff'] >= demand_hour].tail(1)
    capacity_factor_value = float(subsetted_dataframe[renewable_type].values)
    return capacity_factor_value







