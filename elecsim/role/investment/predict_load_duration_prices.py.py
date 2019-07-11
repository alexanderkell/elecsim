import logging
from functools import lru_cache

import numpy as np
import pandas as pd
import os, sys

from elecsim.market.electricity.market.power_exchange import PowerExchange
from elecsim.role.market.latest_market_data import LatestMarketData
import elecsim.scenario.scenario_data

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
        demand_change_predicted = LatestMarketData(self.model).agent_forecast_value("demand", look_back_period, elecsim.scenario.scenario_data.years_for_agents_to_predict_forward)

        # power_ex = PowerExchange(self.model)
        power_ex = self.model.PowerExchange
<<<<<<< HEAD
        power_ex.price_duration_curve = []
        if self.model.market_time_splices == 1:
            predicted_consumption = [cons * demand_change_predicted for cons in self.model.demand.segment_consumption]
            power_ex.tender_bids(self.model.demand.segment_hours, predicted_consumption, predict=True)
            # logger.info("bid length: {}".format(len(self.model.get_gencos()[0].plants[0].accepted_bids)))

            self.model.clear_all_bids()

=======
        if self.model.market_time_splices == 1:
            predicted_consumption = [cons * demand_change_predicted for cons in self.model.demand.segment_consumption]
            power_ex.tender_bids(self.model.demand.segment_hours, predicted_consumption, predict=True)
>>>>>>> 5f3c373861c398621fed06ebb3fe989ceb1733a9
            predicted_price_duration_curve = power_ex.price_duration_curve
            predicted_price_duration_curve = estimate_lost_load_price(predicted_price_duration_curve)
        else:
            price_duration_curve = []
            # year_segment_hours, year_segment_consumption = self.model.demand.get_demand_for_year()
            year_segment_hours = self.model.demand.year_segment_hours
            year_segment_consumption = self.model.demand.year_segment_consumption

            # for segment_hours, segment_consumption in zip(year_segment_hours, year_segment_consumption):

            year_segment_consumption_predicted = [cons * demand_change_predicted for cons in year_segment_consumption]

            power_ex.tender_bids(year_segment_hours, year_segment_consumption_predicted, predict=True)
<<<<<<< HEAD
            self.model.clear_all_bids()

=======
>>>>>>> 5f3c373861c398621fed06ebb3fe989ceb1733a9
            predicted_price_duration_curve = power_ex.price_duration_curve

            predicted_price_duration_curve = estimate_lost_load_price(predicted_price_duration_curve)

            # predicted_price_duration_curve.segment_hour = predicted_price_duration_curve.segment_hour.cumsum()
            # price_duration_curve.append(predicted_price_duration_curve_day)
            # predicted_price_duration_curve = pd.concat(price_duration_curve)
            # predicted_price_duration_curve.sort_values("segment_demand", ascending=False, inplace=True)

        return predicted_price_duration_curve


def estimate_lost_load_price(predicted_price_duration_curve):
    if elecsim.scenario.scenario_data.lost_load_price_predictor:
        if all(predicted_price_duration_curve.accepted_price == elecsim.scenario.scenario_data.lost_load):
            return predicted_price_duration_curve
        if any(predicted_price_duration_curve.accepted_price == elecsim.scenario.scenario_data.lost_load):
            predicted_price_duration_curve.accepted_price = predicted_price_duration_curve.accepted_price.replace(elecsim.scenario.scenario_data.lost_load,np.nan)
            # predicted_price_duration_curve.accepted_price.interpolate(method="polynomial", order=1)
            if predicted_price_duration_curve.accepted_price.count() > 1:
                predicted_price_duration_curve_training = predicted_price_duration_curve.dropna()

                p = np.poly1d(np.polyfit(predicted_price_duration_curve_training.segment_demand, predicted_price_duration_curve_training.accepted_price,1))
                extrapolated = p(predicted_price_duration_curve.loc[np.isnan(predicted_price_duration_curve.accepted_price), 'segment_demand'])
                logger.debug("extrapolated: {}".format(extrapolated))
                predicted_price_duration_curve.loc[np.isnan(predicted_price_duration_curve.accepted_price), "accepted_price"] = extrapolated
                return predicted_price_duration_curve
            elif predicted_price_duration_curve.accepted_price.count() == 1:
                predicted_price_duration_curve.accepted_price = predicted_price_duration_curve.accepted_price.fillna(predicted_price_duration_curve.accepted_price.mean())
                return predicted_price_duration_curve
        else:
            return predicted_price_duration_curve
    else:
        return predicted_price_duration_curve


# @lru_cache(1024)
def   get_price_duration_curve(model, look_back_period):
    predicted_price_duration_curve = PredictPriceDurationCurve(model).predict_price_duration_curve(look_back_period=look_back_period)
    return predicted_price_duration_curve

