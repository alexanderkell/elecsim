"""
File name: test_world
Date created: 01/12/2018
Feature: #Enter feature description here
"""
from unittest import TestCase
from src.model.world import World
from scenario import scenario_data
__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"


class TestWorld(TestCase):
    def test_world_initialization(self):
        world = World(scenario=scenario_data)

        assert 1 == 1
