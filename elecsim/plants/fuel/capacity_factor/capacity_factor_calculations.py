import functools
import logging
# from linetimer import CodeTimer
import numpy as np
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


@functools.lru_cache(maxsize=1024)
def get_capacity_factor(market_time_splices, renewable_type, demand_hour):
    renewable_type = renewable_type.lower()
    if market_time_splices == 1:
        historical_demand = elecsim.scenario.scenario_data.historical_hourly_demand
        capacity_data = get_capacity_data(renewable_type)
    elif market_time_splices > 1:
        historical_demand = elecsim.scenario.scenario_data.historical_hourly_demand
        capacity_data = get_multiple_capacity_data(renewable_type)
    else:
        raise ValueError("market_time_slices must be bigger than 1")
    if renewable_type in ['onshore', 'offshore', 'pv']:
        if market_time_splices == 1:
            capacity_factor = segment_capacity_data_by_load_curve(renewable_type, market_time_splices)
            capacity_factor_value = get_capacity_factor_value_for_segment(capacity_factor, demand_hour, renewable_type)
        else:
            # capacity_factor = segment_multiple_capacity_data_by_load_curve(capacity_data, historical_demand, model)
            capacity_factor_value = get_multi_capacity_factor_value_for_segment(renewable_type, demand_hour)
    else:
        capacity_factor_value = capacity_data
    return capacity_factor_value


def get_multiple_capacity_data(renewable_type):
    capacity_factor_data = elecsim.scenario.scenario_data.multi_year_data_scaled
    if renewable_type in ["onshore", 'offshore']:
        capacity_data = capacity_factor_data[capacity_factor_data.data_type == renewable_type]
    elif renewable_type == "pv":
        capacity_data = capacity_factor_data[capacity_factor_data.data_type == 'solar']
    elif renewable_type == 'hydro':
        capacity_data = elecsim.scenario.scenario_data.hydro_capacity_factor
    elif renewable_type == "nuclear":
        capacity_data = elecsim.scenario.scenario_data.nuclear_capacity_factor
    else:
        # raise ValueError("Calculating demand factor can only be done for Onshore, Offshore or PV power generators.")
        capacity_data = 1
    return capacity_data


def get_capacity_data(renewable_type):
    if renewable_type in ["onshore", 'offshore']:
        capacity_data = elecsim.scenario.scenario_data.wind_capacity_factor[['time', renewable_type]]
    elif renewable_type == "pv":
        capacity_data = elecsim.scenario.scenario_data.solar_capacity_factor
    elif renewable_type == 'hydro':
        capacity_data = elecsim.scenario.scenario_data.hydro_capacity_factor
    elif renewable_type == "nuclear":
        capacity_data = elecsim.scenario.scenario_data.nuclear_capacity_factor
    else:
        raise ValueError("Calculating demand factor can only be done for Onshore, Offshore or PV power generators.")
    return capacity_data


@functools.lru_cache(maxsize=512)
def segment_capacity_data_by_load_curve(renewable_type, market_time_splices):
    historical_demand = elecsim.scenario.scenario_data.historical_hourly_demand
    capacity_data = get_capacity_data(renewable_type)

    demand_capacity = capacity_data.join(historical_demand, how='inner').dropna()
    demand_capacity = demand_capacity[elecsim.scenario.scenario_data.segment_demand[-1] < demand_capacity.demand]
    demand_capacity = demand_capacity[elecsim.scenario.scenario_data.segment_demand[0] > demand_capacity.demand]
    cut_demand = pd.cut(demand_capacity.demand, 20* market_time_splices)
    capacity_factor_grouped = demand_capacity.groupby(cut_demand)[renewable_type]
    capacity_factor = capacity_factor_grouped.apply(np.mean)
    capacity_factor = capacity_factor.to_frame()
    capacity_factor['diff'] = elecsim.scenario.scenario_data.load_duration_curve_diff['hours'].sort_values(ascending=False).values
    return capacity_factor


def get_capacity_factor_value_for_segment(capacity_factor, demand_hour, renewable_type):
    subsetted_dataframe = capacity_factor[capacity_factor['diff'] >= demand_hour].tail(1)
    capacity_factor_value = float(subsetted_dataframe[renewable_type].values)
    return capacity_factor_value


def get_multi_capacity_factor_value_for_segment(renewable_type, demand_hour):
    capacity_factor = get_multiple_capacity_data(renewable_type)

    capacity_factor_value = capacity_factor[capacity_factor['demand_hour'] >= demand_hour].capacity_factor.head(1)
    capacity_factor_value = capacity_factor_value.values[0]

    # subsetted_dataframe = capacity_factor[capacity_factor['diff'] >= demand_hour].tail(1)
    # capacity_factor_value = float(subsetted_dataframe['capacity_factor'].values)
    # capacity_factor_value = subsetted_dataframe['capacity_factor'].values.astype(float)
    return capacity_factor_value


def get_capacity_factor_for_year(renewable_type):
    if renewable_type == "pv":
        renewable_type = "solar"
    capacity_factor_dat = elecsim.scenario.scenario_data.multi_year_data
    capacity_factor = multi_year_data_to_ldc(capacity_factor_dat, renewable_type)

    year_segment_capacity_factor = (pd.DataFrame(pd.cut(capacity_factor.capacity_factor, 20).apply(lambda x: x.right)).groupby("capacity_factor").first()).index.tolist()
    year_segment_hours = (pd.DataFrame(pd.cut(capacity_factor.hour, 20).apply(lambda x: x.right)).groupby("hour").first()).index.tolist()

    return year_segment_hours, year_segment_capacity_factor


def multi_year_data_to_ldc(capacity_factor_dat, renewable_type):
    renewable_capacity_factor = capacity_factor_dat[capacity_factor_dat.data_type == renewable_type]
    capacity_factor = renewable_capacity_factor.sort_values("capacity_factor", ascending=False)
    capacity_factor['hour'] = capacity_factor.counts.cumsum()
    return capacity_factor


functools.lru_cache(maxsize=512)
def segment_multiple_capacity_data_by_load_curve(capacity_data, historical_demand, model):

    demand_capacity = capacity_data.join(historical_demand, how='inner').dropna()
    demand_capacity = demand_capacity[model.demand.segment_consumption[-1] < demand_capacity.demand]
    demand_capacity = demand_capacity[model.demand.segment_consumption[0] > demand_capacity.demand]
    cut_demand = pd.cut(demand_capacity.demand, 20 * model.market_time_splices)
    capacity_factor_grouped = demand_capacity.groupby(cut_demand)['capacity_factor']
    capacity_factor = capacity_factor_grouped.apply(np.mean)
    capacity_factor = capacity_factor.to_frame().fillna(0)

    capacity_factor['diff'] = np.linspace(0.083, 8752.5, 20 * model.market_time_splices)

    # capacity_factor['diff'] = capacity_factor.reset_index()['demand'].apply(lambda x: x.left).astype(float).values
    # capacity_factor = capacity_factor.reset_index()
    # capacity_factor['diff'] = elecsim.scenario.scenario_data.load_duration_curve_diff['hours'].sort_values(ascending=False).values

    # capacity_factor_dat = elecsim.scenario.scenario_data.multi_year_data
    # load_factor = multi_year_data_to_ldc(capacity_factor_dat, 'load')
    #
    # capacity_factor['diff'] = pd.cut(load_factor['hour'], 20 * model.market_time_splices).sort_values(ascending=False).values
    return capacity_factor

