from src.model.world import World
from src.scenario import scenario_data
import logging
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput

"""
File name: test_world
Date created: 01/12/2018
Feature: # Tests the model
"""
# from unittest import TestCase

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"

logging.basicConfig(level=logging.DEBUG)

class TestWorld:
    def test_world_initialization(self):
        # with PyCallGraph(output=GraphvizOutput()):
        world = World(scenario=scenario_data, initialization_year=2016)

        for i in range(1):
            world.step()

        assert 1 == 1
