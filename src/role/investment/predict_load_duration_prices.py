from src.agents.generation_company.gen_co import GenCo
from src.market.electricity.power_exchange import PowerExchange
# from src.scenario.scenario_data import segment_demand, segment_time



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

    def predict_load_curve_price(self, demand_predicted):
        predicted_consumption = [cons * demand_predicted for cons in self.model.Demand.segment_consumption]

        power_ex = PowerExchange(self.model)
        power_ex.tender_bids(self.model.Demand.segment_hours, predicted_consumption, predict=True)
        predicted_price_duration_curve = power_ex.price_duration_curve
        logger.debug("duration_curve_prices: {}".format(predicted_price_duration_curve))
        return predicted_price_duration_curve
