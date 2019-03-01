import logging

import pandas as pd

from elecsim.constants import ROOT_DIR

pd.set_option('display.max_rows', 500)

logger = logging.getLogger(__name__)
"""
File name: test_loadDurationPrices
Date created: 31/12/2018
Feature: # Testing functionality of using demand load curve price predictions.
"""
from unittest.mock import Mock
from pytest import approx
__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"

logging.basicConfig(level=logging.DEBUG)

#
# class TestLoadDurationPrices:
#     def test_get_load_curve_price_predictions(self):
#         model = Mock()
#
#         model.PowerExchange.load_duration_curve_prices = pd.read_csv('{}/test/test_investment/dummy_load_duration_curve.csv'.format(ROOT_DIR))
#         model.PowerExchange.load_duration_curve_prices = model.PowerExchange.load_duration_curve_prices.drop('Prices', axis=1)
#
#         load_duration_prices = LoadDurationPrices(model)
#         forecasted_ldp = load_duration_prices.get_load_curve_price_predictions(1999, 4)
#         logger.debug("forecasted ldp: \n{}".format(forecasted_ldp))
#
#         assert forecasted_ldp.loc[8752.500000] == approx(130.17626975)
#         assert forecasted_ldp.loc[8291.833333] == approx(82.56968175)
#         assert forecasted_ldp.loc[0.083333 ] == approx(94.93571675)

