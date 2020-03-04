import sys

"""
File name: scenario_modifier
Date created: 03/03/2019
Feature: # Feature to enable the user to overwrite the scenario file.
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"

def overwrite_scenario_file(scenario_file):
    sys.modules['elecsim'].scenario.scenario_data=scenario_file
