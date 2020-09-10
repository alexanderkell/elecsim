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
