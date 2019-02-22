"""
File name: test_noFuelPlant
Date created: 28/11/2018
Feature: #Enter feature description here
"""
from unittest import TestCase

from pytest import approx

from elecsim.plants.plant_type.non_fuel_plant import NonFuelPlant



__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"


class TestNoFuelPlant(TestCase):
    # def create_2018_biomass_power_plant(self):
    #     fuel_plant = FuelPlant(name="Test_Plant", plant_type="Biomass_wood", capacity_mw=1200, construction_year=2010,
    #                               average_load_factor=0.93, efficiency=0.54, pre_dev_period=3, construction_period=3,
    #                               operating_period=25, pre_dev_spend_years=[0.44, 0.44, 0.12],
    #                               construction_spend_years=[0.4, 0.4, 0.2], pre_dev_cost_per_mw=1000,
    #                               construction_cost_per_mw=500, infrastructure=15100, fixed_o_and_m_per_mw=12200,
    #                               variable_o_and_m_per_mwh=3, insurance_cost_per_mw=2100, connection_cost_per_mw=3300)
    #     return fuel_plant
    #
    #
    # def test_calculate_lcoe(self):
    #     power_plant = self.create_2018_biomass_power_plant()
    #     print("LCOE for biomass: {}".format(power_plant.calculate_lcoe(0.1)))
    #     # assert power_plant.calculate_lcoe() == 1

    def test_small_hydro_plant_lcoe_calculation(self):
        params = {'connection_cost_per_mw': 0.0, 'construction_cost_per_mw': 4103676.6103626275, 'fixed_o_and_m_per_mw': 37265.847352193756, 'infrastructure': 311.06133108680143, 'insurance_cost_per_mw': 0.0, 'pre_dev_cost_per_mw': 0, 'variable_o_and_m_per_mwh': 3.074841257793032, 'pre_dev_period': 0, 'operating_period': 35, 'construction_period': 0, 'efficiency': 1, 'average_load_factor': 0.4, 'construction_spend_years': [1.0], 'pre_dev_spend_years': []}
        hydro_plant = NonFuelPlant(name="Hydro", plant_type="Hydro", capacity_mw=5, construction_year=2002, **params)
        assert hydro_plant.calculate_lcoe(0.075) == approx(103.8260236534459)

