from src.market.electricity.power_exchange import PowerExchange
from src.role.market.latest_market_data import LatestMarketData


import logging
logger = logging.getLogger(__name__)

"""
File name: predict_load_duration_prices
Date created: 11/01/2019
Feature: # Predict Load Duration Prices
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"



class PredictPriceDurationCurve:

    def __init__(self, model):
        self.model = model

    def predict_price_duration_curve(self, look_back_period):
        demand_change_predicted = LatestMarketData(self.model).agent_forecast_value("demand", look_back_period)
        predicted_consumption = [cons * demand_change_predicted for cons in self.model.demand.segment_consumption]

        power_ex = PowerExchange(self.model)
        power_ex.tender_bids(self.model.demand.segment_hours, predicted_consumption, predict=True)
        predicted_price_duration_curve = power_ex.price_duration_curve
        return predicted_price_duration_curve
