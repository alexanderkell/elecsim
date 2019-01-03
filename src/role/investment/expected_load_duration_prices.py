import logging
from src.data_manipulation.data_modifications.linear_regression import linear_regression
logger = logging.getLogger(__name__)
from scipy.stats import linregress

"""
File name: expected_load_duration_prices
Date created: 31/12/2018
Feature: # Functionality that calculates the expected prices for each segment in the load duration curve.
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"



class LoadDurationPrices:

    def __init__(self, model):
        self.historical_load_duration_prices = model.PowerExchange.load_duration_curve_prices

    def get_load_curve_price_predictions(self, reference_year, look_back_years):
        years_for_regression = list(range((reference_year-look_back_years),(reference_year)))
        data = self.historical_load_duration_prices[self.historical_load_duration_prices['year'].isin(years_for_regression)]

        # logger.debug("data for regression\n {}".format(data))

        # regressed_data = data.groupby('segment_hour').apply(self.model, new_value=reference_year)
        average_price = data.groupby('segment_hour')['accepted_price'].mean().sort_index(ascending=False)
        return average_price

    # Linear regression model
    # def model(self, dataframe, new_value):
    #     y = dataframe['accepted_price']
    #     x = dataframe['year']
    #     logger.debug(x)
    #     logger.debug(y)
    #     m, c, _, _, _ = linregress(x, y)
    #     result = m * new_value + c
    #     return result
