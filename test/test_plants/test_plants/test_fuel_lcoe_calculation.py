"""
File name: test_fuelPlant
Date created: 27/11/2018
Feature: #Tests the functionality of the FuelPlant class.
"""
from unittest import TestCase

from pytest import approx

from elecsim.role.plants.costs.fuel_plant_cost_calculations import FuelPlantCostCalculations

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"


class TestFuelLCOECalculation(TestCase):

    def create_2018_ccgt_power_plant(self):
        lcoe_calc_obj = FuelPlantCostCalculations(plant_type="CCGT", capacity_mw=1200, construction_year=2011,
                                                  average_load_factor=0.93, efficiency=0.54, pre_dev_period=3, construction_period=3,
                                                  operating_period=25, pre_dev_spend_years=[0.44, 0.44, 0.12],
                                                  construction_spend_years=[0.4, 0.4, 0.2], pre_dev_cost_per_mw=10000,
                                                  construction_cost_per_mw=500000, infrastructure=15100, fixed_o_and_m_per_mw=12200,
                                                  variable_o_and_m_per_mwh=3, insurance_cost_per_mw=2100, connection_cost_per_mw=3300)
        return lcoe_calc_obj

    def test_if_fuel_plant_correctly_calculates_fuel_costs(self):
        fuel_plant = self.create_2018_ccgt_power_plant()

        assert fuel_plant._fuel_costs([0]*6 + [9776160] * 25)[0] == 0
        assert fuel_plant._fuel_costs([0]*6 + [9776160] * 25)[4] == 0
        assert fuel_plant._fuel_costs([0]*6 + [9776160] * 25)[6] == approx(275932025.48)
        assert fuel_plant._fuel_costs([0]*6 + [9776160] * 25) == approx([0]*6+[275932025.48]+[343559608.00]*24)

    def test_total_costs(self):
        fuel_plant = self.create_2018_ccgt_power_plant()
        capex = [5280000, 5280000, 1440000, 240000000, 240000000, 135100000]
        opex = [0]*6 + [46488480] * 25
        fuel_costs = [0]*6 + [343559608] * 25
        carbon_costs = [0, 0, 0, 0, 0, 0, 88255913.76, 92985098.57, 97680979.27, 102410164.1, 107139348.9, 111835229.6, 116564414.4, 144040312.1, 171516209.8, 198992107.4, 226468005.1, 253943902.8, 281419800.5, 308895698.2, 336371595.8, 363847493.5, 391323391.2, 418799288.9, 446275186.6, 473751084.2, 501226981.9, 528702879.6, 556178777.3, 583654675, 611130572.6]
        assert fuel_plant._total_costs(capex=capex, opex=opex, fuel_costs=fuel_costs, carbon_costs=carbon_costs) == approx([5280000, 5280000, 1440000, 240000000, 240000000, 135100000, 478304001.8, 483033186.6, 487729067.3, 492458252.1, 497187436.9, 501883317.6, 506612502.4, 534088400.1, 561564297.8, 589040195.4, 616516093.1, 643991990.8, 671467888.5, 698943786.2, 726419683.8, 753895581.5, 781371479.2, 808847376.9, 836323274.6, 863799172.2, 891275069.9, 918750967.6, 946226865.3, 973702763, 1001178661])

    def test_lcoe_calculation(self):
        fuel_plant = self.create_2018_ccgt_power_plant()
        assert fuel_plant.calculate_lcoe(0.1) == approx(57.87418159)

    def test_carbon_emitted(self):
        fuel_plant = self.create_2018_ccgt_power_plant()
        assert fuel_plant._carbon_emitted() == approx([0]*6 + [3330411.84]*25)

    def test_carbon_costs(self):
        fuel_plant = self.create_2018_ccgt_power_plant()
        assert fuel_plant._carbon_costs() == approx([0, 0, 0, 0, 0, 0, 60213846.07, 60213846.07, 59947413.12, 64676597.93, 69372478.63, 74101663.44, 78830848.25, 83526728.95, 88255913.76, 92985098.57, 97680979.27, 102410164.1, 107139348.9, 111835229.6, 116564414.4, 144040312.1, 171516209.8, 198992107.4, 226468005.1, 253943902.8, 281419800.5, 308895698.2, 336371595.8, 363847493.5, 391323391.2])


    def test_carbon_sum(self):
        fuel_plant = self.create_2018_ccgt_power_plant()
        carbon_emitted = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 88255913.76, 92985098.57280001, 97680979.26720001, 102410164.08000001, 107139348.89280002, 111835229.5872, 116564414.4, 144040312.08, 171516209.76000002, 198992107.44000003, 226468005.12000003, 253943902.8, 281419800.48, 308895698.16, 336371595.84000003, 363847493.52000004, 391323391.20000005, 418799288.88000005, 446275186.56000006, 473751084.24000007, 501226981.9200001, 528702879.6, 556178777.2800001, 583654674.96, 611130572.6400001]
        assert fuel_plant._carbon_cost_total(carbon_emitted) == approx(7513409111.04)

