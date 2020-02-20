from itertools import chain

"""
File name: multi_step_forecasting_wrangling
Date created: 20/02/2020
Feature: #Enter feature description here
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"


def get_lags(dat, value, col_prefix='value', lags=None):
    if lags == None:
        previous_three_hours = [1,2,3]
        previous_day = [24,25,26,27]
        previous_week = [168,169,170,171]
        lags = previous_three_hours + previous_day + previous_week
    else:
        lags = lags

    new_cols = dat.assign(**{f'{col_prefix}-{lag}': dat[value].shift(lag) for lag in lags})
    return new_cols


def get_hours_of_day(prev_day_needed, hours_needed=24):
    if prev_day_needed == 0:
        first_hour = 1
    else:
        first_hour = 0
    day = [hour + 24*prev_day_needed for hour in range(first_hour,hours_needed)]
    return day


def get_hours_of_days_needed(days_wanted=[1, 2, 7], hours_wanted=[12, 12, 12]):
    prev_days_needed = [get_hours_of_day(days, num_hours) for days, num_hours in zip(days_wanted, hours_wanted)]
    prev_days_needed = list(chain.from_iterable(prev_days_needed))
    return prev_days_needed


def multi_step_data_prep(dat, input_lags=[1, 2, 3], outputs=3):
    dat = dat.loc[:, ~dat.columns.str.contains('value-')]
    dat = get_lags(dat=dat, value='value', col_prefix="value", lags=range(1, outputs))
    dat = get_lags(dat=dat, value='value-{}'.format(outputs-1), col_prefix="n", lags=input_lags).dropna()
    return dat
