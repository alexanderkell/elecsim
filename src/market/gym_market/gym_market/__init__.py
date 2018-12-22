from gym.envs.registration import register

"""
File name: __init__
Date created: 21/12/2018
Feature: #Enter feature description here
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"


register(
    id='market-v0',
    entry_point='gym_market.envs:MarketEnv',
)
