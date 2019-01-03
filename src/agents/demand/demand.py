from mesa import Agent

import logging
logger = logging.getLogger(__name__)



"""demand.py: Agent which simulates the demand of the UK"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"

class Demand(Agent):

    def __init__(self, unique_id, segment_hours, segment_consumption, yearly_demand_change):
        """
        An agent representing UK electricity demand
        :param segment_hours: A series representing the load duration curve
        """
        self.unique_id = unique_id

        self.segment_hours = segment_hours
        self.segment_consumption = segment_consumption
        self.yearly_demand_change = yearly_demand_change

        self.years_from_start = 0

    def step(self):
        logger.debug("Stepping demand")
        logger.debug("consumption: {}, years_from_start: {}, yearly_demand_change: {}".format(self.segment_consumption, self.years_from_start, self.yearly_demand_change[self.years_from_start]))
        self.segment_consumption = [consumption * self.yearly_demand_change[self.years_from_start] for consumption in self.segment_consumption]
        logger.debug("segment consumption: {}".format(self.segment_consumption))
        self.years_from_start += 1
        # load to change each year due to certain scenario

