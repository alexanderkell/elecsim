from mesa.batchrunner import BatchRunner

from src.model.world import World

"""
File name: batch_run
Date created: 19/01/2019
Feature: # Enables world to be run multiple times based on different parameter sweeps.
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"


batch_run = BatchRunner(World,
                        fixed_parameters=fixed_params,
                        variable_parameters=variable_params,
                        iterations=5,
                        max_steps=100,
                        model_reporters={"Gini": compute_gini})
