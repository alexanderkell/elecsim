from math import log
import logging

logger = logging.getLogger(__name__)


"""
File name: renewable_learning_rate
Date created: 21/12/2018
Feature: # Contains the functionality for implementing a learning rate for renewable plants to simulate a decrease in prices
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"

logging.basicConfig(level=logging.DEBUG)

def future_renewable_energy_costs(starting_lcoe, learning_rate, number_of_generation_assets):
    logging.debug("starting_lcoe: {}, number of generation assets: {}, learning rate: {}".format(starting_lcoe, number_of_generation_assets, learning_rate))
    next_price = starting_lcoe*number_of_generation_assets**(log(learning_rate, 2))
    logging.debug("1 to the power of log: {}".format(1**log(learning_rate, 2)))
    return next_price
