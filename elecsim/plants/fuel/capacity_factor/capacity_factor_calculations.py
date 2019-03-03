import functools
import logging

import pandas as pd

# from elecsim.scen_error.scenario_data import wind_capacity_factor, solar_capacity_factor, historical_hourly_demand, \
#     segment_demand, load_duration_curve_diff, hydro_capacity_factor
import elecsim.scenario.scenario_data

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


@functools.lru_cache(maxsize=512)
def get_capacity_factor(renewable_type, demand_hour):
        historical_demand = elecsim.scenario.scenario_data.historical_hourly_demand
        renewable_type = renewable_type.lower()
        capacity_data = get_capacity_data(renewable_type)
        if renewable_type in ['onshore', 'offshore', 'pv']:
            capacity_factor = segment_capacity_data_by_load_curve(capacity_data, historical_demand, renewable_type)
            capacity_factor_value = get_capacity_factor_value_for_segment(capacity_factor, demand_hour,
                                                                      renewable_type)
        else:
            capacity_factor_value = capacity_data
        return capacity_factor_value

def get_capacity_data(renewable_type):
    if renewable_type in ["onshore", 'offshore']:
        capacity_data = elecsim.scenario.scenario_data.wind_capacity_factor[['time', renewable_type]]
    elif renewable_type == "pv":
        capacity_data = elecsim.scenario.scenario_data.solar_capacity_factor
    elif renewable_type == 'hydro':
        capacity_data = elecsim.scenario.scenario_data.hydro_capacity_factor
    else:
        raise ValueError("Calculating demand factor can only be done for Onshore, Offshore or PV power generators.")
    return capacity_data

def segment_capacity_data_by_load_curve(capacity_data, historical_demand, renewable_type):
    demand_capacity = capacity_data.join(historical_demand, how='inner').dropna()
    demand_capacity = demand_capacity[elecsim.scenario.scenario_data.segment_demand[-1] < demand_capacity.demand]
    demand_capacity = demand_capacity[elecsim.scenario.scenario_data.segment_demand[0] > demand_capacity.demand]
    capacity_factor = demand_capacity.groupby(pd.cut(demand_capacity.demand, 20))[renewable_type].mean()
    capacity_factor = capacity_factor.to_frame()
    capacity_factor['diff'] = elecsim.scenario.scenario_data.load_duration_curve_diff['hours'].sort_values(ascending=False).values
    return capacity_factor

def get_capacity_factor_value_for_segment(capacity_factor, demand_hour, renewable_type):
    subsetted_dataframe = capacity_factor[capacity_factor['diff'] >= demand_hour].tail(1)
    capacity_factor_value = float(subsetted_dataframe[renewable_type].values)
    return capacity_factor_value







