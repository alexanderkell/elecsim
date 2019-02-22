import pandas as pd

from elecsim.data_manipulation.data_modifications.extrapolation_interpolate import ExtrapolateInterpolate

"""
File name: test_extrapolateInterpolate
Date created: 08/01/2019
Feature: #Enter feature description here
"""
from unittest import TestCase

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"


class TestExtrapolateInterpolate(TestCase):
    def test_min_max_extrapolate(self):
        x = pd.Series([1,2,3,4,5])
        y = pd.Series([4,6,4,2,1])

        extrapolate_interpolate = ExtrapolateInterpolate(x,y)

        assert extrapolate_interpolate.min_max_extrapolate(1) == 4
        assert extrapolate_interpolate.min_max_extrapolate(2) == 6
        assert extrapolate_interpolate.min_max_extrapolate(5) == 1
        assert extrapolate_interpolate.min_max_extrapolate(8) == 1
        assert extrapolate_interpolate.min_max_extrapolate(0) == 4
