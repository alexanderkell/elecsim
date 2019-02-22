'''
File name: test_fuelOldPlantCosts
Date created: 26/11/2018
Feature: #Enter feature description here
'''
import logging
from unittest import TestCase

from pytest import approx

from elecsim.plants.plant_costs.estimate_costs.estimate_old_plant_cost_params.fuel_plant_calculations.fuel_plants_old_params import FuelOldPlantCosts
from elecsim.plants.plant_type.fuel_plant import FuelPlant

logging.basicConfig(level=logging.DEBUG)

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"


class TestFuelOldPlantCosts(TestCase):

    def test_estimate_cost_parameters(self):
        fuel_plant_costs_estimate = FuelOldPlantCosts(2011, "CCGT", 1200)
        estimated_params = fuel_plant_costs_estimate.estimate_cost_parameters()
        print("Estimated parameters")
        print(estimated_params)
        assert estimated_params['connection_cost_per_mw'] == approx(3300*5.4570773402)
        assert estimated_params['construction_cost_per_mw'] == approx(500000*5.4570773402)
        assert estimated_params['fixed_o_and_m_per_mw'] == approx(12200*5.4570773402)
        assert estimated_params['infrastructure'] == approx(15100*5.4570773402)
        assert estimated_params['insurance_cost_per_mw'] == approx(2100*5.4570773402)
        assert estimated_params['pre_dev_cost_per_mw'] == approx(10000*5.4570773402)
        assert estimated_params['variable_o_and_m_per_mwh'] == approx(3*5.4570773402)
        assert estimated_params['pre_dev_period'] == 3
        assert estimated_params['construction_period'] == 3
        assert estimated_params['efficiency'] == 0.54
        assert estimated_params['average_load_factor'] == 0.93
        assert estimated_params['construction_spend_years'] == [0.4, 0.4, 0.2]
        assert estimated_params['pre_dev_spend_years'] == [0.44, 0.44, 0.12]

    def test_if_estimated_parameters_lead_to_correct_lcoe(self):
        fuel_plant_costs_estimate = FuelOldPlantCosts(2011, "CCGT", 1200)
        estimated_params = fuel_plant_costs_estimate.estimate_cost_parameters()
        print(estimated_params)
        print("LCOE: {}".format(FuelPlant(name="Test", plant_type="CCGT", capacity_mw=1200, construction_year=2011, **estimated_params).calculate_lcoe(0.1)))
