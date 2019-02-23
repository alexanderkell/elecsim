from unittest.mock import Mock

import pytest

from elecsim.agents.generation_company.gen_co import GenCo
from elecsim.market.electricity.power_exchange import PowerExchange
from elecsim.plants.plant_costs.estimate_costs.estimate_costs import create_power_plant

"""
File name: test_powerExchange
Date created: 01/01/2019
Feature: # Testing of power exchange.
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"


class TestPowerExchange:

    @pytest.fixture(scope="module")
    def power_exchange(self):
        model = Mock()

        gen_co1 = GenCo(1, model, "Test", 0.06)
        gen_co1.plants = [create_power_plant("Test", )]
        gen_co1 = GenCo(1, model, "Test", 0.06)
        gen_co1 = GenCo(1, model, "Test", 0.06)
        gen_co1 = GenCo(1, model, "Test", 0.06)


        model.schedule.agents = []
        power_exchange = PowerExchange(model)
        return power_exchange

    def test_tender_bids(self):
        pass

    def test__create_load_duration_price_curve(self):
        pass

    def test__accept_bids(self):
        pass

    def test__sort_bids(self):
        pass

    def test__respond_to_bids(self):
        pass
