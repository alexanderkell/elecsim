import numpy as np

"""
File name: curve_fitting
Date created: 10/07/2019
Feature: #Enter feature description here
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"


def logit(x, a, b, c, d, e):
    return -a*np.log(b*x/(c-d*x)) + e

