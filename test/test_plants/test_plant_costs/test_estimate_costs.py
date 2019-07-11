"""
File name: test_estimate_costs
Date created: 01/12/2018
Feature: # Test for Estimate costs. Takes a construction date, plant type and capacity and returns cost parameters
"""
from unittest import TestCase

from pytest import approx
import matplotlib.pyplot as plt
import seaborn as sns
from elecsim.plants.plant_costs.estimate_costs.estimate_costs import _select_cost_estimator, create_power_plant_group
from elecsim.plants.plant_type.fuel_plant import FuelPlant

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"


class TestEstimateCosts(TestCase):
    def test_estimate_modern_costs(self):

        print(_select_cost_estimator(2018, "CCGT", 1200))
        assert _select_cost_estimator(2018, "CCGT", 1200) == {'connection_cost_per_mw': 3300,
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
        params_2011 = _select_cost_estimator(2011, "CCGT", 1200)
        assert FuelPlant(name="Test", plant_type="CCGT", construction_year=2011, capacity_mw=1200,
                         **params_2011).calculate_lcoe(0.1) == approx(114.61207558392651)

    def test_select_power_plant_group(self):
        val = create_power_plant_group("group", 20000, 2019, "PV")
        assert val == 15400000400
