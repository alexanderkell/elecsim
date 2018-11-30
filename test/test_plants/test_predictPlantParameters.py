'''
File name: test_predictPlantStatistics
Date created: 27/11/2018
Feature: #Enter feature description here
'''
from unittest import TestCase
from pytest import approx

from src.plants.plant_costs.estimate_costs.estimate_modern_power_plant_costs.predict_modern_plant_costs import PredictPlantParameters

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"


class TestPredictPlantParameters(TestCase):
    def test___call__(self):
        estimated_plant_parameters = PredictPlantParameters("CCGT", 1200, 2018)()
        assert estimated_plant_parameters['connection_cost_per_mw'] == 3300
        assert estimated_plant_parameters['construction_cost_per_mw'] == 500000
        assert estimated_plant_parameters['fixed_o_and_m_per_mw'] == 12200
        assert estimated_plant_parameters['infrastructure'] == 15100
        assert estimated_plant_parameters['insurance_cost_per_mw'] == 2100
        assert estimated_plant_parameters['pre_dev_cost_per_mw'] == 10000
        assert estimated_plant_parameters['variable_o_and_m_per_mwh'] == 3.00
        assert estimated_plant_parameters['pre_dev_period'] == 3
        assert estimated_plant_parameters['operating_period'] == 25
        assert estimated_plant_parameters['construction_period'] == 3
        assert estimated_plant_parameters['efficiency'] == 0.54
        assert estimated_plant_parameters['average_load_factor'] == 0.93
        assert estimated_plant_parameters['construction_spend_years'] == [0.4, 0.4, 0.2]
        assert estimated_plant_parameters['pre_dev_spend_years'] == [0.44, 0.44, 0.12]




