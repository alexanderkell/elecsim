"""
File name: test_select_cost_estimator
Date created: 04/12/2018
Feature: #Enter feature description here
"""
from unittest import TestCase
from src.plants.plant_costs.estimate_costs.estimate_costs import select_cost_estimator

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"


class TestSelectCostEstimator(TestCase):
    # def test_parameter_estimator_for_modern_small_gas_turbine_with_capacity_matching_data(self):
    #     assert select_cost_estimator(2018, "CCGT", 168.0) == {'connection_cost_per_mw': 3300.0,
    #                                                           'construction_cost_per_mw': 700000.0,
    #                                                           'fixed_o_and_m_per_mw': 28200.0,
    #                                                           'infrastructure': 13600.0,
    #                                                           'insurance_cost_per_mw': 2900.0,
    #                                                           'pre_dev_cost_per_mw': 60000.0,
    #                                                           'variable_o_and_m_per_mwh': 5.0, 'pre_dev_period': 3,
    #                                                           'operating_period': 25, 'construction_period': 3,
    #                                                           'efficiency': 0.34, 'average_load_factor': 0.93,
    #                                                           'construction_spend_years': [0.4, 0.4, 0.2],
    #                                                           'pre_dev_spend_years': [0.435, 0.435, 0.13]}

    def test_parameter_estimator_for_historic_small_gas_turbine_with_capacity_matching_data(self):
        print(select_cost_estimator(1990, "CCGT", 168.0))
