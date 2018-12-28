from src.plants.fuel.capacity_factor.capacity_factor_calculations import CapacityFactorCalculations
import pytest
import logging
logger = logging.getLogger(__name__)
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
    def test_calculate_pv_demand_factor_for_segment(self):
        demand_factor = CapacityFactorCalculations("pv")
        demand_factors = demand_factor._calculate_demand_factors()
        assert demand_factors.mean() ==  pytest.approx(0.1053, abs=0.01)

    def test_calculate_onshore_demand_factor_for_segment(self):
        demand_factor = CapacityFactorCalculations("onshore")
        demand_factors = demand_factor._calculate_demand_factors()
        assert demand_factors.mean() == pytest.approx(0.3, abs=0.5)

    def test_calculate_offshore_demand_factor_for_segment(self):
        demand_factor = CapacityFactorCalculations("offshore")
        demand_factors = demand_factor._calculate_demand_factors()
        assert demand_factors.mean() == pytest.approx(0.39, abs=1)

    def test_calculate_hours_of_demand(self):
        demand_factor = CapacityFactorCalculations("offshore")
        demand_factor.get_capacity_factor()
