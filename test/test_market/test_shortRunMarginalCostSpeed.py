import logging
from unittest.mock import Mock

import pytest

from pycallgraph.output import GraphvizOutput
from pycallgraph import PyCallGraph

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))


from elecsim.model.world import World
from elecsim.role.plants.costs.fuel_plant_cost_calculations import FuelPlantCostCalculations
from elecsim.agents.generation_company.gen_co import GenCo

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)


with PyCallGraph(output=GraphvizOutput()):

    mock_model = Mock(spec=World)
    genco = Mock(spec=GenCo)

    genco.gas_price_modifier = 1
    mock_model.year_number=2020
    plant_cost_calculation = FuelPlantCostCalculations(plant_type = "CCGT", capacity_mw = 1200, construction_year = 2018, average_load_factor = 0.93, efficiency = 0.54, pre_dev_period = 3,
                construction_period = 3, operating_period = 25, pre_dev_spend_years = [0.44, 0.44, 0.12], construction_spend_years = [0.4, 0.4, 0.2],
                pre_dev_cost_per_mw = 10000, construction_cost_per_mw = 500000, infrastructure = 15100000, fixed_o_and_m_per_mw = 12200,
                variable_o_and_m_per_mwh = 3, insurance_cost_per_mw = 2100, connection_cost_per_mw = 3300)
    # logger.info(plant_cost_calculation.calculate_short_run_marginal_cost(mock_model, genco))
    
    for _ in range(5000):
        short_run_marginal_cost = plant_cost_calculation.calculate_short_run_marginal_cost(mock_model, genco)
    assert short_run_marginal_cost == pytest.approx(39.23609592592592)
