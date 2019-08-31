import pandas as pd
import pickle
# !pip install -U elecsim
from elecsim import World
from elecsim.market.electricity.market.power_exchange import PowerExchange
from elecsim.agents.demand.multi_day_demand import MultiDayDemand
import elecsim.scenario.scenario_data
from elecsim.plants.plant_costs.estimate_costs.estimate_costs import create_power_plant, create_power_plant_group
from elecsim.role.investment.calculate_npv import CalculateNPV

import array
import numpy
import random

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

"""
File name: run_price_forecaster
Date created: 30/08/2019
Feature: #Enter feature description here
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"

scenario_2013 = "/Users/b1017579/Documents/PhD/Projects/10. ELECSIM/run/beis_case_study/scenario/reference_scenario_2018.py"

model = World(initialization_year=2018, scenario_file=scenario_2013, market_time_splices=8, data_folder="best_run_beis_comparison", number_of_steps=8*5, fitting_params=[0.001644, 11.04157], highest_demand=63910)
demand = MultiDayDemand(model, 1, elecsim.scenario.scenario_data.multi_year_data)


plant = elecsim.scenario.scenario_data.modern_plant_costs[elecsim.scenario.scenario_data.modern_plant_costs.Plant_Type.str.contains("CCGT H Class")]

plant_group = create_power_plant_group("plant_RL_invested", 2026, plant.Type.values[0], plant.Plant_Size.values[0], 5)
model.get_gencos()[0].plants.append(plant_group)

model.operate_constructed_plants(2050)
pdc = []
for _ in range(8):
    demand.step()
    electricity_prices = PowerExchange(model).tender_bids(demand.segment_hours, demand.segment_consumption)
    pdc.append(electricity_prices)
    pdc_df = pd.concat(pdc)

print(CalculateNPV(model, 0.002, 10).calculate_npv_costs("CCGT", 1400, pdc_df))
