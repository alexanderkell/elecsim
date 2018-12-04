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


class TestSelect_cost_estimator(TestCase):
    def test_select_cost_estimator(self):
        print(select_cost_estimator(1983.0, "Hydro_Store", 1800.0))
