"""
File name: test_powerPlant
Date created: 28/11/2018
Feature: #Enter feature description here
"""
import logging
from unittest import TestCase

from pytest import approx
logger = logging.getLogger(__name__)

from elecsim.role.plants.costs.fuel_plant_cost_calculations import FuelPlantCostCalculations
from elecsim.plants.plant_costs.estimate_costs.estimate_costs import create_power_plant


__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"

logging.basicConfig(level=logging.DEBUG)


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
        power_plant_calculations = self.create_ccgt_2018_power_plant_object()
        variable_to_discount = [10, 10, 10, 10, 10]
        discount_rate = 0.05
        assert power_plant_calculations._discount_data(variable_to_discount, discount_rate) == approx([10, 9.52381, 9.070295, 8.6383762, 8.22702495])

    def test_pre_dev_yearly_spend(self):
        power_plant_calculations = self.create_ccgt_2018_power_plant_object()
        assert power_plant_calculations._pre_dev_yearly_spend() == [5280000, 5280000, 1440000]

    def test_construction_yearly_spend(self):
        power_plant_calculations = self.create_ccgt_2018_power_plant_object()
        assert power_plant_calculations._construction_yearly_spend() == [240000000, 240000000, 120000000]

    def test_capex(self):
        power_plant_calculations = self.create_ccgt_2018_power_plant_object()
        assert power_plant_calculations._capex() == [5280000, 5280000, 1440000, 240000000, 240000000, 135100000]

    def test_insurance_cost(self):
        power_plant_calculations = self.create_ccgt_2018_power_plant_object()
        power_plant_calculations._insurance_cost() == [0, 0, 0, 0, 0]+[2520000]*25

    def test_variable_o_and_m_cost(self):
        power_plant_calculations = self.create_ccgt_2018_power_plant_object()
        power_plant_calculations._variable_o_and_m_cost() == [0]*6 + [29328480]*25

    def test_fixed_o_and_m_cost(self):
        power_plant_calculations = self.create_ccgt_2018_power_plant_object()
        assert power_plant_calculations._fixed_o_and_m_cost() == [0]*6 + [14640000]*25

    def test_opex(self):
        power_plant_calculations = self.create_ccgt_2018_power_plant_object()
        assert power_plant_calculations._opex_cost() == [0] * 6 + [46488480]*25

    def test_electricity_generated(self):
        power_plant_calculations = self.create_ccgt_2018_power_plant_object()
        assert power_plant_calculations._electricity_generated() == [0]*6+[9776160]*25

    def test_check_if_operating_in_certain_year(self):
        power_plant = create_power_plant("test_plant", 2018, "CCGT", 1200)
        assert power_plant.check_if_operating_in_certain_year(2018, 2) == False
        assert power_plant.check_if_operating_in_certain_year(2018, 3) == False
        assert power_plant.check_if_operating_in_certain_year(2018, 4) == False
        assert power_plant.check_if_operating_in_certain_year(2018, 5) == False
        assert power_plant.check_if_operating_in_certain_year(2018, 6) == False
        assert power_plant.check_if_operating_in_certain_year(2018, 7) == True
        assert power_plant.check_if_operating_in_certain_year(2018, 8) == True
        assert power_plant.check_if_operating_in_certain_year(2018, 9) == True
        assert power_plant.check_if_operating_in_certain_year(2018, 10) == True
        assert power_plant.check_if_operating_in_certain_year(2018, 11) == True
        assert power_plant.check_if_operating_in_certain_year(2018, 12) == True
        assert power_plant.check_if_operating_in_certain_year(2018, 13) == True
        assert power_plant.check_if_operating_in_certain_year(2018, 14) == True
        assert power_plant.check_if_operating_in_certain_year(2018, 31) == True
        assert power_plant.check_if_operating_in_certain_year(2018, 32) == False
        assert power_plant.check_if_operating_in_certain_year(2018, 33) == False


