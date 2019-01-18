from src.market.electricity.power_exchange import PowerExchange
from src.role.market.latest_market_data import LatestMarketData
from src.scenario.scenario_data import years_for_agents_to_predict_forward

from functools import lru_cache

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
        demand_change_predicted = LatestMarketData(self.model).agent_forecast_value("demand", look_back_period, years_for_agents_to_predict_forward)
        predicted_consumption = [cons * demand_change_predicted for cons in self.model.demand.segment_consumption]

        power_ex = PowerExchange(self.model)
        power_ex.tender_bids(self.model.demand.segment_hours, predicted_consumption, predict=True)
        predicted_price_duration_curve = power_ex.price_duration_curve
        logger.info("predicted_price_duration_curve: {}".format(predicted_price_duration_curve))
        return predicted_price_duration_curve

@lru_cache(1024)
def get_price_duration_curve(model, look_back_period):
    predicted_price_duration_curve = PredictPriceDurationCurve(model).predict_price_duration_curve(look_back_period=look_back_period)
    return predicted_price_duration_curve
