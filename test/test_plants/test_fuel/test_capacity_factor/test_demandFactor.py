from src.plants.fuel.capacity_factor.solar_capacity_factor import DemandFactor
import logging
"""
File name: test_demandFactor
Date created: 27/12/2018
Feature: #Enter feature description here
"""
from unittest import TestCase
logging.basicConfig(level=logging.DEBUG)


__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"


class TestDemandFactor(TestCase):
    def test_calculate_demand_factor_for_segment(self):
        demand_factor = DemandFactor("Onshore")
        demand_factor.calculate_demand_factor_for_segment()
