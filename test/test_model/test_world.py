import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from src.model.world import World
from src.scenario import scenario_data
import logging

import pandas as pd

from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput

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

class TestWorld:
    def test_world_initialization(self):
# with PyCallGraph(output=GraphvizOutput()):
        world = World(initialization_year=2018)

        for i in range(10):
            world.step()

        # data = world.datacollector.get_model_vars_dataframe()
        # logger.info("final data: \n {}".format(data))
