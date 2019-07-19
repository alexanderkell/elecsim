import os.path
import sys

from pycallgraph.output import GraphvizOutput
from pycallgraph import PyCallGraph

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from elecsim.model.world import World

import pandas as pd

import logging
logger = logging.getLogger(__name__)

"""
File name: test_world
Date created: 01/12/2018
Feature: # Tests the model
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"

pd.set_option('display.max_rows', 4000)

logging.basicConfig(level=logging.INFO)


with PyCallGraph(output=GraphvizOutput()):
    MARKET_TIME_SPLICES = 8
    YEARS_TO_RUN = 40
    number_of_steps = YEARS_TO_RUN * MARKET_TIME_SPLICES
    world = World(initialization_year=2018, market_time_splices=MARKET_TIME_SPLICES, data_folder="test_new", number_of_steps=number_of_steps)

    for i in range(number_of_steps):
        world.step()

