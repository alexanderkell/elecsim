from src.plants.plant_costs.estimate_costs.estimate_costs import _select_cost_estimator
from src.scenario.scenario_data import modern_plant_costs

import pandas as pd
"""
File name: historical_fuel_cost_analysis
Date created: 26/01/2019
Feature: #Enter feature description here
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"


historical_cost_data = pd.DataFrame(columns=['connection_cost_per_mw', 'construction_cost_per_mw', 'fixed_o_and_m_per_mw', 'infrastructure', 'insurance_cost_per_mw', 'pre_dev_cost_per_mw', 'variable_o_and_m_per_mwh', 'pre_dev_period', 'operating_period', 'construction_period', 'efficiency', 'average_load_factor', 'construction_spend_years', 'pre_dev_spend_years'])
for plant_type in ['CCGT', 'Coal', 'Nuclear', 'Onshore', 'Offshore', 'PV']:
    for year in [1980, 1990, 2000, 2010]:

            plant_cost_data = modern_plant_costs[(modern_plant_costs.Type == plant_type) & (modern_plant_costs.Plant_Size>5)]
            for plant_row in plant_cost_data.itertuples():

                cost_estimations  = _select_cost_estimator(year,plant_row.Type,plant_row.Plant_Size)
                cost_estimations['Type'] = plant_row.Type
                cost_estimations['Plant_Size'] = plant_row.Plant_Size
                cost_estimations['Year'] = year
                print(cost_estimations)
                historical_cost_data = historical_cost_data.append(pd.Series(cost_estimations), ignore_index=True)

historical_cost_data.to_csv('~/Documents/PhD/Reports/6. ELECSIM/Paper/visualisation/jupyter/power_plant_cost_table/historical_costs.csv')
