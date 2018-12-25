import logging
logging.getLogger(__name__)

from src.role.investment.calculate_npv import calculate_npv

"""
File name: test_calculate_npv
Date created: 24/12/2018
Feature: #Enter feature description here
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"

logging.basicConfig(level=logging.DEBUG)


class TestCalculate_npv:
    def test_calculate_npv(self):
        calculate_npv(0.05, 2018, 2)
