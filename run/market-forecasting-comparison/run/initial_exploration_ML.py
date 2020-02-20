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

"""
File name: initial_exploration_ML
Date created: 20/02/2020
Feature: #Enter feature description here
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"


if __name__ == "__main__":

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
        'ExtraTreesRegressor': { 'model__estimator__n_estimators': [16, 32] },
        'RandomForestRegressor': { 'model__estimator__n_estimators': [16, 32] },
        'AdaBoostRegressor':  { 'model__estimator__n_n_estimators': [16, 32] },
        'GradientBoostingRegressor': { 'model__estimator__n_n_estimators': [16, 32], 'model__estimator__n_learning_rate': [0.8, 1.0] },
        'SVR': [
            {'model__estimator__n_kernel': ['linear'], 'model__estimator__n_C': [1, 10]},
            {'model__estimator__n_kernel': ['rbf'], 'model__estimator__n_C': [1, 10], 'model__estimator__n_gamma': [0.001, 0.0001]},
        ],
        'MLPRegressor': {"model__estimator__n_hidden_layer_sizes": [(1,), (50,)], "model__estimator__n_activation": ["tanh", "relu"], "model__estimator__n_solver": ["adam"], "model__estimator__n_alpha": [0.00005, 0.0005]},
        'KNeighborsRegressor': {'model__estimator__n_neighbors': [5, 20, 50], 'model__estimator__n_weights': ['distance','uniform']},
    }
