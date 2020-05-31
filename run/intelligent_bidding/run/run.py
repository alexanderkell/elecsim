import pandas as pd
import os.path
import sys
import numpy as np
import pickle
from fitter import Fitter
import fitter

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from elecsim.model.world import World
import tracemalloc

import pandas as pd
import linecache
import time
from elecsim.constants import ROOT_DIR
import logging
logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)
from scipy.stats import johnsonsb, skewnorm, dgamma, genlogistic, dweibull, johnsonsu
import ray

# @ray.remote
def run_scenario(gencos_rl_bidding, port_number):
    print("Running scenario with: {}".format(gencos_rl_bidding))
    time.sleep(60)
    beis_params = [0.00121256259168, 46.850377392563864, 0.0029982421515, 28.9229765616468, 0.00106156336814,
                   18.370337670063762, 0.00228312539654, 0.0, 0.0024046471141100003, 34.43480109190594, 0.0,
                   -20.88014916953091, 0.0, 8.15032953348701, 0.00200271495761, -12.546185375581802, 0.00155518243668,
                   39.791132970522796, 0.00027449937576, 8.42878689508516, 0.00111989525697, 19.81640207212787,
                   0.00224091998324, 5.26288570922149, 0.00209189353332, -5.9117317131295195, 0.00240696026847,
                   -5.0144941135222, 0.00021183142492999999, -1.29658413335784, 0.00039441444392000004,
                   -11.41659250225168, 0.00039441444392000004, -11.41659250225168, 120.21276910611674, 0.0,
                   0.00059945111227]

    prices_individual = np.array(beis_params[:-3]).reshape(-1, 2).tolist()

    MARKET_TIME_SPLICES = 8
    YEARS_TO_RUN = 1
    number_of_steps = YEARS_TO_RUN * MARKET_TIME_SPLICES

    scenario_2018 = "../scenario/reference_scenario_2018.py".format(ROOT_DIR)


    carbon_df = pd.read_csv('linear_data_exploded.csv'.format(ROOT_DIR))
    carbon_list = carbon_df.x.tolist()

    result_distributions_object = pickle.load(open(
        "/Users/alexanderkell/Documents/PhD/Projects/10-ELECSIM/run/market_forecasting_comparison/run/Compare_worlds/result_distributions_object.p",
        "rb"))

    resultant_dist = '{}'

    # dist_class = eval(list(result_distributions_object[resultant_dist].fitted_param.keys())[0] + ".rvs")
    # dist_object = dist_class(*list(result_distributions_object[resultant_dist].fitted_param.values())[0],
    #                          size=50000).tolist()

    while True:
        world = World(carbon_price_scenario=carbon_list, initialization_year=2018, scenario_file=scenario_2018,
                      market_time_splices=MARKET_TIME_SPLICES, data_folder="compare_ml_accuracy",
                      number_of_steps=number_of_steps, long_term_fitting_params=prices_individual, highest_demand=63910,
                      nuclear_subsidy=beis_params[-3], future_price_uncertainty_m=beis_params[-2],
                      future_price_uncertainty_c=beis_params[-1], dropbox=False, gencos_rl=gencos_rl_bidding,
                      write_data_to_file=True, rl_port_number=port_number)

        for _ in range(YEARS_TO_RUN):
            for i in range(MARKET_TIME_SPLICES):
                # try:
                if i / 8 == 0:
                    print('end of year')
                world.step()


if __name__ == "__main__":
    # gencos_rl_bidding = ['EDF Energy', 'RWE Generation SE', 'Uniper UK Limited', 'Drax Power Ltd']
    gencos_rl_bidding = ['EDF Energy', 'RWE Generation SE'] # 25
    # gencos_rl_bidding = ['EDF Energy', 'RWE Generation SE', 'Uniper UK Limited', 'Drax Power Ltd', 'SSE', 'Scottish power']
    # gencos_rl_bidding = ['AES'] # 5 Generators
    run_scenario(gencos_rl_bidding)
