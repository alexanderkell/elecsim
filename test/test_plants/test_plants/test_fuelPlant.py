"""
File name: test_fuelPlant
Date created: 27/11/2018
Feature: #Tests the functionality of the FuelPlant class.
"""
from unittest import TestCase
from src.plants.plant_type.fuel_plant import FuelPlant
from pytest import approx

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"


class TestFuelPlant(TestCase):
    def create_2018_ccgt_power_plant(self):
        fuel_plant = FuelPlant(name="Test_Plant", plant_type="CCGT", capacity_mw=1200, construction_year=2018,
                               average_load_factor=0.93, efficiency=0.54, pre_dev_period=3, construction_period=3,
                               operating_period=25, pre_dev_spend_years=[0.44, 0.44, 0.12],
                               construction_spend_years=[0.4, 0.4, 0.2], pre_dev_cost_per_mw=10000,
                               construction_cost_per_mw=500000, infrastructure=15100, fixed_o_and_m_per_mw=12200,
                               variable_o_and_m_per_mwh=3, insurance_cost_per_mw=2100, connection_cost_per_mw=3300)
        return fuel_plant

    def test_if_fuel_plant_correctly_calculates_fuel_costs_with_future_fuel_data(self):
        fuel_plant = self.create_2018_ccgt_power_plant()

        assert fuel_plant.fuel_costs([0]*6 + [9776160] * 25)[0] == 0
        assert fuel_plant.fuel_costs([0]*6 + [9776160] * 25)[4] == 0
        assert fuel_plant.fuel_costs([0]*6 + [9776160] * 25)[6] == approx(343559608)

    def test_total_costs(self):
        fuel_plant = self.create_2018_ccgt_power_plant()
        capex = [5280000, 5280000, 1440000, 240000000, 240000000, 135100000]
        opex = [0]*6 + [46488480] * 25
        fuel_costs = [0]*6 + [343559608] * 25
        assert fuel_plant.total_costs(capex=capex, opex=opex, fuel_costs=fuel_costs) == [5280000, 5280000, 1440000, 240000000, 240000000, 135100000] + [390048088]*25

    def test_lcoe_calculation(self):
        fuel_plant = self.create_2018_ccgt_power_plant()
        assert fuel_plant.calculate_lcoe(0.035) == approx(43.96005032)

    def test_carbon_emitted(self):
        fuel_plant = self.create_2018_ccgt_power_plant()
        assert fuel_plant.carbon_emitted() == approx([0]*6 + [3330411.84]*25)

    def test_carbon_costs(self):
        fuel_plant = self.create_2018_ccgt_power_plant()
        assert fuel_plant.carbon_costs()[7] == approx(92985098.57)
        assert fuel_plant.carbon_costs()[8] == approx(97680979.27)

    def test_carbon_sum(self):
        fuel_plant = self.create_2018_ccgt_power_plant()
        carbon_emitted = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 88255913.76, 92985098.57280001, 97680979.26720001, 102410164.08000001, 107139348.89280002, 111835229.5872, 116564414.4, 144040312.08, 171516209.76000002, 198992107.44000003, 226468005.12000003, 253943902.8, 281419800.48, 308895698.16, 336371595.84000003, 363847493.52000004, 391323391.20000005, 418799288.88000005, 446275186.56000006, 473751084.24000007, 501226981.9200001, 528702879.6, 556178777.2800001, 583654674.96, 611130572.6400001]
        assert fuel_plant.carbon_cost_total(carbon_emitted) == approx(7513409111.04)

