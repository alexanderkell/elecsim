"""
File name: predict_fuel_prices
Date created: 26/12/2018
Feature: # Class which predicts prices of commodities such as CO2, Fuel and expected sale price.
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"

class PredictElectricityPrices:

    def __init__(self, year, number_of_years_looking_back, future_year,):
        self.year = year
        self.number_of_years_looking_back = number_of_years_looking_back
        self.future_year = future_year

    def predict_electricity_price(self):
        pass
