"""
File name: test_fuelPlant
Date created: 27/11/2018
Feature: #Tests the functionality of the FuelPlant class.
"""
from unittest import TestCase
from src.plants.plant_type.fuel_plant import FuelPlant

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"


class TestFuelPlant(TestCase):
    def test_fuel_costs(self):
        fuel_plant = FuelPlant(name="Test_Plant", plant_type="CCGT", capacity_mw=1200, construction_year=2010,
                               average_load_factor=0.93, efficiency=0.54, pre_dev_period=2, construction_period=3,
                               operating_period=25, pre_dev_spend_years=[0.44, 0.44, 0.12],
                               construction_spend_years=[0.4, 0.4, 0.2], pre_dev_cost_per_kw=1000,
                               construction_cost_per_kw=500, infrastructure=15100, fixed_o_and_m_per_mw=12200,
                               variable_o_and_m_per_mwh=3, insurance_cost_per_mw=2100, connection_cost_per_mw=3300)

        print(fuel_plant.fuel_costs(10))
        # assert fuel_plant.fuel_costs(10) == []
