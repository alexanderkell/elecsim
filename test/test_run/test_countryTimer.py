import logging

import pytest
from pytest import approx

from run.timing.batch_run_timer import DemandTimer
from elecsim.scenario.scenario_data import power_plants
logger = logging.getLogger(__name__)

"""
File name: test_countryTimer
Date created: 25/01/2019
Feature: #Enter feature description here
"""

logging.basicConfig(level=logging.INFO)

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"


class TestCountryTimer:

    @pytest.mark.parametrize("demand_required,demand_expected", [
        (1074000, 1074000),  # USA
        (1646000, 1646000), # China
        (322200, 322200), # Japan
        (150300, 150300), # Brazil
        (94640, 94640), # United Kingdom
        (65450, 65450), # Mexico
        (37320, 37320), # Poland
        (18940, 18940), # Greece
        # (4881, 4881), # Croatia
        # (2772, 2772), # Iceland
        # Source: https://www.cia.gov/LIBRARY/publications/the-world-factbook/rankorder/2236rank.html
    ])
    def test_stratify_data(self, demand_required, demand_expected):
        timer_calc = DemandTimer()
        stratified_sample = timer_calc.stratify_data(demand_required)
        logger.info("total capacity: {}, peak demand: {}".format(power_plants.Capacity.sum(), 52152))
        assert stratified_sample.Capacity.sum() == approx(demand_expected, rel=0.4)


