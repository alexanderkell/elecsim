"""
File name: test_noFuelPlant
Date created: 28/11/2018
Feature: #Enter feature description here
"""
from unittest import TestCase

from plants.plant_type.non_fuel_plants.non_fuel_plant import NonFuelPlant

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"


class TestNoFuelPlant(TestCase):
    def create_2018_biomass_power_plant(self):
        fuel_plant = NonFuelPlant(name="Test_Plant", plant_type="Biomass", capacity_mw=1200, construction_year=2010,
                                  average_load_factor=0.93, efficiency=0.54, pre_dev_period=3, construction_period=3,
                                  operating_period=25, pre_dev_spend_years=[0.44, 0.44, 0.12],
                                  construction_spend_years=[0.4, 0.4, 0.2], pre_dev_cost_per_mw=1000,
                                  construction_cost_per_mw=500, infrastructure=15100, fixed_o_and_m_per_mw=12200,
                                  variable_o_and_m_per_mwh=3, insurance_cost_per_mw=2100, connection_cost_per_mw=3300)
        return fuel_plant


    def test_calculate_lcoe(self):
        power_plant = self.create_2018_biomass_power_plant()
        # TO DO
        # assert power_plant.calculate_lcoe() == 1
