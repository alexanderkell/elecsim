# from src.plants.fuel.capacity_factor.capacity_factor_calculations import CapacityFactorCalculations

from src.plants.fuel.capacity_factor.capacity_factor_calculations import get_capacity_factor, get_capacity_data, segment_capacity_data_by_load_curve
from src.scenario.scenario_data import historical_hourly_demand

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
        capacity_data = get_capacity_data('pv')
        logger.debug(capacity_data)
        capacity_factor = segment_capacity_data_by_load_curve(capacity_data, historical_hourly_demand, "pv")
        logger.debug(capacity_factor)

        assert capacity_factor.mean()[0] ==  pytest.approx(0.1053, abs=0.01)


    def test_calculate_onshore_demand_factor_for_segment(self):
        capacity_data = get_capacity_data('onshore')
        logger.debug(capacity_data)
        capacity_factor = segment_capacity_data_by_load_curve(capacity_data, historical_hourly_demand, "onshore")
        logger.debug(capacity_factor)
        assert capacity_factor.mean()[0] == pytest.approx(0.3, abs=0.5)

    def test_calculate_offshore_demand_factor_for_segment(self):
        capacity_data = get_capacity_data('offshore')
        logger.debug(capacity_data)
        capacity_factor = segment_capacity_data_by_load_curve(capacity_data, historical_hourly_demand, "offshore")
        logger.debug(capacity_factor)
        assert capacity_factor.mean()[0] == pytest.approx(0.39, abs=1)

    # def test_calculate_hours_of_demand(self):
    #     demand_factor = CapacityFactorCalculations("offshore")
    #     demand_factor.get_capacity_factor()


    def test_get_capacity_factor(self):
        get_capacity_factor("offshore", 6910)
