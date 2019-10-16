import logging
from functools import lru_cache

import numpy as np
import pandas as pd
import os, sys

from elecsim.market.electricity.market.power_exchange import PowerExchange
from elecsim.role.market.latest_market_data import LatestMarketData
from elecsim.role.investment.curve_fitting_functions import logit
from elecsim.scenario.scenario_data import years_for_agents_to_predict_forward
import elecsim.scenario.scenario_data
from scipy.optimize import curve_fit
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

    def __init__(self, model, look_back_period):
        self.model = model
        self.demand_change_predicted = LatestMarketData(self.model).agent_forecast_value("demand", look_back_period, elecsim.scenario.scenario_data.years_for_agents_to_predict_forward)

        # power_ex = PowerExchange(self.model)
        self.power_ex = self.model.PowerExchange

    def predict_price_duration_curve(self):
        self.power_ex.price_duration_curve = []
        if self.model.market_time_splices == 1:
            year_segment_consumption_predicted = [cons * self.demand_change_predicted for cons in self.model.demand.segment_consumption]
            # self.power_ex.tender_bids(self.model.demand.segment_hours, predicted_consumption, predict=True)
            year_segment_hours = self.model.demand.segment_hours
            # self.model.clear_all_bids()
            #
            # predicted_price_duration_curve = power_ex.price_duration_curve
            # predicted_price_duration_curve = estimate_lost_load_price(predicted_price_duration_curve)
        else:
            price_duration_curve = []
            # year_segment_hours, year_segment_consumption = self.model.demand.get_demand_for_year()
            year_segment_hours = self.model.demand.year_segment_hours
            year_segment_consumption = self.model.demand.year_segment_consumption

            # for segment_hours, segment_consumption in zip(year_segment_hours, year_segment_consumption):

            year_segment_consumption_predicted = [cons * self.demand_change_predicted for cons in year_segment_consumption]

        if elecsim.scenario.scenario_data.investment_mechanism == "future_price_fit":
            predicted_price_duration_curve = self.fit_linear_price_duration_curve(year_segment_consumption_predicted, year_segment_hours)
        elif elecsim.scenario.scenario_data.investment_mechanism == "projection_fit":
            predicted_price_duration_curve = self.fit_linear_price_duration_curve_from_projections(year_segment_consumption_predicted, year_segment_hours)
            predicted_price_duration_curve_market = self.market_price_curve_prediction(year_segment_consumption_predicted, year_segment_hours)
            linear_price_mean = predicted_price_duration_curve['accepted_price'].mean()
            market_price_mean = predicted_price_duration_curve_market['accepted_price'].mean()
            if market_price_mean < linear_price_mean:
                predicted_price_duration_curve = predicted_price_duration_curve_market
        else:
            predicted_price_duration_curve = self.market_price_curve_prediction(year_segment_consumption_predicted, year_segment_hours)

        logger.debug("predicted_price_duration_curve: {}".format(predicted_price_duration_curve))
        # predicted_price_duration_curve.segment_hour = predicted_price_duration_curve.segment_hour.cumsum()
        # price_duration_curve.append(predicted_price_duration_curve_day)
        # predicted_price_duration_curve = pd.concat(price_duration_curve)
        # predicted_price_duration_curve.sort_values("segment_demand", ascending=False, inplace=True)

        return predicted_price_duration_curve

    def market_price_curve_prediction(self, year_segment_consumption_predicted, year_segment_hours):
        self.power_ex.tender_bids(year_segment_hours, year_segment_consumption_predicted, predict=True)
        self.model.clear_all_bids()
        predicted_price_duration_curve = self.power_ex.price_duration_curve
        predicted_price_duration_curve = estimate_lost_load_price(predicted_price_duration_curve)
        return predicted_price_duration_curve

    def fit_linear_price_duration_curve(self, year_segment_consumption_predicted, year_segment_hours):
        segment_demand = year_segment_consumption_predicted
        segment_hour = year_segment_hours
        year = self.model.year_number

        if self.model.fitting_params is not None:
            fitting_params = self.model.fitting_params
        elif self.model.long_term_fitting_params is not None:
            fitting_params = self.model.long_term_fitting_params[self.model.years_from_start]

            holder_params = fitting_params.copy()


        # if self.model.fitting_params is not None and self.model.long_term_fitting_params is not None:
        if hasattr(self.model, "fitting_params") or hasattr(self.model, "long_term_fitting_params"):
            try:
                holder_params[0] *= np.random.normal(0, self.model.future_price_uncertainty_m)
                holder_params[1] *= np.random.normal(0, self.model.future_price_uncertainty_c)
            except:
                pass

        temp_price_dataframe = {"segment_demand": segment_demand, "segment_hour": segment_hour, "year": year}

        price_duration_curve = pd.DataFrame(temp_price_dataframe)
        price_duration_curve['accepted_price'] = fitting_params[0]*price_duration_curve.segment_demand + fitting_params[1]
        # price_duration_curve['accepted_price'] = fitting_params[0]*segment_hour + fitting_params[1]

        predicted_price_duration_curve = price_duration_curve
        return predicted_price_duration_curve

    def fit_linear_price_duration_curve_from_projections(self, year_segment_consumption_predicted, year_segment_hours):
        segment_demand = year_segment_consumption_predicted
        segment_hour = year_segment_hours
        year = self.model.year_number + years_for_agents_to_predict_forward
        year_for_prediction = self.model.years_from_start + years_for_agents_to_predict_forward
        try:
            baseload_price = electricity_baseload[year_for_prediction]
            volume_weighted_price = electricity_volume_weighted[year_for_prediction]
        except:
            baseload_price = electricity_baseload[-1]
            volume_weighted_price = electricity_volume_weighted[-1]

        temp_price_dataframe = {"segment_demand": segment_demand, "segment_hour": segment_hour, "accepted_price": np.NaN, "year": year}

        price_duration_curve = pd.DataFrame(temp_price_dataframe)
        # price_duration_curve.accepted_price =
        price_duration_curve.accepted_price.iloc[len(price_duration_curve)-1] = baseload_price
        price_duration_curve.accepted_price.iloc[int((len(price_duration_curve)-1)/2)] = volume_weighted_price
        price_duration_curve.accepted_price = price_duration_curve.accepted_price.interpolate(method="spline", order=1, limit_direction="both")


        predicted_price_duration_curve = price_duration_curve
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

                logger.debug("predicted_price_duration_curve: {}".format(predicted_price_duration_curve))

                # popt, pcov = curve_fit(logit, predicted_price_duration_curve_training.segment_demand, predicted_price_duration_curve_training.accepted_price, [1, 1, 1, 1, 90])
                # extrapolated = logit(predicted_price_duration_curve.loc[np.isnan(predicted_price_duration_curve.accepted_price), 'segment_demand'], *popt)

                # # Polynomial regression fitting
                p = np.poly1d(np.polyfit(predicted_price_duration_curve_training.segment_demand, predicted_price_duration_curve_training.accepted_price,3))
                extrapolated = p(predicted_price_duration_curve.loc[np.isnan(predicted_price_duration_curve.accepted_price), 'segment_demand'])
                # logger.debug("extrapolated: {}".format(extrapolated))
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
def get_price_duration_curve(model, look_back_period):
    predicted_price_duration_curve = PredictPriceDurationCurve(model, look_back_period=look_back_period).predict_price_duration_curve()
    return predicted_price_duration_curve

