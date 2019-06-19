
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../..'))

import logging

import pytest

from elecsim.plants.fuel.capacity_factor.capacity_factor_calculations import get_capacity_factor, get_capacity_data, segment_capacity_data_by_load_curve
from elecsim.scenario.scenario_data import historical_hourly_demand

logger = logging.getLogger(__name__)

capacity_data = get_capacity_data('pv')
logger.debug(capacity_data)
capacity_factor = segment_capacity_data_by_load_curve(capacity_data, historical_hourly_demand, "pv")
logger.debug(capacity_factor)

assert capacity_factor.mean()[0] ==  pytest.approx(0.1053, abs=0.01)