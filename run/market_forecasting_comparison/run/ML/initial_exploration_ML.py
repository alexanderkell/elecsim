import os.path
import sys
from datetime import datetime
import pytz
from itertools import chain

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

# from run.market_forecasting_comparison.munging.multi_step_forecasting_wrangling import multi_step_data_prep, get_hours_of_days_needed
# from run.market_forecasting_comparison.ML.EstimatorSelectionHelper import EstimatorSelectionHelper

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
from sklearn.metrics import SCORERS
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
    'GradientBoostingRegressor': {'model__estimator__n_estimators': [16, 32], 'model__estimator__learning_rate': [0.8, 1.0]},
    'SVR': [
        {'model__estimator__kernel': ['linear'], 'model__estimator__C': [1, 10]},
        {'model__estimator__kernel': ['rbf'], 'model__estimator__C': [1, 10], 'model__estimator__gamma': [0.001, 0.0001]},
    ],
    'MLPRegressor': {"model__estimator__hidden_layer_sizes": [(1,), (50,)], "model__estimator__activation": ["tanh", "relu"], "model__estimator__solver": ["adam"], "model__estimator__alpha": [0.00005, 0.0005]},
    'KNeighborsRegressor': {'model__estimator__n_neighbors': [5, 20, 50]},
}

# params = {
#     'LinearRegression': {},
#     'Lasso': {},
#     'Ridge': {},
#     'ElasticNet': {},
#     'llars': {},
#     'ExtraTreesRegressor': {'model__estimator__n_estimators': [32]},
#     'RandomForestRegressor': {'model__estimator__n_estimators': [32]},
#     'AdaBoostRegressor':  {'model__estimator__n_estimators': [32]},
#     'GradientBoostingRegressor': {'model__estimator__n_estimators': [32], 'model__estimator__learning_rate': [0.8]},
#     'SVR': [
#         # {'model__estimator__kernel': ['linear'], 'model__estimator__C': [10]},
#         {'model__estimator__kernel': ['rbf'], 'model__estimator__C': [10], 'model__estimator__gamma': [0.001]},
#     ],
#     'MLPRegressor': {"model__estimator__hidden_layer_sizes": [(1,), (50,)], "model__estimator__activation": ["tanh", "relu"], "model__estimator__solver": ["adam"], "model__estimator__alpha": [0.0005]},
#     'KNeighborsRegressor': {'model__estimator__n_neighbors': [20]},
# }



import pandas as pd
import numpy as np
import ray

from sklearn.model_selection import GridSearchCV

from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline

from sklearn.multioutput import MultiOutputRegressor
from sklearn.model_selection import TimeSeriesSplit


"""
File name: EstimatorSelectionHelper
Date created: 20/02/2020
Feature: #Enter feature description here
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"


class EstimatorSelectionHelper:

    def __init__(self, models, params, scoring=None):
        if not set(models.keys()).issubset(set(params.keys())):
            missing_params = list(set(models.keys()) - set(params.keys()))
            raise ValueError("Some estimators are missing parameters: %s" % missing_params)
        self.models = models
        self.params = params
        self.keys = models.keys()
        self.grid_searches = {}
        self.scoring = scoring

    def fit(self, X, y, cv=3, n_jobs=3, verbose=1, refit=True):
        for key in self.keys:
            print("Running GridSearchCV for %s." % key)
            model = MultiOutputRegressor(self.models[key])

            pipeline = self.make_pipeline(model)
            params = self.params[key]
            tscv = TimeSeriesSplit(n_splits=cv, max_train_size=60)

            gs = GridSearchCV(pipeline, params, cv=tscv, n_jobs=n_jobs,
                              verbose=verbose, scoring=self.scoring, refit=refit,
                              return_train_score=True)
            gs.fit(X, y)
            self.grid_searches[key] = gs

    def fit_parallel(self, X, y, cv=3, n_jobs=3, verbose=1, refit=True, scoring=None):

        ray.init(
            # address="auto",  # or "<hostname>:<port>" if not using the default port
            # driver_object_store_memory=2 * 100000 * 1024 * 1024
        )
        list_of_keys = []
        output = []
        for key in self.keys:
            print("Running GridSearchCV for %s." % key)

            gs = run_model.remote(self.params[key], self.models[key], scoring, X, y, cv, n_jobs, verbose, refit)
            list_of_keys.append(key)
            output.append(gs)

        output = ray.get(output)
        self.grid_searches = {key: out for key, out in zip(list_of_keys, output)}

    def score_summary(self):
        all_results = []
        for k in self.grid_searches:
            try:
                results = pd.DataFrame(self.grid_searches[k].cv_results_)
                results['estimator'] = k
                all_results.append(results)
            except Exception as e:
                print(e)

        results_df = pd.concat(all_results)
        results_df = results_df.loc[:,~results_df.columns.str.contains('train')]

        return results_df

def make_pipeline(model):
    steps = list()
    steps.append(('standardize', StandardScaler()))
    steps.append(('normalize', MinMaxScaler()))
    steps.append(('model', model))
    # create pipeline
    pipeline = Pipeline(steps=steps)
    return pipeline


@ray.remote(num_return_vals=1)
def run_model(param, model, scoring, X, y, cv=3, n_jobs=3, verbose=1, refit=True):
    multi_model = MultiOutputRegressor(model)

    pipeline = make_pipeline(multi_model)
    params = param
    tscv = TimeSeriesSplit(n_splits=cv)

    gs = GridSearchCV(pipeline, params, cv=tscv, n_jobs=n_jobs,
                      verbose=verbose, scoring=scoring, refit=refit,
                      return_train_score=True)
    gs.fit(X, y)

    return gs

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
    day = [hour + 24*prev_day_needed for hour in range(first_hour, hours_needed)]
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

    prev_days_needed = get_hours_of_days_needed(days_wanted=[1, 2, 7, 30], hours_wanted=[28, 28, 28, 28, 28])
    multi_step_dat = multi_step_data_prep(dat=demand, input_lags=prev_days_needed, outputs=24)

    y = multi_step_dat.filter(like='value').values
    X = multi_step_dat.filter(regex='^(?!.*value).*$').values.astype(np.float32)

    print(sorted(SCORERS.keys()))
    scoring_params = ['neg_mean_absolute_error', 'neg_mean_squared_error', 'r2']

    helper1 = EstimatorSelectionHelper(models, params, scoring=scoring_params)
    # helper1.fit(X, y, n_jobs=-1, cv=5, refit=False)

    helper1.fit_parallel(X, y, scoring=scoring_params, n_jobs=-1, cv=20, refit=False, verbose=1)





    res = helper1.score_summary()

    timezone = pytz.timezone("Europe/London")

    res.to_csv('{}/../data/results/demand_initial_exploration-{}.csv'.format(ROOT_DIR, datetime.now(tz=timezone)))
