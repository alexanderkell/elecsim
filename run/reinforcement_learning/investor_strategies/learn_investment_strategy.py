import os.path
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from elecsim.model.world import World
import tracemalloc

import pandas as pd
import linecache

# from multiprocessing import Pool, Process
import logging
import ray
import psutil

import time

try:
    # Capirca uses Google's abseil-py library, which uses a Google-specific
    # wrapper for logging. That wrapper will write a warning to sys.stderr if
    # the Google command-line flags library has not been initialized.
    #
    # https://github.com/abseil/abseil-py/blob/pypi-v0.7.1/absl/logging/__init__.py#L819-L825
    #
    # This is not right behavior for Python code that is invoked outside of a
    # Google-authored main program. Use knowledge of abseil-py to disable that
    # warning; ignore and continue if something goes wrong.
    import absl.logging

    # https://github.com/abseil/abseil-py/issues/99
    logging.root.removeHandler(absl.logging._absl_handler)
    # https://github.com/abseil/abseil-py/issues/102
    absl.logging._warn_preinit_stderr = False
except Exception:
    pass


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

logging.basicConfig(level=logging.INFO)

MARKET_TIME_SPLICES = 8
YEARS_TO_RUN = 40
number_of_steps = YEARS_TO_RUN * MARKET_TIME_SPLICES

num_cpus = psutil.cpu_count(logical=False)

print("num_cpus: {}".format(num_cpus))
ray.init(num_cpus=num_cpus, redis_max_memory=100000000000)

time.sleep(20)

@ray.remote
def run_world(num_steps=number_of_steps):
    world = World(initialization_year=2018, market_time_splices=MARKET_TIME_SPLICES, data_folder="test_new", number_of_steps=number_of_steps)
    for i in range(num_steps):
        world.step()

results = []
for j in range(10000):
    results.append(run_world.remote(number_of_steps))

result_ray = ray.get(results)
