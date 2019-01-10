from src.data_manipulation.data_modifications.inverse_transform_sampling import sample_from_custom_distribution
import numpy as np
from logging import getLogger
import logging
logger = getLogger(__name__)
from operator import itemgetter
from pytest import approx
"""
File name: test_sample
Date created: 10/01/2019
Feature: #Enter feature description here
"""
from unittest import TestCase

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"

logging.basicConfig(level=logging.DEBUG)

class TestSample(TestCase):
    def test_sample(self):
        division = [-2.67136237, -2.05612326, -1.44088415, -0.82564504, -0.21040593,
         0.40483318,  1.0200723 ,  1.63531141,  2.25055052,  2.86578963,
         3.48102874]
        count = [ 3,  1,  4, 17, 26, 14,  3,  2,  0,  1]
        result = sample_from_custom_distribution(count, division, 100000)
        dist = [[x,result.count(x)] for x in set(result)]
        sorted_dist = sorted(dist, key=itemgetter(1))
        logger.debug(sorted_dist)
        assert sorted_dist[0][1] == approx(100000*0.01408451, abs=500)
        assert sorted_dist[1][1] == approx(100000*0.01408451, abs=500)
        assert sorted_dist[2][1] == approx(100000*0.02816901, abs=500)
        assert sorted_dist[3][1] == approx(100000*0.04225352, abs=500)
        assert sorted_dist[4][1] == approx(100000*0.04225352, abs=500)
        assert sorted_dist[5][1] == approx(100000*0.05633803, abs=500)
        assert sorted_dist[6][1] == approx(100000*0.1971831, abs=500)
        assert sorted_dist[7][1] == approx(100000*0.23943662, abs=500)
        assert sorted_dist[8][1] == approx(100000*0.36619718, abs=500)


