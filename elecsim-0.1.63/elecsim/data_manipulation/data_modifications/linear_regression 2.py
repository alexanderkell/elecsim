from scipy.stats import linregress
import numpy as np
from functools import lru_cache
import logging

logger = logging.getLogger(__name__)
"""
File name: linear_regression
Date created: 29/12/2018
Feature: #Enter feature description here
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"


@lru_cache(1024)
def linear_regression(regression, years_to_look_back, years_to_look_ahead=None):
    regression = list(regression)
    years_to_regress = list(range(years_to_look_back))
    years_to_regress = np.array(years_to_regress).astype(float)
    try:
        regression = np.stack(regression, axis=1)
    except:
        pass
    try:
        m, c, _, _, _ = linregress(years_to_regress, np.array(regression).astype(float))
        next_value = m * (years_to_look_back + years_to_look_ahead-1) + c
    except Exception as e:
        logger.warning(str(e.with_traceback))
        logger.warning("regression: {}".format(regression))
        logger.warning("years to regress: {}".format(years_to_regress))
        next_value = regression[-1]
    return next_value
