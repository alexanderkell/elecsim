
import pytz
import os.path
import sys
from datetime import date, datetime, timedelta
sys.path.append(os.path.join(os.path.dirname(os.path.realpath('__file__')), '../../../..'))
ROOT_DIR = os.path.join(os.path.dirname(os.path.realpath('__file__')), '')
sys.path.append(ROOT_DIR)
print(sys.path)

# from run.market_forecasting_comparison.munging.multi_step_forecasting_wrangling import multi_step_data_prep, get_hours_of_days_needed
# from run.market_forecasting_comparison.ML.EstimatorSelectionHelper import EstimatorSelectionHelper

import numpy as np

import pickle
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

# from run.market_forecasting_comparison.munging.multi_step_forecasting_wrangling import multi_step_data_prep, get_hours_of_days_needed
# from run.market_forecasting_comparison.ML.EstimatorSelectionHelperCreme import EstimatorSelectionHelperCreme
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

from creme import linear_model
from creme import meta
from creme import neighbors
from sklearn import neural_network
from joblib import Parallel, delayed
from creme import compat
from creme import model_selection
from sklearn.model_selection import ParameterGrid
from itertools import product
import json
import ray
from sklearn.model_selection import ParameterGrid
from creme import linear_model
from creme import metrics
from creme import model_selection
from creme import multioutput
from creme import preprocessing
from creme import stream
from creme import base
from creme import ensemble
from creme import optim
import time

import numpy as np
import pandas as pd
from tqdm import tqdm
import multiprocessing
from joblib import Parallel, delayed
# from sklearn import metrics

"""
File name: EstimatorSelectionHelperCreme
Date created: 04/04/2020
Feature: #Enter feature description here
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"


class EstimatorSelectionHelperCreme:

    def __init__(self, models, params, cv=2):
        if not set(models.keys()).issubset(set(params.keys())):
            missing_params = list(set(models.keys()) - set(params.keys()))
            raise ValueError("Some estimators are missing parameters: %s" % missing_params)
        self.models = models
        self.params = params
        self.cv = cv
        self.keys = models.keys()
        self.grid_searches = {}
        self.model_results = {}

    def fit(self, dat):
        for key in self.keys:
            print("Running {}".format(key))
            grid_searches = {}
            param_grid = list(ParameterGrid(self.params[key]))
            for params in param_grid:
                # print("Running {}".format(self.params))
                for model_param_key,value in params.items():
                    # print("Running {}".format(model_param_key))
                    setattr(self.models[key],model_param_key,value)

                model = self.models[key]

                error = self.run_creme(dat=dat, model_to_run = model)
                print(error)
                params_string = json.dumps(params)
                grid_searches[params_string] = error
            self.model_results[key] = grid_searches



    def fit_parallel(self, dat, n_jobs=3, verbose=1, cv=2):
        # ray.shutdown()
        # ray.init(object_store_memory=int(220000000000), num_cpus=multiprocessing.cpu_count()-1)
        # ray.init(object_store_memory=int(2.30e11), num_cpus=multiprocessing.cpu_count()-20, num_redis_shards=7)
        ray.init()
        output = []
        list_of_keys = []
        for _ in range(cv):
            for key in self.keys:
    #             list_of_keys = []

                print("Running {}".format(key))
                grid_searches = {}
                param_grid = list(ParameterGrid(self.params[key]))
                for params in param_grid:
                    # print("Running {}".format(self.params))
                    for model_param_key,value in params.items():
    #                     print("Running {}".format(model_param_key))
                        setattr(self.models[key],model_param_key,value)

                    model = self.models[key]

                    error = run_creme.remote(dat, model, cv=self.cv)
                    # error = run_creme(dat, model, cv=self.cv)
                    # error = dat.groupby(['season', 'working_day']).apply(run_creme, (model))

    #                 print(error)
                    params_string = json.dumps(params)
    #                 grid_searches[params_string] = error
                    list_of_keys.append(params_string)
                    output.append(error)

                output_of_creme = ray.get(output)
                # output_of_creme = output

        # print("self.keys: {}".format(self.keys))
        # print("output_of_creme: {}".format(output_of_creme))
#             self.model_results[key] = grid_searches
        self.grid_searches = {key: out for key, out in zip(list_of_keys, output_of_creme)}



def applyParallel(dfGrouped, func):
    retLst = Parallel(n_jobs=multiprocessing.cpu_count())(delayed(func)(group) for name, group in dfGrouped)
    return pd.concat(retLst)

@ray.remote(num_return_vals=1)
def run_creme(dat, model_to_use=None, metric=None, cv = 2):
    all_differences = []
    results = []

    # diffs = run_models.remote(dat, i, model_to_use, all_differences)
    # results.append(diffs)
    # results = Parallel(n_jobs=multiprocessing.cpu_count()-1)(delayed(run_models)(dat, i, model_to_use, all_differences)for i in tqdm(range(0, 24))))
    results = Parallel(n_jobs=multiprocessing.cpu_count()-1)(delayed(run_models)(dat, i, model_to_use, all_differences, cv=cv) for i in tqdm(range(0,24)))

    # for i in range(0,24):

        # diffs = run_models.remote(dat, i, model_to_use, all_differences)
        # results.append(diffs)

#         model = model_selection.online_score(X_y1, model, metric, print_every=47000)
        # print(type(model))
    # error_metrics = ray.get(diffs)

    # print(differences_dataframe)

    # return np.mean(abs(differences_dataframe.differences))
    # return differences_dataframe
    # return error_metrics
    return results

# @ray.remote(num_return_vals=1)
def run_models(dat, i, model_to_use, all_differences, cv=2):
    error_metrics_cv = []
    for cv_i in range(cv):
        X_stream = dat[dat.year < 2018].filter(regex='^(?!.*value|working_day|season|time).*$')#.values.astype(np.float32)
        start_date = len(X_stream[X_stream.year<2017])
        if i == 0:
            y_stream = dat[dat.year < 2018]['value']
        else:
            y_stream = dat[dat.year < 2018]['value-{}'.format(i)]

        X_stream_values = X_stream.values.astype(np.float32)
        y_stream_values = y_stream.values

        X_y1 = stream.iter_array(X=X_stream_values, y=y_stream_values)

        if model_to_use is None:
            model = (
                preprocessing.StandardScaler() |
                linear_model.LinearRegression()
            )
        else:
            model = (
                preprocessing.StandardScaler() |
                model_to_use
            )

        metric = metrics.Rolling(metrics.MAE(), 48)

        X_y1 = stream.iter_array(X=X_stream_values, y=y_stream_values)

        total_training = 0
        total_testing = 0
        for j, (x, y) in enumerate(X_y1):
            if j > start_date:
                predict_iteration_start = time.perf_counter()
                y_pred = model.predict_one(x)      # make a prediction
                predict_iteration_end = time.perf_counter()
                total_testing += predict_iteration_end - predict_iteration_start
            else:
                y_pred = model.predict_one(x)      # make a prediction
            metric = metric.update(y, y_pred)  # update the metric
            train_iteration_start = time.perf_counter()
            model = model.fit_one(x, y)        # make the model learn
            train_iteration_end = time.perf_counter()
            total_training += train_iteration_end - train_iteration_start
        #         if i % 55000 == 0:
            if j == len(X_stream)-1 and i == 0:
                print("{}-{}".format(j, metric))

            if j > start_date:
                actual = y

                difference = y_pred - actual
                all_differences.append(difference)

            #     flattened_differences = np.concatenate(all_differences, axis=0).flatten()
            differences_dataframe = pd.DataFrame({'differences':all_differences})
    #         diff_results = int(np.mean(abs(differences_dataframe.differences)))

        error_metrics = {
            "median_absolute_error": np.median(abs(differences_dataframe.differences)),
            "mean_squared_error": np.mean(np.square(differences_dataframe.differences)),
            "mean_absolute_error": np.mean(abs(differences_dataframe.differences)),
            "root_mean_squared_error": np.sqrt(np.mean(np.square(differences_dataframe.differences))),
            "training_time": total_training,
            "testing_time": total_testing
        }
        error_metrics_cv.append(error_metrics)
    return error_metrics_cv
    # return differences_dataframe


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
#     'SoftmaxRegression': {},
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





