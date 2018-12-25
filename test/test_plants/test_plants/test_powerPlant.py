"""
File name: test_powerPlant
Date created: 28/11/2018
Feature: #Enter feature description here
"""
from src.plants.plant_type.power_plant import PowerPlant
from pytest import approx
from unittest import TestCase
import pytest
from src.role.plants.fuel_plant_cost_calculations import FuelPlantCostCalculations

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"


class TestPowerPlant(TestCase):

    def create_ccgt_2018_power_plant_object(self):
        fuelLCOECalculationObj = FuelPlantCostCalculations(plant_type="CCGT", capacity_mw=1200, construction_year=2010,
                                                           average_load_factor=0.93, efficiency=0.54, pre_dev_period=3, construction_period=3,
                                                           operating_period=25, pre_dev_spend_years=[0.44, 0.44, 0.12],
                                                           construction_spend_years=[0.4, 0.4, 0.2], pre_dev_cost_per_mw=10000,
                                                           construction_cost_per_mw=500000, infrastructure=15100, fixed_o_and_m_per_mw=12200,
                                                           variable_o_and_m_per_mwh=3, insurance_cost_per_mw=2100, connection_cost_per_mw=3300)
        return fuelLCOECalculationObj

    def test_discounted_variable(self):
        power_plant = self.create_ccgt_2018_power_plant_object()
        variable_to_discount = [10, 10, 10, 10, 10]
        discount_rate = 0.05
        assert power_plant._discount_data(variable_to_discount, discount_rate) == approx([10, 9.52381, 9.070295, 8.6383762, 8.22702495])

    def test_pre_dev_yearly_spend(self):
        power_plant = self.create_ccgt_2018_power_plant_object()
        assert power_plant._pre_dev_yearly_spend() == [5280000, 5280000, 1440000]

    def test_construction_yearly_spend(self):
        power_plant = self.create_ccgt_2018_power_plant_object()
        assert power_plant._construction_yearly_spend() == [240000000, 240000000, 120000000]

    def test_capex(self):
        power_plant = self.create_ccgt_2018_power_plant_object()
        assert power_plant._capex() == [5280000, 5280000, 1440000, 240000000, 240000000, 135100000]

    def test_insurance_cost(self):
        power_plant = self.create_ccgt_2018_power_plant_object()
        power_plant._insurance_cost() == [0, 0, 0, 0, 0]+[2520000]*25

    def test_variable_o_and_m_cost(self):
        power_plant = self.create_ccgt_2018_power_plant_object()
        power_plant._variable_o_and_m_cost() == [0]*6 + [29328480]*25

    def test_fixed_o_and_m_cost(self):
        power_plant = self.create_ccgt_2018_power_plant_object()
        assert power_plant._fixed_o_and_m_cost() == [0]*6 + [14640000]*25

    def test_opex(self):
        power_plant = self.create_ccgt_2018_power_plant_object()
        assert power_plant._opex_cost() == [0] * 6 + [46488480]*25

    def test_electricity_generated(self):
        power_plant = self.create_ccgt_2018_power_plant_object()
        assert power_plant._electricity_generated() == [0]*6+[9776160]*25
