from scenario.scenario_data import wind_capacity_factor, solar_capacity_factor

"""
File name: solar_capacity_factor
Date created: 27/12/2018
Feature: # Calculates the average capacity factor per demand segment
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"


class DemandFactor():

    def __init__(self, renewable_type):
        self.renewable_type = renewable_type
        if self.renewable_type == "Onshore" or 'Offshore':
            self.capacity_data = wind_capacity_factor[['time',self.renewable_type.lower()]]

