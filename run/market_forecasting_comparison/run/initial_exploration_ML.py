import os.path
import sys
from datetime import datetime
import pytz

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from run.market_forecasting_comparison.munging.multi_step_forecasting_wrangling import multi_step_data_prep, get_hours_of_days_needed
from run.market_forecasting_comparison.ML.EstimatorSelectionHelper import EstimatorSelectionHelper

import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.linear_model import Ridge
from sklearn.linear_model import ElasticNet
from sklearn.linear_model import LassoLars
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.svm import SVR

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
    'LinearRegression': LinearRegression(),
    'Lasso': Lasso(),
    'Ridge': Ridge(),
    'ElasticNet': ElasticNet(),
    'llars': LassoLars(),
    'ExtraTreesRegressor': ExtraTreesRegressor(),
    'RandomForestRegressor': RandomForestRegressor(),
    'AdaBoostRegressor': AdaBoostRegressor(),
    'GradientBoostingRegressor': GradientBoostingRegressor(),
    'SVR': SVR(),
    "MLPRegressor": MLPRegressor(),
    'KNeighborsRegressor': KNeighborsRegressor()
}

params = {
    'LinearRegression': {},
    'Lasso': {},
    'Ridge': {},
    'ElasticNet': {},
    'llars': {},
    'ExtraTreesRegressor': {'model__estimator__n_estimators': [16, 32]},
    'RandomForestRegressor': {'model__estimator__n_estimators': [16, 32]},
    'AdaBoostRegressor':  {'model__estimator__n_estimators': [16, 32]},
    'GradientBoostingRegressor': {'model__estimator__n_estimators': [16, 32], 'model__estimator__learning_rate': [0.8, 1.0] },
    'SVR': [
        {'model__estimator__kernel': ['linear'], 'model__estimator__C': [1, 10]},
        {'model__estimator__kernel': ['rbf'], 'model__estimator__C': [1, 10], 'model__estimator__gamma': [0.001, 0.0001]},
    ],
    'MLPRegressor': {"model__estimator__hidden_layer_sizes": [(1,), (50,)], "model__estimator__activation": ["tanh", "relu"], "model__estimator__solver": ["adam"], "model__estimator__alpha": [0.00005, 0.0005]},
    'KNeighborsRegressor': {'model__estimator__n_neighbors': [5, 20, 50]},
}


if __name__ == "__main__":

    # "{}/../run/beis_case_study/scenario/reference_scenario_2018.py".format(ROOT_DIR)

    demand = pd.read_csv('{}/../data/capacity/demand.csv'.format(ROOT_DIR))
    # solar = pd.read_csv('{}/../run/market_forecasting_comparison/data/capacity/solar.csv'.format(ROOT_DIR))
    # offshore = pd.read_csv('{}/../run/market_forecasting_comparison/data/capacity/offshore.csv'.format(ROOT_DIR))
    # onshore = pd.read_csv('{}/../run/market_forecasting_comparison/data/capacity/onshore.csv'.format(ROOT_DIR))

    demand = demand[demand.time < "2018"]

    demand = demand.drop(columns=['time', 'Unnamed: 0'])
    # solar = solar.drop(columns=['time','Unnamed: 0'])
    # onshore = onshore.drop(columns=['time','Unnamed: 0'])
    # offshore = offshore.drop(columns=['time','Unnamed: 0'])

    prev_days_needed = get_hours_of_days_needed(days_wanted=[1, 2, 3, 7, 30], hours_wanted=[36, 36, 36, 36, 36])
    multi_step_dat = multi_step_data_prep(dat=demand, input_lags=prev_days_needed, outputs=24)

    y = multi_step_dat.filter(like='value').values
    X = multi_step_dat.filter(regex='^(?!.*value).*$').values.astype(np.float32)

    helper1 = EstimatorSelectionHelper(models, params, scoring=['neg_mean_absolute_error', 'neg_mean_squared_error', 'r2'])
    helper1.fit(X, y, n_jobs=-1, cv=5, refit=False)

    res = helper1.score_summary()

    timezone = pytz.timezone("Europe/London")

    res.to_csv('{}/../data/results/demand_initial_exploration-{}.csv'.format(ROOT_DIR, datetime.now(tz=timezone)))
