
import pytz
import os.path
import sys
from datetime import date, datetime, timedelta
sys.path.append(os.path.join(os.path.dirname(os.path.realpath('__file__')), '../../..'))
ROOT_DIR = os.path.join(os.path.dirname(os.path.realpath('__file__')), '')

from run.market_forecasting_comparison.munging.multi_step_forecasting_wrangling import multi_step_data_prep, get_hours_of_days_needed
# from run.market_forecasting_comparison.ML.EstimatorSelectionHelper import EstimatorSelectionHelper

import numpy as np

import pickle
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from run.market_forecasting_comparison.munging.multi_step_forecasting_wrangling import multi_step_data_prep, get_hours_of_days_needed
from run.market_forecasting_comparison.ML.EstimatorSelectionHelperCreme import EstimatorSelectionHelperCreme
import pickle
import pandas as pd
import numpy as np

from creme import linear_model
from creme import meta
from creme import neighbors
from sklearn import neural_network

from creme import compat
from creme import model_selection
from sklearn.model_selection import ParameterGrid
from itertools import product

# from elecsim.constants import ROOT_DIR
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

"""
File name: initial_exploration_ML
Date created: 20/02/2020
Feature: #Enter feature description here
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"


models = {
    'PassiveAggressiveRegressor': linear_model.PARegressor(),
    'LinearRegression': linear_model.LinearRegression(),
    'BoxCoxRegressor': meta.BoxCoxRegressor(regressor=linear_model.LinearRegression(intercept_lr=0.2)),
#     'KNeighborsRegressor': neighbors.KNeighborsRegressor(),
    'SoftmaxRegression': linear_model.SoftmaxRegression(),
    'MLPRegressor': compat.convert_sklearn_to_creme(neural_network.MLPRegressor()),
}

# params = {
#     'PassiveAggressiveRegressor': {'C': [0.1, 1, 2], "fit_intercept": [True, False], "max_iter": [1, 10, 100, 1000], "shuffle": [False], 'tol': [0.001]},
#     'LinearRegression': {},
#     'BoxCoxRegressor': {'power': [0.1, 0.05, 0.01]},
# #     'KNeighborsRegressor': {},
#     'SoftmaxRegression': {},
#     'MLPRegressor': {
#         "solver": ['adam'],
#         'learning_rate': ['constant', 'adaptive'],
#         'hidden_layer_sizes': {(10,50,100), (10), (20),(50), (10,50)},
#     },
# }

params = {
    'PassiveAggressiveRegressor': {'C': [0.1, 2], "fit_intercept": [True, False], "max_iter": [1, 1000], "shuffle": [False], 'tol': [0.001]},
    'LinearRegression': {},
    'BoxCoxRegressor': {'power': [0.1]},
#     'KNeighborsRegressor': {},
    'SoftmaxRegression': {},
    'MLPRegressor': {
        "solver": ['adam'],
        'learning_rate': ['adaptive'],
        'hidden_layer_sizes': {(10)},
    },
}





Y = 2000 # dummy leap year to allow input X-02-29 (leap day)
seasons = [('1', (date(Y,  4,  1),  date(Y,  4, 26))),
           ('2', (date(Y,  4, 27),  date(Y,  8, 16))),
           ('3', (date(Y,  8, 17),  date(Y,  9, 20))),
           ('4', (date(Y,  9, 21),  date(Y, 10, 25))),
           ('5', (date(Y,  10, 26),  date(Y, 12, 31))),
           ('6', (date(Y, 1, 1),  date(Y, 1, 24))),
           ('7', (date(Y, 1, 25),  date(Y, 3, 31)))]

def get_season(now):
    if isinstance(now, datetime):
        now = now.date()
    now = now.replace(year=Y)
    return next(season for season, (start, end) in seasons
                if start <= now <= end)

def working_day_check(date):
    if date.holiday == True or date.dayofweek == 6:
        return "non_working_day"
    elif date.dayofweek in [0,1,2,3,4,5]:
        return "working_day"
    else:
        print("error")


if __name__ == "__main__":

    # "{}/../run/beis_case_study/scenario/reference_scenario_2018.py".format(ROOT_DIR)

    demand = pd.read_csv('{}/../../data/capacity/demand.csv'.format(ROOT_DIR))
    # solar = pd.read_csv('{}/../run/market_forecasting_comparison/data/capacity/solar.csv'.format(ROOT_DIR))
    # offshore = pd.read_csv('{}/../run/market_forecasting_comparison/data/capacity/offshore.csv'.format(ROOT_DIR))
    # onshore = pd.read_csv('{}/../run/market_forecasting_comparison/data/capacity/onshore.csv'.format(ROOT_DIR))

    demand = demand[demand.time < "2018"]

    demand = demand.drop(columns=['time', 'Unnamed: 0'])
    # solar = solar.drop(columns=['time','Unnamed: 0'])
    # onshore = onshore.drop(columns=['time','Unnamed: 0'])
    # offshore = offshore.drop(columns=['time','Unnamed: 0'])

    # prev_days_needed = get_hours_of_days_needed(days_wanted=[1, 2, 7, 30], hours_wanted=[28, 28, 28, 28, 28])
    # multi_step_dat = multi_step_data_prep(dat=demand, input_lags=prev_days_needed, outputs=24)



    demand = pd.read_csv('{}/../../data/capacity/demand.csv'.format(ROOT_DIR))

    demand = demand[demand.time < '2018']

    prev_days_needed = get_hours_of_days_needed(days_wanted=[1, 2, 7, 30], hours_wanted=[28, 28, 28, 28, 28])
    multi_step_dat = multi_step_data_prep(dat=demand, input_lags=prev_days_needed, outputs=24)
    multi_step_dat.time = pd.to_datetime(multi_step_dat.time)
    multi_step_dat['season'] = multi_step_dat.time.map(lambda x: get_season(x))

    multi_step_dat['working_day'] = multi_step_dat.apply(lambda x: working_day_check(x), axis=1)

    multi_step_dat = multi_step_dat.drop(columns=['Unnamed: 0'])

    # multi_step_dat





    # multi_step_dat = multi_step_dat[(multi_step_dat.time > "2016-11-28")  & (multi_step_dat.time < "2017-01-10")]


    estimator = EstimatorSelectionHelperCreme(models, params, cv=20)
    estimator.fit_parallel(multi_step_dat)

    estimator.grid_searches

    timezone = pytz.timezone("Europe/London")
    with open('{}/../../data/results/demand_initial_exploration-{}.csv'.format(ROOT_DIR, datetime.now(tz=timezone)), 'wb') as handle:
        pickle.dump(estimator.grid_searches, handle, protocol=pickle.HIGHEST_PROTOCOL)
        # res.to_csv('{}/../data/results/demand_initial_exploration-{}.csv'.format(ROOT_DIR, datetime.now(tz=timezone)))





