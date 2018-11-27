'''
File name: test_fuelOldPlantCosts
Date created: 26/11/2018
Feature: #Enter feature description here
'''
from unittest import TestCase
import pytest
from src.plants.plant_costs.estimate_costs.estimate_old_plant_cost_params.fuel_plants_old_params import FuelOldPlantCosts

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"


class TestFuelOldPlantCosts(TestCase):

    def test_estimate_cost_parameters(self):
        fuel_plant_costs_estimate = FuelOldPlantCosts(2018, "CCGT", 1200)
        estimated_params = fuel_plant_costs_estimate.estimate_cost_parameters()

        # print(estimated_params)

        # assert estimated_params['connection_cost_per_mw'] == pytest.approx(3300*8.781317895767428)
        # assert estimated_params['construction_cost_per_kw'] == pytest.approx(500*8.781317895767428)
        # assert estimated_params['fixed_o_and_m_per_mw'] == pytest.approx(12200*8.781317895767428)
        # assert estimated_params['infrastructure'] == pytest.approx(15100*8.781317895767428)
        # assert estimated_params['insurance_cost_per_mw'] == pytest.approx(2100*8.781317895767428)
        # assert estimated_params['pre_dev_cost_per_kw'] == pytest.approx(10*8.781317895767428)
        # assert estimated_params['variable_o_and_m_per_mwh'] == pytest.approx(3*8.781317895767428)
        assert estimated_params['pre_dev_period'] == 2
        assert estimated_params['construction_period'] == 3
        assert estimated_params['efficiency'] == 0.54
        assert estimated_params['average_load_factor'] == 0.93
        assert estimated_params['construction_spend_years'] == [0.4, 0.4, 0.2]
        assert estimated_params['pre_dev_spend_years'] == [0.44, 0.44, 0.12]
