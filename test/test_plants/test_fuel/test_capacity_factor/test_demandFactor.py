import logging

import pytest

from elecsim.plants.fuel.capacity_factor.capacity_factor_calculations import get_capacity_factor, get_capacity_data, segment_capacity_data_by_load_curve
from elecsim.scen_error.scenario_data import historical_hourly_demand

logger = logging.getLogger(__name__)
"""
File name: test_demandFactor
Date created: 27/12/2018
Feature: # Testing for demand factor calculations.
"""
logging.basicConfig(level=logging.DEBUG)


__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"


class TestDemandFactor:
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
        capacity_factor = segment_capacity_data_by_load_curve(capacity_data, historical_hourly_demand, "offshore")
        logger.debug(capacity_factor)
        assert capacity_factor.mean()[0] == pytest.approx(0.39, abs=1)

    @pytest.mark.parametrize("plant_type, demand_hour, expected_output",
                             [
                                 ("pv", 6910, 0.208738),
                                 ("pv", 8752.500000, 0.304236),
                                 ("pv", 0, 0.004586),
                                 ("pv", 2763, 0.037869),
                                 ("pv", 1841, 0.032182),
                                 ("offshore", 8752.500000, 0.472709),
                                 ("offshore", 6910, 0.408348),
                                 ("offshore", 6448, 0.388440),
                                 ("offshore", 0, 0.332907),
                                 ("onshore", 8752.500000, 0.359845),
                                 ("onshore", 6910, 0.314773),
                                 ("onshore", 6448, 0.299287),
                                 ("onshore", 0, 0.236361),
                             ])
    def test_get_capacity_factor(self, plant_type, demand_hour, expected_output):
         assert get_capacity_factor(plant_type, demand_hour) == pytest.approx(expected_output, rel=0.001)
