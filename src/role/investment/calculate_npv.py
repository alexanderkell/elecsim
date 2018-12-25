from numpy import npv
from scipy.optimize import minimize
import numpy as np
import seaborn as sns
from operator import itemgetter
import pandas as pd
import matplotlib.pyplot as plt

import logging
from inspect import signature
logger = logging.getLogger(__name__)

from src.role.plants.fuel_lcoe_calculation import FuelPlantCostCalculations
from src.plants.plant_costs.estimate_costs.estimate_costs import create_power_plant


"""
File name: calculate_npv
Date created: 24/12/2018
Feature: # Contains functionality to assess options of investment and return lowest NPV for decision to be made.
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"


def calculate_npv(plant_size, discount_rate, year, plant_type, expected_sell_price, lookback_period):
    plant = create_power_plant("Test", year, plant_type, plant_size)
    plant_dict = vars(plant)
    expected_cash_flow = calculate_expected_cash_flow(plant_dict, expected_sell_price)
    npv_value = npv(discount_rate, expected_cash_flow)
    return npv_value

def calculate_expected_cash_flow(plant_dict, expected_sell_price):
    func = FuelPlantCostCalculations
    args_to_use = signature(func)._parameters
    dict_to_use = {key: plant_dict[key] for key in plant_dict if key in args_to_use}
    cost_calc = FuelPlantCostCalculations(**dict_to_use)
    total_costs = cost_calc.calculate_total_costs()[1]
    total_income = cost_calc.total_income(expected_sell_price)
    expected_cash_flow = [income - cost for income, cost in zip(total_income, total_costs)]

    return expected_cash_flow

def maximum_return():
    cost_list = []
    for plant_type in ['CCGT','Coal','Nuclear','OCGT']:
        for i in range(0,2000):
            npv = calculate_npv(i, 0.06, 2018, plant_type, 80, 4)
            dict = {"npv":npv, "capacity":i, "plant_type":plant_type}
            cost_list.append(dict.copy())
    #
    # cost_list = {"npv":calculate_npv(i, 0.06, 2018, 'Nuclear', 80, 4), "capacity":i for i in range(10)}
    # cost_list1 = {"npv":calculate_npv(i, 0.06, 2018, 'CCGT', 80, 4) for i in range(10)}
    # cost_list2 = {"npv":calculate_npv(i, 0.06, 2018, 'Coal', 80, 4) for i in range(10)}

    df = pd.DataFrame(cost_list)
    # plt.plot(df['capacity'], df['npv'])
    sns.lineplot(x='capacity', y="npv", hue='plant_type', data = df)
    plt.show()
    logging.debug(max(cost_list,key=itemgetter(0)))

