import logging

from mesa import Agent

import elecsim.scenario.scenario_data
logger = logging.getLogger(__name__)



"""demand.py: Agent which simulates the demand of the UK"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"


class Demand(Agent):

    def __init__(self, model, unique_id, segment_hours=None, segment_consumption=None):
        """ An agent representing UK electricity demand

        :param segment_hours: A series representing the load duration curve
        """
        self.unique_id = unique_id
        self.model = model
        self.segment_hours = segment_hours
        self.segment_consumption = segment_consumption

        self.year_segment_hours = segment_hours
        self.year_segment_consumption = segment_consumption

        self.yearly_demand_change = elecsim.scenario.scenario_data.yearly_demand_change
        self.years_from_start = 0

    def step(self):
        logger.debug("Stepping demand")
        self.segment_consumption = [i * self.yearly_demand_change[self.years_from_start] for i in self.segment_consumption]
        self.years_from_start += 1

        # load to change each year due to certain scenario

