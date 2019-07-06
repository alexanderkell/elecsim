import os.path
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from elecsim.model.world import World
import tracemalloc

import pandas as pd
import linecache

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

#
# def display_top(snapshot, key_type='lineno', limit=3):
#     snapshot = snapshot.filter_traces((
#         tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
#         tracemalloc.Filter(False, "<unknown>"),
#     ))
#     top_stats = snapshot.statistics(key_type)
#
#     print("Top %s lines" % limit)
#     for index, stat in enumerate(top_stats[:limit], 1):
#         frame = stat.traceback[0]
#         # replace "/path/to/module/file.py" with "module/file.py"
#         filename = os.sep.join(frame.filename.split(os.sep)[-2:])
#         print("#%s: %s:%s: %.1f KiB"
#               % (index, filename, frame.lineno, stat.size / 1024))
#         line = linecache.getline(frame.filename, frame.lineno).strip()
#         if line:
#             print('    %s' % line)
#
#     other = top_stats[limit:]
#     if other:
#         size = sum(stat.size for stat in other)
#         print("%s other: %.1f KiB" % (len(other), size / 1024))
#     total = sum(stat.size for stat in top_stats)
#     print("Total allocated size: %.1f KiB" % (total / 1024))
#
# class TestWorld:
    # def test_world_initialization(self):

# with PyCallGraph(output=GraphvizOutput()):
<<<<<<< HEAD
MARKET_TIME_SPLICES = 8
=======
MARKET_TIME_SPLICES = 1
>>>>>>> 5f3c373861c398621fed06ebb3fe989ceb1733a9
YEARS_TO_RUN = 40
number_of_steps = YEARS_TO_RUN * MARKET_TIME_SPLICES
world = World(initialization_year=2018, market_time_splices=MARKET_TIME_SPLICES, data_folder="test_new", number_of_steps=number_of_steps)

for i in range(number_of_steps):
    world.step()

