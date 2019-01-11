from src.role.investment.predict_load_duration_prices import PredictPriceDurationCurve
from src.plants.plant_costs.estimate_costs.estimate_costs import create_power_plant
from src.agents.generation_company.gen_co import GenCo
import numpy as np
from src.scenario.scenario_data import segment_demand, segment_time

"""
File name: test_predictLoadDuration
Date created: 11/01/2019
Feature: #Enter feature description here
"""
from unittest.mock import Mock
import pytest
import logging
logger = logging.getLogger(__name__)
__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"

logging.basicConfig(level=logging.DEBUG)

class TestPredictLoadDuration:

    def test_predict_load_curve_price(self):

        model = Mock()
        model.year_number = 2025
        model.step_number = 6

        model.Demand.segment_consumption = [52152, 45209, 42206, 39585, 37480, 35505, 34182, 33188, 32315, 31567, 30721, 29865, 28935, 27888, 26760, 25520, 24327, 23127, 21964, 17568]
        model.Demand.segment_hours = [8752.5, 8291.83, 7831.17, 7370.5, 6909.92, 6449.25, 5988.58, 5527.92, 5067.25, 4606.58, 4146, 3685.33, 3224.67, 2764, 2303.33, 1842.67, 1382.08, 921.42, 460.75, 0.08]


        plant1 = create_power_plant("plant1", 2016, "CCGT", 1200)
        plant2 = create_power_plant("plant2", 2015, "CCGT", 1200)
        plant3 = create_power_plant("plant3", 2014, "CCGT", 1200)
        plant4 = create_power_plant("plant4", 2020, "CCGT", 1200)
        plant5 = create_power_plant("plant5", 2021, "CCGT", 1200)
        plant6 = create_power_plant("plant6", 2035, "CCGT", 1200)

        plants = [plant1, plant2, plant3, plant4, plant5, plant6]
        all_variable_costs = [plant1.variable_o_and_m_per_mwh, plant2.variable_o_and_m_per_mwh, plant3.variable_o_and_m_per_mwh, plant4.variable_o_and_m_per_mwh, plant5.variable_o_and_m_per_mwh, plant6.variable_o_and_m_per_mwh]
        index_of_max_var_o_m_costs = np.argmax(all_variable_costs)
        plant_with_highest_o_m = plants[index_of_max_var_o_m_costs]
        gen_co1 = GenCo(1, model, "genco1", 0.02, 4)
        gen_co1.plants = [plant1, plant2]

        gen_co2 = GenCo(1, model, "genco2", 0.02, 4)
        gen_co2.plants = [plant3, plant4, plant5, plant6]

        model.schedule.agents = [gen_co1, gen_co2]

        predict_price_duration_curve = PredictPriceDurationCurve(model=model)
        predicted_price_duration_curve = predict_price_duration_curve.predict_load_curve_price(1.1)
        assert predicted_price_duration_curve.accepted_price.iloc[0] == pytest.approx(plant_with_highest_o_m.variable_o_and_m_per_mwh + 18.977/plant_with_highest_o_m.efficiency+25.085*plant_with_highest_o_m.fuel.mwh_to_co2e_conversion_factor*(1/plant_with_highest_o_m.efficiency))
        assert predicted_price_duration_curve.accepted_price.iloc[1] == pytest.approx(plant_with_highest_o_m.variable_o_and_m_per_mwh + 18.977/plant_with_highest_o_m.efficiency+25.085*plant_with_highest_o_m.fuel.mwh_to_co2e_conversion_factor*(1/plant_with_highest_o_m.efficiency))
        assert predicted_price_duration_curve.accepted_price.iloc[2] == pytest.approx(plant_with_highest_o_m.variable_o_and_m_per_mwh + 18.977/plant_with_highest_o_m.efficiency+25.085*plant_with_highest_o_m.fuel.mwh_to_co2e_conversion_factor*(1/plant_with_highest_o_m.efficiency))
        assert predicted_price_duration_curve.accepted_price.iloc[3] == pytest.approx(plant_with_highest_o_m.variable_o_and_m_per_mwh + 18.977/plant_with_highest_o_m.efficiency+25.085*plant_with_highest_o_m.fuel.mwh_to_co2e_conversion_factor*(1/plant_with_highest_o_m.efficiency))
        assert predicted_price_duration_curve.accepted_price.iloc[4] == pytest.approx(plant_with_highest_o_m.variable_o_and_m_per_mwh + 18.977/plant_with_highest_o_m.efficiency+25.085*plant_with_highest_o_m.fuel.mwh_to_co2e_conversion_factor*(1/plant_with_highest_o_m.efficiency))
        assert predicted_price_duration_curve.accepted_price.iloc[5] == pytest.approx(plant_with_highest_o_m.variable_o_and_m_per_mwh + 18.977/plant_with_highest_o_m.efficiency+25.085*plant_with_highest_o_m.fuel.mwh_to_co2e_conversion_factor*(1/plant_with_highest_o_m.efficiency))
        assert predicted_price_duration_curve.accepted_price.iloc[6] == pytest.approx(plant_with_highest_o_m.variable_o_and_m_per_mwh + 18.977/plant_with_highest_o_m.efficiency+25.085*plant_with_highest_o_m.fuel.mwh_to_co2e_conversion_factor*(1/plant_with_highest_o_m.efficiency))
        assert predicted_price_duration_curve.accepted_price.iloc[7] == pytest.approx(plant_with_highest_o_m.variable_o_and_m_per_mwh + 18.977/plant_with_highest_o_m.efficiency+25.085*plant_with_highest_o_m.fuel.mwh_to_co2e_conversion_factor*(1/plant_with_highest_o_m.efficiency))
        assert predicted_price_duration_curve.accepted_price.iloc[8] == pytest.approx(plant_with_highest_o_m.variable_o_and_m_per_mwh + 18.977/plant_with_highest_o_m.efficiency+25.085*plant_with_highest_o_m.fuel.mwh_to_co2e_conversion_factor*(1/plant_with_highest_o_m.efficiency))
        assert predicted_price_duration_curve.accepted_price.iloc[9] == pytest.approx(plant_with_highest_o_m.variable_o_and_m_per_mwh + 18.977/plant_with_highest_o_m.efficiency+25.085*plant_with_highest_o_m.fuel.mwh_to_co2e_conversion_factor*(1/plant_with_highest_o_m.efficiency))
