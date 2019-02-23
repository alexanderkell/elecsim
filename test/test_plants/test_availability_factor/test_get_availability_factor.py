from elecsim.plants.availability_factors.availability_factor_calculations import get_availability_factor

"""
File name: test_get_availability_factor
Date created: 13/01/2019
Feature: #Enter feature description here
"""
import pytest
__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"


class TestGet_availability_factor:


    @pytest.mark.parametrize("plant_type, year, expected_output",
                             [
                                 ("CCGT", 2011, 0.72),
                                 ("CCGT", 2013, 0.72),
                                 ("CCGT", 2014, 0.42),
                                 ("CCGT", 2015, 0.64),
                                 ("CCGT", 2016, 0.69),
                                 ("CCGT", 2017, 0.77),
                                 ("CCGT", 2019, 0.77),
                                 ("Coal", 2013, 0.79),
                                 ("Coal", 2014, 0.89),
                                 ("Coal", 2015, 0.85),
                                 ("Coal", 2016, 0.87),
                                 ("Coal", 2017, 0.85),
                                 ("OCGT", 2013, 0.72),
                                 ("OCGT", 2014, 0.42),
                                 ("OCGT", 2015, 0.64),
                                 ("OCGT", 2016, 0.69),
                                 ("OCGT", 2017, 0.77),
                             ])
    def test_get_availability_factor(self, plant_type, year, expected_output):
        assert get_availability_factor(plant_type, year) == expected_output
