from src.plants.fuel.capacity_factor.capacity_factor_calculations import DemandFactor
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
        demand_factor = DemandFactor("pv")
        demand_factors = demand_factor.calculate_demand_factor_for_segment()
        assert demand_factors.mean() ==  pytest.approx(0.1053, abs=0.01)

    def test_calculate_onshore_demand_factor_for_segment(self):
        demand_factor = DemandFactor("onshore")
        demand_factors = demand_factor.calculate_demand_factor_for_segment()
        assert demand_factors.mean() == pytest.approx(0.3, abs=0.5)

    def test_calculate_offshore_demand_factor_for_segment(self):
        demand_factor = DemandFactor("offshore")
        demand_factors = demand_factor.calculate_demand_factor_for_segment()
        assert demand_factors.mean() == pytest.approx(0.39, abs=1)
