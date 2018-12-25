from numpy import npv

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


def calculate_npv(discount_rate, year, lookback_period):

    plant = create_power_plant("Test", year, "CCGT", 1200)
    plant_dict = vars(plant)
    func = FuelPlantCostCalculations
    args_to_use = signature(func)._parameters

    dict_to_use = {key:plant_dict[key] for key in plant_dict if key in args_to_use}

    cost_calc = FuelPlantCostCalculations(**dict_to_use)

    total_costs = cost_calc.calculate_total_costs()[1]

    total_income = cost_calc.total_returns(70)

    expected_cash_flow = [income-cost for income, cost in zip(total_income, total_costs)]

    logging.debug("expected cash flow: {}".format(expected_cash_flow))
    logging.debug("total costs: {}".format(total_costs))
    logging.debug("total income: {}".format(total_income))

    logging.debug("expected cash flow len : {}".format(len(expected_cash_flow)))
    logging.debug("total costs len: {}".format(len(total_costs)))
    logging.debug("total income len : {}".format(len(total_income)))

    logging.debug(npv(discount_rate, expected_cash_flow))
