'''
File name: test_predictPlantStatistics
Date created: 27/11/2018
Feature: #Enter feature description here
'''
from unittest import TestCase

import pytest

from src.plants.plant_costs.estimate_costs.estimate_modern_power_plant_costs.predict_modern_plant_costs import \
    PredictModernPlantParameters

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"


class TestPredictPlantParameters(TestCase):
    def test_parameter_estimation_for_ccgt_1200(self):
        estimated_plant_parameters = PredictModernPlantParameters("CCGT", 1200, 2018).parameter_estimation()
        assert estimated_plant_parameters['connection_cost_per_mw'] == 3300
        assert estimated_plant_parameters['construction_cost_per_mw'] == 500000
        assert estimated_plant_parameters['fixed_o_and_m_per_mw'] == 12200
        assert estimated_plant_parameters['infrastructure'] == 15100
        assert estimated_plant_parameters['insurance_cost_per_mw'] == 2100
        assert estimated_plant_parameters['pre_dev_cost_per_mw'] == 10000
        assert estimated_plant_parameters['variable_o_and_m_per_mwh'] == 3.00
        assert estimated_plant_parameters['pre_dev_period'] == 3
        assert estimated_plant_parameters['operating_period'] == 25
        assert estimated_plant_parameters['construction_period'] == 3
        assert estimated_plant_parameters['efficiency'] == 0.54
        assert estimated_plant_parameters['average_load_factor'] == 0.93
        assert estimated_plant_parameters['construction_spend_years'] == [0.4, 0.4, 0.2]
        assert estimated_plant_parameters['pre_dev_spend_years'] == [0.44, 0.44, 0.12]

    def test_parameter_estimation_for_ccgt_1335_5(self):
        estimated_plant_parameters = PredictModernPlantParameters("CCGT", 1335.5, 2018).parameter_estimation()
        assert estimated_plant_parameters['connection_cost_per_mw'] == 3300
        assert estimated_plant_parameters['construction_cost_per_mw'] == 500000
        assert estimated_plant_parameters['fixed_o_and_m_per_mw'] == 11800
        assert estimated_plant_parameters['infrastructure'] == 15100
        assert estimated_plant_parameters['insurance_cost_per_mw'] == 2000
        assert estimated_plant_parameters['pre_dev_cost_per_mw'] == 10000
        assert estimated_plant_parameters['variable_o_and_m_per_mwh'] == 3.00
        assert estimated_plant_parameters['pre_dev_period'] == 3
        assert estimated_plant_parameters['operating_period'] == 25
        assert estimated_plant_parameters['construction_period'] == 3
        assert estimated_plant_parameters['efficiency'] == 0.54
        assert estimated_plant_parameters['average_load_factor'] == 0.93
        assert estimated_plant_parameters['construction_spend_years'] == [0.4, 0.4, 0.2]
        assert estimated_plant_parameters['pre_dev_spend_years'] == [0.44, 0.44, 0.12]

    def setup_method(self, module):
        self.initial_stub_cost_parameters = ['Connect_system_cost-Medium _', 'Constr_cost-Medium _',
                                             'Fixed_cost-Medium _',
                                             'Infra_cost-Medium _', 'Insurance_cost-Medium _', 'Pre_dev_cost-Medium _',
                                             'Var_cost-Medium _']

    def test_creation_of_parameter_names_2018(self):
        predict_plant = PredictModernPlantParameters("CCGT", 1200, 2018)
        cost_parameter_variables = predict_plant._create_parameter_names(self.initial_stub_cost_parameters)

        assert cost_parameter_variables == ['Connect_system_cost-Medium _2018', 'Constr_cost-Medium _2018',
                                            'Fixed_cost-Medium _2018',
                                            'Infra_cost-Medium _2018', 'Insurance_cost-Medium _2018',
                                            'Pre_dev_cost-Medium _2018',
                                            'Var_cost-Medium _2018']

    def test_creation_of_parameter_names_2019(self):
        predict_plant = PredictModernPlantParameters("CCGT", 1200, 2019)
        cost_parameter_variables = predict_plant._create_parameter_names(self.initial_stub_cost_parameters)

        assert cost_parameter_variables == ['Connect_system_cost-Medium _2018', 'Constr_cost-Medium _2018',
                                            'Fixed_cost-Medium _2018',
                                            'Infra_cost-Medium _2018', 'Insurance_cost-Medium _2018',
                                            'Pre_dev_cost-Medium _2018',
                                            'Var_cost-Medium _2018']

    def test_creation_of_parameter_names_2020(self):
        PredictPlant = PredictModernPlantParameters("CCGT", 1200, 2020)
        cost_parameter_variables = PredictPlant._create_parameter_names(self.initial_stub_cost_parameters)

        assert cost_parameter_variables == ['Connect_system_cost-Medium _2020', 'Constr_cost-Medium _2020',
                                            'Fixed_cost-Medium _2020',
                                            'Infra_cost-Medium _2020', 'Insurance_cost-Medium _2020',
                                            'Pre_dev_cost-Medium _2020',
                                            'Var_cost-Medium _2020']

    def test_creation_of_parameter_names_2021(self):
        PredictPlant = PredictModernPlantParameters("CCGT", 1200, 2021)
        cost_parameter_variables = PredictPlant._create_parameter_names(self.initial_stub_cost_parameters)

        assert cost_parameter_variables == ['Connect_system_cost-Medium _2020', 'Constr_cost-Medium _2020',
                                            'Fixed_cost-Medium _2020',
                                            'Infra_cost-Medium _2020', 'Insurance_cost-Medium _2020',
                                            'Pre_dev_cost-Medium _2020',
                                            'Var_cost-Medium _2020']

    def test_creation_of_parameter_names_2022(self):
        PredictPlant = PredictModernPlantParameters("CCGT", 1200, 2022)
        cost_parameter_variables = PredictPlant._create_parameter_names(self.initial_stub_cost_parameters)

        assert cost_parameter_variables == ['Connect_system_cost-Medium _2020', 'Constr_cost-Medium _2020',
                                            'Fixed_cost-Medium _2020',
                                            'Infra_cost-Medium _2020', 'Insurance_cost-Medium _2020',
                                            'Pre_dev_cost-Medium _2020',
                                            'Var_cost-Medium _2020']

    def test_creation_of_parameter_names_2023(self):
        PredictPlant = PredictModernPlantParameters("CCGT", 1200, 2023)
        cost_parameter_variables = PredictPlant._create_parameter_names(self.initial_stub_cost_parameters)

        assert cost_parameter_variables == ['Connect_system_cost-Medium _2020', 'Constr_cost-Medium _2020',
                                            'Fixed_cost-Medium _2020',
                                            'Infra_cost-Medium _2020', 'Insurance_cost-Medium _2020',
                                            'Pre_dev_cost-Medium _2020',
                                            'Var_cost-Medium _2020']

    def test_creation_of_parameter_names_2024(self):
        PredictPlant = PredictModernPlantParameters("CCGT", 1200, 2024)
        cost_parameter_variables = PredictPlant._create_parameter_names(self.initial_stub_cost_parameters)

        assert cost_parameter_variables == ['Connect_system_cost-Medium _2020', 'Constr_cost-Medium _2020',
                                            'Fixed_cost-Medium _2020',
                                            'Infra_cost-Medium _2020', 'Insurance_cost-Medium _2020',
                                            'Pre_dev_cost-Medium _2020',
                                            'Var_cost-Medium _2020']

    def test_creation_of_parameter_names_2025(self):
        PredictPlant = PredictModernPlantParameters("CCGT", 1200, 2025)
        cost_parameter_variables = PredictPlant._create_parameter_names(self.initial_stub_cost_parameters)

        assert cost_parameter_variables == ['Connect_system_cost-Medium _2025', 'Constr_cost-Medium _2025',
                                            'Fixed_cost-Medium _2025',
                                            'Infra_cost-Medium _2025', 'Insurance_cost-Medium _2025',
                                            'Pre_dev_cost-Medium _2025',
                                            'Var_cost-Medium _2025']

    def test_creation_of_parameter_names_high_year(self):
        PredictPlant = PredictModernPlantParameters("CCGT", 1200, 200000)
        cost_parameter_variables = PredictPlant._create_parameter_names(self.initial_stub_cost_parameters)

        assert cost_parameter_variables == ['Connect_system_cost-Medium _2025', 'Constr_cost-Medium _2025',
                                            'Fixed_cost-Medium _2025',
                                            'Infra_cost-Medium _2025', 'Insurance_cost-Medium _2025',
                                            'Pre_dev_cost-Medium _2025',
                                            'Var_cost-Medium _2025']

    def test_creation_of_parameter_names_low_year(self):
        PredictPlant = PredictModernPlantParameters("CCGT", 1200, 0)
        cost_parameter_variables = PredictPlant._create_parameter_names(self.initial_stub_cost_parameters)

        assert cost_parameter_variables == ['Connect_system_cost-Medium _2018', 'Constr_cost-Medium _2018',
                                            'Fixed_cost-Medium _2018',
                                            'Infra_cost-Medium _2018', 'Insurance_cost-Medium _2018',
                                            'Pre_dev_cost-Medium _2018',
                                            'Var_cost-Medium _2018']

    def test_check_plant_exists_fails_with_no_data(self):
        with pytest.raises(ValueError) as excinfo:
            PredictModernPlantParameters("Fake_Plant", 1200, 2018).check_plant_exists(
                {'connection_cost_per_mw': 0, 'construction_cost_per_mw': 0, 'fixed_o_and_m_per_mw': 0,
                 'infrastructure': 0, 'insurance_cost_per_mw': 0, 'pre_dev_cost_per_mw': 0,
                 'variable_o_and_m_per_mwh': 0, 'pre_dev_period': 0, 'operating_period': 0, 'construction_period': 0,
                 'efficiency': 0, 'average_load_factor': 0, 'construction_spend_years': 0, 'pre_dev_spend_years': 0})
        assert "No cost data for power plant of type: Fake_Plant" in str(excinfo.value)

    def test_check_plant_exists_with_data(self):
        PredictModernPlantParameters("Fake_Plant", 1200, 2018).check_plant_exists(
                {'connection_cost_per_mw': 100, 'construction_cost_per_mw': 100, 'fixed_o_and_m_per_mw': 100,
                 'infrastructure': 100, 'insurance_cost_per_mw': 100, 'pre_dev_cost_per_mw': 100,
                 'variable_o_and_m_per_mwh': 100, 'pre_dev_period': 100, 'operating_period': 100, 'construction_period': 100,
                 'efficiency': 100, 'average_load_factor': 100, 'construction_spend_years': 100, 'pre_dev_spend_years': 100})


    def test_estimate_non_interpolatable_parameters_for_ccgt_1200(self):
        predict_modern_parameters = PredictModernPlantParameters("CCGT", 1200, 2018)

        assert predict_modern_parameters._estimate_non_interpolatable_parameters("Pre_Dur") == 3
        assert predict_modern_parameters._estimate_non_interpolatable_parameters("Operating_Period") ==25
        assert predict_modern_parameters._estimate_non_interpolatable_parameters("Constr_Dur") == 3
        assert predict_modern_parameters._estimate_non_interpolatable_parameters("Efficiency") == 0.54
        assert predict_modern_parameters._estimate_non_interpolatable_parameters("Average_Load_Factor") == 0.93

    def test_estimate_non_interpolatable_parameters_for_ccgt_1450(self):
        predict_modern_parameters = PredictModernPlantParameters("CCGT", 1450, 2018)

        assert predict_modern_parameters._estimate_non_interpolatable_parameters("Pre_Dur") == 3
        assert predict_modern_parameters._estimate_non_interpolatable_parameters("Operating_Period") ==25
        assert predict_modern_parameters._estimate_non_interpolatable_parameters("Constr_Dur") == 3
        assert predict_modern_parameters._estimate_non_interpolatable_parameters("Efficiency") == 0.53
        assert predict_modern_parameters._estimate_non_interpolatable_parameters("Average_Load_Factor") == 0.93

    def test_payment_spread_estimator_for_ccgt_1200(self):
        predict_modern_parameters = PredictModernPlantParameters("CCGT", 1200, 2018)

        assert predict_modern_parameters._payment_spread_estimator("Constr") == [0.4, 0.4, 0.2]
        assert predict_modern_parameters._payment_spread_estimator("Pre") == [0.44, 0.44, 0.12]

    def test_payment_spread_estimator_for_ccgt_160(self):
        predict_modern_parameters = PredictModernPlantParameters("CCGT", 160, 2018)

        assert predict_modern_parameters._payment_spread_estimator("Constr") == [0.4, 0.4, 0.2]
        assert predict_modern_parameters._payment_spread_estimator("Pre") == [0.435, 0.435, 0.13]

