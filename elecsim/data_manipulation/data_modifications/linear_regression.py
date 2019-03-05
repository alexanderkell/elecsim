from scipy.stats import linregress

"""
File name: linear_regression
Date created: 29/12/2018
Feature: #Enter feature description here
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"

def linear_regression(regression, years_to_look_back, years_to_look_ahead=None):
    years_to_regress = list(range(years_to_look_back))
    years_to_regress = [float(i) for i in years_to_regress]
    m, c, _, _, _ = linregress(years_to_regress, regression)
    next_value = m * (years_to_look_back+years_to_look_ahead-1) + c
    return next_value
