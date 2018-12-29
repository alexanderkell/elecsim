import logging
from src.data_manipulation.data_modifications.linear_regression import linear_regression


logger = logging.getLogger(__name__)

"""
File name: current_market_data
Date created: 29/12/2018
Feature: # Data which collates market information for generator companies when making decisions about investments.
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"


class LatestMarketData:

    def __init__(self, model):
        self.model = model
        self.demand = self.model.demand

    def demand_data(self, years_to_look_back):
        years_for_regression = list(range(self.demand.years_from_start-years_to_look_back-1,self.demand.years_from_start-1))
        logger.debug("years of regression: {}".format(years_for_regression))

        regression = self._get_yearly_demand_change_for_regression(years_for_regression)

        logger.debug(regression)

        next_value = linear_regression(regression, years_to_look_back)
        return next_value

    def _get_yearly_demand_change_for_regression(self, years_for_regression):
        regression = [self.demand.yearly_demand_change[i] if i > 0 else self.demand.yearly_demand_change[0] if
        self.demand.yearly_demand_change[i] == None else self.demand.yearly_demand_change[-1] for i in
                      years_for_regression]
        return regression


