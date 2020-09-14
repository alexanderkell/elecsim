import pandas as pd
import pickle
import seaborn as sns
import matplotlib.pyplot as plt
from fitter import Fitter


from joblib import Parallel, delayed

"""
File name: get_optimal_distributions
Date created: 19/04/2020
Feature: #Enter feature description here
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"


def dict_to_results_df(results_dict):
    residuals = {}
    for result in results_dict:
        model_type = {}
        flat_list = []
        for i in range(len(results_dict[result])):
            flat_list.append(results_dict[result][i])
        residuals[result] = pd.concat(flat_list[0])

    return residuals





results_dict = pickle.load( open( '../data/results/demand_initial_exploration-2020-04-19 09_19_00.102190-select-few-groupby-day-season.csv', "rb" ) )
residuals = dict_to_results_df(results_dict)
residuals = {f'{k}-groupby': v for k, v in residuals.items()}

results_no_work_day = pickle.load( open( '../data/results/demand_initial_exploration-2020-04-19 11_11_17.690094-no-workday-season-groupby.csv', "rb" ) )

merged_dict = {**residuals, **results_no_work_day}

result_distributions = {}



def find_distributions(results, results_dict):
    try:
        f = Fitter(results_dict[results])
    except:
        f = Fitter(results_dict[results][0])
    f.fit()
    result_distributions[results] = f.summary()
    return result_distributions

# for result in merged_dict:
#     find_distributions(result, merged_dict)

final_result = Parallel(n_jobs=62)(delayed(find_distributions)(result, merged_dict) for result in merged_dict)

with open('final_result_distributions.pickle', 'wb') as handle:
    pickle.dump(final_result, handle)
