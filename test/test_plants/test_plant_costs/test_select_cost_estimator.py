"""
File name: test_select_cost_estimator
Date created: 04/12/2018
Feature: #Enter feature description here
"""
from unittest import TestCase
from pytest import approx
import pytest
from src.plants.plant_costs.estimate_costs.estimate_costs import select_cost_estimator
from src.plants.plant_type.non_fuel_plants.non_fuel_plant import NonFuelPlant
from src.plants.plant_type.fuel_plants.fuel_plant import FuelPlant


__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"


class TestSelectCostEstimator:
    def test_parameter_estimator_for_modern_small_gas_turbine_with_capacity_matching_data(self):
        assert select_cost_estimator(2018, "CCGT", 168.0) == {'connection_cost_per_mw': 3300.0,
                                                              'construction_cost_per_mw': 700000.0,
                                                              'fixed_o_and_m_per_mw': 28200.0,
                                                              'infrastructure': 13600.0,
                                                              'insurance_cost_per_mw': 2900.0,
                                                              'pre_dev_cost_per_mw': 60000.0,
                                                              'variable_o_and_m_per_mwh': 5.0, 'pre_dev_period': 3,
                                                              'operating_period': 25, 'construction_period': 3,
                                                              'efficiency': 0.34, 'average_load_factor': 0.93,
                                                              'construction_spend_years': [0.4, 0.4, 0.2],
                                                              'pre_dev_spend_years': [0.435, 0.435, 0.13]}

    def test_parameter_estimator_for_historic_gas_turbine_with_capacity_matching_data(self):
        CAPACITY = 1200
        START_YEAR = 1990
        PLANT_TYPE = "CCGT"
        parameters = select_cost_estimator(START_YEAR, PLANT_TYPE, CAPACITY)
        print(parameters)
        plant = FuelPlant(name="Modern Plant", plant_type=PLANT_TYPE,
                     capacity_mw=CAPACITY, construction_year=START_YEAR,
                     **parameters)
        assert plant.calculate_lcoe(0.05) == approx(82.55488)
        assert parameters['construction_cost_per_mw'] == approx(500*1000*6.4047971336)
        assert parameters['fixed_o_and_m_per_mw'] == approx(12200*6.4047971336)
        assert parameters['infrastructure'] == approx(15100*6.4047971336)
        assert parameters['insurance_cost_per_mw'] == approx(2100*6.4047971336)
        assert parameters['pre_dev_cost_per_mw'] == approx(10*1000*6.4047971336)
        assert parameters['variable_o_and_m_per_mwh'] == approx(3*6.4047971336)
        assert parameters['connection_cost_per_mw'] == approx(3300*6.4047971336)
        assert parameters['pre_dev_period'] == 3
        assert parameters['operating_period'] == 25
        assert parameters['construction_period'] == 3
        assert parameters['efficiency'] == 0.54
        assert parameters['average_load_factor'] == 0.93
        assert parameters['construction_spend_years'] == [0.4, 0.4, 0.2]
        assert parameters['pre_dev_spend_years'] == [0.44, 0.44, 0.12]

    def test_parameter_estimator_for_old_recip_gas_with_540_capacity(self):
        print(select_cost_estimator(1968, "Recip_gas", 540))

    def test_parameter_estimator_for_old_hydro(self):
        print(select_cost_estimator(1980, "Hydro", 100))

    def test_parameter_estimator_for_old_biomass(self):
        print(select_cost_estimator(1974, "Biomass_wood", 100))

    def test_parameter_estimator_for_small_old_hydro(self):
        parameters = select_cost_estimator(2002, "Hydro", 5)
        plant = NonFuelPlant(name="Modern Plant", plant_type="Hydro",
                             capacity_mw=5, construction_year=2002,
                             **parameters)
        print("parameters: {}".format(parameters))
        assert parameters['construction_spend_years'] == approx([1.0])
        assert parameters['pre_dev_spend_years'] == []
        assert parameters['operating_period'] == 35
        assert plant.calculate_lcoe(0.075) == approx(103.82602365344589)

    def test_parameter_estimator_for_5mw_modern_hydro(self):
        parameters = select_cost_estimator(2018, "Hydro", 5)
        assert parameters['construction_cost_per_mw'] == approx(3180.831826*1000)
        assert parameters['fixed_o_and_m_per_mw'] == approx(28885.4129)
        assert parameters['infrastructure'] == approx(241.1091019)
        assert parameters['insurance_cost_per_mw'] == approx(0)
        assert parameters['pre_dev_cost_per_mw'] == 0
        assert parameters['variable_o_and_m_per_mwh'] == approx(2.383363472)
        assert parameters['pre_dev_period'] == 0
        assert parameters['operating_period'] == 35
        assert parameters['construction_period'] == 0
        assert parameters['efficiency'] == 1
        assert parameters['average_load_factor'] == 0.4
        assert parameters['construction_spend_years'] == [1]
        assert parameters['pre_dev_spend_years'] == []

    def test_parameter_estimator_for_20kw_modern_hydro(self):
        parameters = select_cost_estimator(2018, "Hydro", 0.02)
        print("parameters: {}".format(parameters))
        assert parameters['construction_cost_per_mw'] == approx(6300*1000)
        assert parameters['fixed_o_and_m_per_mw'] == approx(83300)
        assert parameters['infrastructure'] == approx(0)
        assert parameters['insurance_cost_per_mw'] == approx(0)
        assert parameters['pre_dev_cost_per_mw'] == 0
        assert parameters['variable_o_and_m_per_mwh'] == approx(0)
        assert parameters['pre_dev_period'] == 0
        assert parameters['operating_period'] == 35
        assert parameters['construction_period'] == 0
        assert parameters['efficiency'] == 1
        assert parameters['average_load_factor'] == 0.6
        assert parameters['construction_spend_years'] == [1]
        assert parameters['pre_dev_spend_years'] == []

    def test_parameter_estimator_for_15mw_modern_hydro(self):
        parameters = select_cost_estimator(2018, "Hydro", 15)
        print("parameters: {}".format(parameters))
        assert parameters['construction_cost_per_mw'] == approx(3000*1000)
        assert parameters['fixed_o_and_m_per_mw'] == approx(45100)
        assert parameters['infrastructure'] == approx(0)
        assert parameters['insurance_cost_per_mw'] == approx(0)
        assert parameters['pre_dev_cost_per_mw'] == 60*1000
        assert parameters['variable_o_and_m_per_mwh'] == approx(6)
        assert parameters['pre_dev_period'] == 2
        assert parameters['operating_period'] == 41
        assert parameters['construction_period'] == 2
        assert parameters['efficiency'] == 1
        assert parameters['average_load_factor'] == 0.35
        assert parameters['construction_spend_years'] == [0.7, 0.3]
        assert parameters['pre_dev_spend_years'] == [0.77, 0.23]

    def test_parameter_estimator_for_5mw_old_hydro(self):
        parameters = select_cost_estimator(2012, "Hydro", 5)


        assert parameters['construction_cost_per_mw'] == approx(3180.831826*1000*1.2901268706825089)
        assert parameters['fixed_o_and_m_per_mw'] == approx(28885.4129*1.2901268706825089)
        assert parameters['infrastructure'] == approx(241.1091019*1.2901268706825089)
        assert parameters['insurance_cost_per_mw'] == approx(0)
        assert parameters['pre_dev_cost_per_mw'] == 0
        assert parameters['variable_o_and_m_per_mwh'] == approx(2.383363472*1.2901268706825089)
        assert parameters['pre_dev_period'] == 0
        assert parameters['operating_period'] == 35
        assert parameters['construction_period'] == 0
        assert parameters['efficiency'] == 1
        assert parameters['average_load_factor'] == 0.4
        assert parameters['construction_spend_years'] == [1]
        assert parameters['pre_dev_spend_years'] == []

    @pytest.mark.parametrize("year, plant_type, capacity, expected_output",
                             [
                                 # (1, "Hydro", 5, 103.82602365344589),
                                 # (2010, "Hydro", 5, 103.82602365344589),
                                 # (2011, "Hydro", 5, 103.82602365344589),
                                 # (2012, "Hydro", 5, 103.82602365344589),
                                 # (200, "PV", 1000, 440.87611118675716),
                                 # (2009, "PV", 1000, 440.87611118675716),
                                 # (2010, "PV", 1000, 440.87611118675716),
                                 # (2011, "PV", 1000, 427.94063296309986),
                                 # (2012, "PV", 1000, 489.4084693341632),
                                 # (2013, "PV", 1000, 225.93320235756386),
                                 # (2014, "PV", 1000, 194.4212102939174),
                                 # (2015, "PV", 1000, 159.505145013519),
                                 # (2016, "PV", 1000, 158.33803419634694),
                                 # (2017, "PV", 1000, 145.791592911747),
                                 # (1989, "Onshore", 1000, 227.84511564123014),
                                 # (1999, "Onshore", 1000, 148.07367387033398),
                                 # (2016, "Onshore", 1000, 76.71672469801007),
                                 # (1992, "CCGT", 1200, 82.55488000000001),
                                 # (2016, "CCGT", 1200, 103.69024),
                             ]
                             )
    def test_lcoe_calculations_for_non_fuel_plant(self, year, plant_type, capacity, expected_output):
        parameters = select_cost_estimator(year, plant_type, capacity)
        plant = NonFuelPlant(name="Modern Plant", plant_type=plant_type, capacity_mw=capacity, construction_year=year,
                             **parameters)
        lcoe = plant.calculate_lcoe(0.075)
        assert lcoe == approx(expected_output)

    @pytest.mark.parametrize("year, plant_type, capacity, expected_output",
                             [
                                 (1980, "CCGT", 1200, 82.55488000000001),
                                 (1992, "CCGT", 1200, 82.55488000000001),
                                 (2004, "CCGT", 1200, 93.58202434782609),
                                 (2015, "CCGT", 1200, 103.69024),
                                 (1981, "Coal", 1200, 177.19296),
                                 (1984, "Coal", 1200, 102.93248),
                                 (1992, "Coal", 1200, 89.86624),
                                 (1995, "Coal", 1200, 89.86624),
                                 (1995, "Coal", 390, 89.86624),
                             ]
                             )
    def test_lcoe_calculations_for_non_fuel_plant(self, year, plant_type, capacity, expected_output):
        parameters = select_cost_estimator(year, plant_type, capacity)
        print(parameters)
        plant = FuelPlant(name="Modern Plant", plant_type=plant_type, capacity_mw=capacity, construction_year=year,
                          **parameters)
        lcoe = plant.calculate_lcoe(0.05)
        assert lcoe == approx(expected_output)

    @pytest.mark.parametrize("year, plant_type, capacity",
                             [
                                 (-1, "Hydro", 5),
                                 (1, "Hydro", -6),
                                 ("string", "Hydro", -6),
                                 (1, "Hydro", "string"),
                             ]
                             )
    def test_lcoe_calculations_value_error_raised(self, year, plant_type, capacity):
        with pytest.raises(ValueError):
            select_cost_estimator(year, plant_type, capacity)

    # @pytest.mark.parametrize("year, plant_type, capacity, expected_output",
    #                          [
    #
    #                          ])
    # def test_various_historical_LCOE_calculations_for_PV(self, year, plant_type, capacity, expected_output):
    #     parameters = select_cost_estimator(year, plant_type, capacity)
    #     plant = NonFuelPlant(name="Modern Plant", plant_type=plant_type, capacity_mw=capacity, construction_year=year,
    #                          **parameters)
    #     lcoe = plant.calculate_lcoe(0.075)
    #     assert lcoe == approx(expected_output)


