import os.path
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from elecsim.model.world import World
import tracemalloc

import pandas as pd
import linecache

from elecsim.constants import ROOT_DIR

import logging
logger = logging.getLogger(__name__)

"""
File name: run_2013
Date created: 09/07/2019
Feature: #Enter feature description here
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"

pd.set_option('display.max_rows', 4000)

logging.basicConfig(level=logging.INFO)

MARKET_TIME_SPLICES = 4
YEARS_TO_RUN = 10
number_of_steps = YEARS_TO_RUN * MARKET_TIME_SPLICES

scenario_2013 = "{}/../run/validation-optimisation/scenario_file/scenario_2013.py".format(ROOT_DIR)



world = World(initialization_year=2013, scenario_file=scenario_2013, market_time_splices=MARKET_TIME_SPLICES, data_folder="runs_2013", number_of_steps=number_of_steps)

for i in range(number_of_steps):
    world.step()
