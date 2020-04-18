from creme import linear_model
from creme import meta
from creme import neighbors
from sklearn import neural_network

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

import numpy as np
import pandas as pd

import multiprocessing

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

    def __init__(self, models, params):
        if not set(models.keys()).issubset(set(params.keys())):
            missing_params = list(set(models.keys()) - set(params.keys()))
            raise ValueError("Some estimators are missing parameters: %s" % missing_params)
        self.models = models
        self.params = params
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



    def fit_parallel(self, dat, n_jobs=3, verbose=1):
        ray.shutdown()
        # ray.init(object_store_memory=int(220000000000), num_cpus=multiprocessing.cpu_count()-1)
        ray.init(object_store_memory=int(2.30*10^11), num_cpus=multiprocessing.cpu_count()-6)
        output = []
        list_of_keys = []
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

                # error = run_creme.remote(dat, model)
                error = run_creme(dat, model)

#                 print(error)
                params_string = json.dumps(params)
#                 grid_searches[params_string] = error
                list_of_keys.append(params_string)
                output.append(error)

            output_of_creme = ray.get(output)
        # print("self.keys: {}".format(self.keys))
        # print("output_of_creme: {}".format(output_of_creme))
#             self.model_results[key] = grid_searches
        self.grid_searches = {key: out for key, out in zip(list_of_keys, output_of_creme)}


# @ray.remote(num_return_vals=1)
def run_creme(dat, model_to_use=None, metric=None):
    all_differences = []
    results = []
    for i in range(0,24):

        diffs = run_models.remote(dat, i, model_to_use, all_differences)
        results.append(diffs)

#         model = model_selection.online_score(X_y1, model, metric, print_every=47000)
        # print(type(model))
    error_metrics = ray.get(diffs)
    # print(differences_dataframe)

    # return np.mean(abs(differences_dataframe.differences))
    # return differences_dataframe
    return error_metrics

@ray.remote(num_return_vals=1)
def run_models(dat, i, model_to_use, all_differences):

    X_stream = dat[dat.year<2018].filter(regex='^(?!.*value|working_day|season|time).*$')#.values.astype(np.float32)
    start_date = len(X_stream[X_stream.year<2017])
    if i == 0:
        y_stream = dat[dat.year<2018]['value']
    else:
        y_stream = dat[dat.year<2018]['value-{}'.format(i)]

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

    for j, (x, y) in enumerate(X_y1):
        y_pred = model.predict_one(x)      # make a prediction
        metric = metric.update(y, y_pred)  # update the metric
        model = model.fit_one(x, y)        # make the model learn
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
            "mean_absolute_error" : np.mean(abs(differences_dataframe.differences)),
            "root_mean_squared_error": np.sqrt(np.mean(np.square(differences_dataframe.differences)))
        }
    return error_metrics


