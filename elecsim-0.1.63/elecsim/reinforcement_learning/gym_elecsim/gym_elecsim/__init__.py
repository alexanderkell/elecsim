from gym.envs.registration import register

"""
File name: __init__.py
Date created: 19/02/2019
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"

register(
    id='MyEnv-v0',
    entry_point='elecsim.reinforcement_learning.gym_elecsim.gym_elecsim.envs:WorldEnvironment',
)
