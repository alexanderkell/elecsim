from elecsim.model.world import World
import sys
import os

import logging

from elecsim.constants import ROOT_DIR
from pathlib import Path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

project_dir = Path("__file__").resolve().parents[1]
logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)



"""
File name: run_reference_scenario.py
Date created: 22/08/2019
Feature: #Enter feature description here
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"



# MARKET_TIME_SPLICES = 8
MARKET_TIME_SPLICES = 8
YEARS_TO_RUN = 17
number_of_steps = YEARS_TO_RUN * MARKET_TIME_SPLICES

scenario_2013 = "{}/../run/beis_case_study/scenario/reference_scenario_2018.py".format(ROOT_DIR)

for _ in range(100):
    world = World(initialization_year=2018, scenario_file=scenario_2013, market_time_splices=MARKET_TIME_SPLICES, data_folder="best_run_beis_comparison", number_of_steps=number_of_steps, fitting_params=[0.001644, 11.04157], highest_demand=63910)

    for _ in range(number_of_steps):
        world.step()

