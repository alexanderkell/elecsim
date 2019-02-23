"""
File name: test_select_cost_estimator
Date created: 04/12/2018
Feature: # Testing estimation capabilities of seelct_cost_estimator. Asserting if LCOE's are as expected, and individual cost data is returned.
"""
import pytest
from pytest import approx

from elecsim.plants.plant_costs.estimate_costs.estimate_costs import _select_cost_estimator
from elecsim.plants.plant_costs.estimate_costs.estimate_old_plant_cost_params.fuel_plant_calculations.fuel_plants_old_params import FuelOldPlantCosts
from elecsim.plants.plant_costs.estimate_costs.estimate_old_plant_cost_params.non_fuel_plant_calculations.non_fuel_plants_old_params import NonFuelOldPlantCosts
from elecsim.plants.plant_type.fuel_plant import FuelPlant
from elecsim.plants.plant_type.non_fuel_plant import NonFuelPlant

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"


class TestSelectCostEstimator:
    def test_parameter_estimator_for_modern_small_gas_turbine_with_capacity_matching_data(self):
        assert _select_cost_estimator(2018, "CCGT", 168.0) == {'connection_cost_per_mw': 3300.0,
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
        parameters = _select_cost_estimator(START_YEAR, PLANT_TYPE, CAPACITY)
        print(parameters)
        plant = FuelPlant(name="Modern Plant", plant_type=PLANT_TYPE,
                          capacity_mw=CAPACITY, construction_year=START_YEAR,
                          **parameters)
        assert plant.calculate_lcoe(0.05) == approx(82.55488)
        assert parameters['construction_cost_per_mw'] == approx(500 * 1000 * 4.7868450994)
        assert parameters['fixed_o_and_m_per_mw'] == approx(12200 * 4.7868450994)
        assert parameters['infrastructure'] == approx(15100 * 4.7868450994)
        assert parameters['insurance_cost_per_mw'] == approx(2100 * 4.7868450994)
        assert parameters['pre_dev_cost_per_mw'] == approx(10 * 1000 * 4.7868450994)
        assert parameters['variable_o_and_m_per_mwh'] == approx(3 * 4.7868450994)
        assert parameters['connection_cost_per_mw'] == approx(3300 * 4.7868450994)
        assert parameters['pre_dev_period'] == 3
        assert parameters['operating_period'] == 25
        assert parameters['construction_period'] == 3
        assert parameters['efficiency'] == 0.54
        assert parameters['average_load_factor'] == 0.93
        assert parameters['construction_spend_years'] == [0.4, 0.4, 0.2]
        assert parameters['pre_dev_spend_years'] == [0.44, 0.44, 0.12]

    def test_parameter_estimator_for_old_recip_gas_with_540_capacity(self):
        print(_select_cost_estimator(1968, "Recip_gas", 540))

    def test_parameter_estimator_for_old_hydro(self):
        print(_select_cost_estimator(1980, "Hydro", 100))

    def test_parameter_estimator_for_old_biomass(self):
        print(_select_cost_estimator(1974, "Biomass_wood", 100))

    def test_parameter_estimator_for_small_old_hydro(self):
        parameters = _select_cost_estimator(2002, "Hydro", 5)
        plant = NonFuelPlant(name="Modern Plant", plant_type="Hydro",
                             capacity_mw=5, construction_year=2002,
                             **parameters)
        print("parameters: {}".format(parameters))
        assert parameters['construction_spend_years'] == approx([1.0])
        assert parameters['pre_dev_spend_years'] == []
        assert parameters['operating_period'] == 35
        assert plant.calculate_lcoe(0.075) == approx(103.82602365344589)

    def test_parameter_estimator_for_5mw_modern_hydro(self):
        parameters = _select_cost_estimator(2018, "Hydro", 5)
        assert parameters['construction_cost_per_mw'] == approx(3180.831826 * 1000)
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
        parameters = _select_cost_estimator(2018, "Hydro", 0.02)
        print("parameters: {}".format(parameters))
        assert parameters['construction_cost_per_mw'] == approx(6300 * 1000)
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
        parameters = _select_cost_estimator(2018, "Hydro", 15)
        print("parameters: {}".format(parameters))
        assert parameters['construction_cost_per_mw'] == approx(3000 * 1000)
        assert parameters['fixed_o_and_m_per_mw'] == approx(45100)
        assert parameters['infrastructure'] == approx(0)
        assert parameters['insurance_cost_per_mw'] == approx(0)
        assert parameters['pre_dev_cost_per_mw'] == 60 * 1000
        assert parameters['variable_o_and_m_per_mwh'] == approx(6)
        assert parameters['pre_dev_period'] == 2
        assert parameters['operating_period'] == 41
        assert parameters['construction_period'] == 2
        assert parameters['efficiency'] == 1
        assert parameters['average_load_factor'] == 0.35
        assert parameters['construction_spend_years'] == [0.7, 0.3]
        assert parameters['pre_dev_spend_years'] == [0.77, 0.23]

    def test_parameter_estimator_for_5mw_old_hydro(self):
        parameters = _select_cost_estimator(2012, "Hydro", 5)

        assert parameters['construction_cost_per_mw'] == approx(3180.831826 * 1000 * 1.2901268706825089)
        assert parameters['fixed_o_and_m_per_mw'] == approx(28885.4129 * 1.2901268706825089)
        assert parameters['infrastructure'] == approx(241.1091019 * 1.2901268706825089)
        assert parameters['insurance_cost_per_mw'] == approx(0)
        assert parameters['pre_dev_cost_per_mw'] == 0
        assert parameters['variable_o_and_m_per_mwh'] == approx(2.383363472 * 1.2901268706825089)
        assert parameters['pre_dev_period'] == 0
        assert parameters['operating_period'] == 35
        assert parameters['construction_period'] == 0
        assert parameters['efficiency'] == 1
        assert parameters['average_load_factor'] == 0.4
        assert parameters['construction_spend_years'] == [1]
        assert parameters['pre_dev_spend_years'] == []

    @pytest.mark.parametrize("year, plant_type, capacity, discount_rate, expected_output",
                             [
                                 (1, "Hydro", 5, 0.075, 103.82602365344589),
                                 (2010, "Hydro", 5, 0.075, 103.82602365344589),
                                 (2011, "Hydro", 5, 0.075, 103.82602365344589),
                                 (2012, "Hydro", 5, 0.075, 103.82602365344589),
                                 (1, "Hydro", 20, 0.075, 135.22924001633953),
                                 (2010, "Hydro", 50, 0.075, 135.22924001633953),
                                 (2011, "Hydro", 60, 0.075, 135.22924001633953),
                                 (2012, "Hydro", 70, 0.075, 135.22924001633953),
                                 (200, "PV", 1000, 0.075, 440.87611118675716),
                                 (2009, "PV", 1000, 0.075, 440.87611118675716),
                                 (2010, "PV", 1000, 0.075, 440.87611118675716),
                                 (2011, "PV", 1000, 0.075, 427.94063296309986),
                                 (2012, "PV", 1, 0.075, 489.4084693341632),
                                 (2013, "PV", 1.3, 0.075, 225.93320235756386),
                                 (2014, "PV", 9, 0.075, 194.4212102939174),
                                 (2015, "PV", 1000, 0.075, 159.505145013519),
                                 (2016, "PV", 1000, 0.075, 158.33803419634694),
                                 (2017, "PV", 1000, 0.075, 145.791592911747),
                                 (1989, "Onshore", 1000, 0.075, 227.84511564123014),
                                 (1999, "Onshore", 1000, 0.075, 148.07367387033398),
                                 (1999, "Onshore", 1, 0.075, 148.07367387033398),
                                 (1999, "Onshore", 2.3, 0.075, 148.07367387033398),
                                 (1999, "Onshore", 100000.54, 0.075, 148.07367387033398),
                                 (2016, "Onshore", 1000, 0.075, 76.71672469801007),
                                 (1989, "Offshore", 1000, 0.08900000000000001, 148.03206144000004),
                                 (2006, "Offshore", 1000, 0.08900000000000001, 148.03206144000004),
                                 (2006, "Offshore", 1, 0.08900000000000001, 148.03206144000004),
                                 (2006, "Offshore", 2.3, 0.08900000000000001, 148.03206144000004),
                                 (2006, "Offshore", 100000.54, 0.08900000000000001, 148.03206144000004),
                                 (2016, "Offshore", 1000, 0.08900000000000001, 115.486777344),
                             ]
                             )
    def test_lcoe_calculations_for_non_fuel_plant(self, year, plant_type, capacity, discount_rate, expected_output):
        parameters = _select_cost_estimator(year, plant_type, capacity)
        plant = NonFuelPlant(name="Modern Plant", plant_type=plant_type, capacity_mw=capacity, construction_year=year,
                             **parameters)
        lcoe = plant.calculate_lcoe(discount_rate)
        assert lcoe == approx(expected_output)

    @pytest.mark.parametrize("year, plant_type, capacity, discount_rate, expected_output",
                             [
                                 (1980, "CCGT", 1200, 0.05, 82.55488000000001),
                                 (1992, "CCGT", 1200, 0.05, 82.55488000000001),
                                 (2004, "CCGT", 1200, 0.05, 93.58202434782609),
                                 (2015, "CCGT", 1200, 0.05, 103.69024),
                                 (1981, "Coal", 1200, 0.05, 177.19296),
                                 (1984, "Coal", 1200, 0.05, 102.93248),
                                 (1992, "Coal", 1200, 0.05, 89.86624),
                                 (1995, "Coal", 1200, 0.05, 89.86624),
                                 (1995, "Coal", 390, 0.05, 89.86624),
                                 (1995, "Coal", 552.0, 0.05, 89.86624),
                                 (1995, "Coal", 624.0, 0.05, 89.86624),
                                 (1995, "Coal", 652.0, 0.05, 89.86624),
                                 (1995, "Coal", 760.0, 0.05, 89.86624),
                                 (1995, "Coal", 734.0, 0.05, 89.86624),
                                 (1995, "Coal", 624.0, 0.05, 89.86624),
                                 (1984, "Coal", 624.0, 0.05, 102.93248),
                                 (1984, "Coal", 54.5, 0.05, 102.93248),
                                 (2015, "Nuclear", 624.0, 0.05, 82.82112),
                                 (1981, "Nuclear", 624.0, 0.05, 123.83232),
                                 (1984, "Nuclear", 624.0, 0.05, 66.99008),
                                 (1984, "Nuclear", 1, 0.05, 66.99008),
                                 (1984, "Nuclear", 1.3, 0.05, 66.99008),
                                 (1984, "Nuclear", 10000000, 0.05, 66.99008),
                                 (1983, "Nuclear", 10000000, 0.05, 85.93749333333335),
                                 (1910, "Nuclear", 10000000, 0.05, 123.83232000000001),
                                 (2016, 'Biomass_wood', 65, 0.075, 87.5333112879068),
                                 (1960, 'Biomass_wood', 65, 0.075, 87.5333112879068),
                                 (2013, 'Biomass_wood', 65, 0.075, 87.5333112879068),
                                 (2016, 'Biomass_wood', 1000, 0.075, 87.5333112879068),
                                 (2016, 'Biomass_wood', 1, 0.075, 87.5333112879068),
                                 (2017, 'Biomass_wood', 65, 0.075, 87.5333112879068),
                                 (2010, 'Biomass_poultry_litter', 100, 0.075, 87.5333112879068),
                                 (2005, 'Biomass_poultry_litter', 100, 0.075, 87.5333112879068),
                                 (2015, 'Biomass_poultry_litter', 10000, 0.075, 87.5333112879068),
                                 (2015, 'Biomass_poultry_litter', 1.3, 0.075, 87.5333112879068),
                                 (2010, 'Biomass_meat', 100, 0.075, 87.5333112879068),
                                 (2005, 'Biomass_meat', 100, 0.075, 87.5333112879068),
                                 (2015, 'Biomass_meat', 10000, 0.075, 87.5333112879068),
                                 (2015, 'Biomass_meat', 1.3, 0.075, 87.5333112879068),
                                 (2010, 'Biomass_straw', 100, 0.075, 87.5333112879068),
                                 (2005, 'Biomass_straw', 100, 0.075, 87.5333112879068),
                                 (2015, 'Biomass_straw', 10000, 0.075, 87.5333112879068),
                                 (2015, 'Biomass_straw', 1.3, 0.075, 87.5333112879068),
                             ]
                             )
    def test_lcoe_calculations_for_fuel_plant(self, year, plant_type, capacity, discount_rate, expected_output):
        parameters = _select_cost_estimator(year, plant_type, capacity)
        plant = FuelPlant(name="TestPlant", plant_type=plant_type, capacity_mw=capacity, construction_year=year,
                          **parameters)
        lcoe = plant.calculate_lcoe(discount_rate)
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
            _select_cost_estimator(year, plant_type, capacity)

    @pytest.mark.parametrize("year, plant_type, capacity",
                             [
                                 (1980, "CCGT", 1200),
                                 (1992, "CCGT", 1200),
                                 (2004, "CCGT", 1200),
                                 (2015, "CCGT", 1200),
                                 (1981, "Coal", 1200),
                                 (1984, "Coal", 1200),
                                 (1992, "Coal", 1200),
                                 (1995, "Coal", 1200),
                                 (1995, "Coal", 390),
                                 (1995, "Coal", 552.0),
                                 (1995, "Coal", 624.0),
                                 (1995, "Coal", 652.0),
                                 (1995, "Coal", 760.0),
                                 (1995, "Coal", 734.0),
                                 (1995, "Coal", 624.0),
                                 (1984, "Coal", 624.0),
                                 (1984, "Coal", 54.5),
                                 (2015, "Nuclear", 624.0),
                                 (1981, "Nuclear", 624.0),
                                 (1984, "Nuclear", 624.0),
                                 (1984, "Nuclear", 1),
                                 (1984, "Nuclear", 1.3),
                                 (1984, "Nuclear", 10000000),
                                 (1983, "Nuclear", 10000000),
                                 (1910, "Nuclear", 10000000),
                                 (2016, 'Biomass_wood', 65),
                                 (1960, 'Biomass_wood', 65),
                                 (2013, 'Biomass_wood', 65),
                                 (2016, 'Biomass_wood', 1000),
                                 (2016, 'Biomass_wood', 1),
                                 (2017, 'Biomass_wood', 65),
                                 (2010, 'Biomass_poultry_litter', 100),
                                 (2005, 'Biomass_poultry_litter', 100),
                                 (2015, 'Biomass_poultry_litter', 1000),
                                 (2015, 'Biomass_poultry_litter', 1.3),
                                 (2010, 'Biomass_meat', 100),
                                 (2005, 'Biomass_meat', 100),
                                 (2015, 'Biomass_meat', 10000),
                                 (2015, 'Biomass_meat', 1.3),
                                 (2010, 'Biomass_straw', 100),
                                 (2005, 'Biomass_straw', 100),
                                 (2015, 'Biomass_straw', 10000),
                                 (2015, 'Biomass_straw', 1.3),
                             ])
    def test_estimated_fuel_plant_parameters_scaled_equally(self, year, plant_type, capacity):
        parameters = _select_cost_estimator(start_year=year, plant_type=plant_type, capacity=capacity)
        fuel_plant_params_calc = FuelOldPlantCosts(year, plant_type, capacity)
        modern_parameters = fuel_plant_params_calc.estimate_modern_parameters()

        divided_params = {key: round(parameters[key] / modern_parameters[key], 4) for key in modern_parameters if
                          key in parameters}
        assert len(set(divided_params.values())) == 1

    @pytest.mark.parametrize("year, plant_type, capacity",
                             [
                                 (1, "Hydro", 5),
                                 (2010, "Hydro", 5),
                                 (2011, "Hydro", 5),
                                 (2012, "Hydro", 5),
                                 (1, "Hydro", 20),
                                 (2010, "Hydro", 50),
                                 (2011, "Hydro", 60),
                                 (2012, "Hydro", 70),
                                 (200, "PV", 1000),
                                 (2009, "PV", 1000),
                                 (2010, "PV", 1000),
                                 (2011, "PV", 1000),
                                 (2012, "PV", 1),
                                 (2013, "PV", 1.3),
                                 (2014, "PV", 9),
                                 (2015, "PV", 1000),
                                 (2016, "PV", 1000),
                                 (2017, "PV", 1000),
                                 (1989, "Onshore", 1000),
                                 (1999, "Onshore", 1000),
                                 (1999, "Onshore", 1),
                                 (1999, "Onshore", 2.3),
                                 (1999, "Onshore", 100000.54),
                                 (2016, "Onshore", 1000),
                                 (1989, "Offshore", 1000),
                                 (2006, "Offshore", 1000),
                                 (2006, "Offshore", 1),
                                 (2006, "Offshore", 2.3),
                                 (2006, "Offshore", 100000.54),
                                 (2016, "Offshore", 1000),
                             ])
    def test_estimated_non_fuel_plant_parameters_scaled_equally(self, year, plant_type, capacity):
        parameters = _select_cost_estimator(start_year=year, plant_type=plant_type, capacity=capacity)
        nonfuel_calculator = NonFuelOldPlantCosts(year=year, plant_type=plant_type, capacity=capacity)

        nonfuel_calculator.get_params_to_scale()

        modern_parameters = nonfuel_calculator.estimated_modern_plant_parameters

        divided_params = {key: round(parameters[key] / modern_parameters[key], 4) for key in modern_parameters if
                          key not in nonfuel_calculator.dict_to_ignore and modern_parameters[key] != 0}
        assert len(set(divided_params.values())) == 1
