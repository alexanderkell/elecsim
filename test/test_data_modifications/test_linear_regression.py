from elecsim.data_manipulation.data_modifications.linear_regression import linear_regression

"""
File name: test_linear_regression
Date created: 17/01/2019
Feature: #Enter feature description here
"""
from unittest import TestCase

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"


class TestLinear_regression(TestCase):
    def test_linear_regression(self):
        x = 4
        y = [1,2,3,4]
        assert linear_regression(y, x, 6) == 10
