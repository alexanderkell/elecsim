"""
File name: test_estimate_costs
Date created: 01/12/2018
Feature: # Test for Estimate costs. Takes a construction date, plant type and capacity and returns cost parameters
"""
from unittest import TestCase

from pytest import approx

from src.plants.plant_type.fuel_plants.fuel_plant import FuelPlant
from src.plants.plant_costs.estimate_costs.estimate_costs import select_cost_estimator

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"


class TestEstimateCosts(TestCase):
    def test_estimate_modern_costs(self):

        print(select_cost_estimator(2018, "CCGT", 1200))
        assert select_cost_estimator(2018, "CCGT", 1200) == {'connection_cost_per_mw': 3300,
                                                             'construction_cost_per_mw': 500000,
                                                             'fixed_o_and_m_per_mw': 12200, 'infrastructure': 15100,
                                                             'insurance_cost_per_mw': 2100,
                                                             'pre_dev_cost_per_mw': 10000,
                                                             'variable_o_and_m_per_mwh': 3, 'pre_dev_period': 3,
                                                             'operating_period': 25, 'construction_period': 3,
                                                             'efficiency': 0.54, 'average_load_factor': 0.93,
                                                             'construction_spend_years': [0.4, 0.4, 0.2],
                                                             'pre_dev_spend_years': [0.44, 0.44, 0.12]}

    def test_estimate_old_power_plant(self):
        params_2011 = select_cost_estimator(2011, "CCGT", 1200)
        assert FuelPlant(name="Test", plant_type="CCGT", construction_year=2011, capacity_mw=1200,
                         **params_2011).calculate_lcoe(0.1) == approx(100.6760057)
