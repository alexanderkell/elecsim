import logging
logging.getLogger(__name__)
from src.plants.plant_costs.estimate_costs.estimate_costs import create_power_plant

from src.role.investment.calculate_npv import calculate_npv, calculate_expected_cash_flow, maximum_return
from pytest import approx
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
        assert calculate_npv(0.06, 2018, 2) == approx(247876046.0559078)

    def test_calculate_expected_cash_flow(self):
        plant = create_power_plant("Test", 2018, "CCGT", 1200)
        plant_dict = vars(plant)
        assert calculate_expected_cash_flow(plant_dict) == approx([-5280000, -5280000, -1440000, -240000000, -240000000, -135100000, 210756383.1, 206027198.2, 201298013.4, 196602132.7, 191872947.9, 187143763.1, 182447882.4, 177718697.6, 150242799.9, 122766902.2, 95291004.56, 67815106.88, 40339209.2, 12863311.52, -14612586.16, -42088483.84, -69564381.52, -97040279.2, -124516176.9, -151992074.6, -179467972.2, -206943869.9, -234419767.6, -261895665.3, -289371563])

    def test_maximum_return(self):
        maximum_return()

