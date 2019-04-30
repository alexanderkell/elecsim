import logging

import elecsim.scenario.scenario_data
from elecsim.agents.demand.demand import Demand
logger = logging.getLogger(__name__)



"""demand.py: Agent which simulates the demand of the UK"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"

class MultiDayDemand(Demand):

    def __init__(self, unique_id, segment_hours, segment_consumption):
        """ An agent representing UK electricity demand by selecting representative days.

        :param segment_hours: A series representing the load duration curve
        """
        super.__init__(unique_id= unique_id, )

        self.segment_hours = segment_hours
        self.segment_consumption = segment_consumption
        self.yearly_demand_change = elecsim.scenario.scenario_data.yearly_demand_change
        self.years_from_start = 0

    def step(self):
        logger.debug("Stepping demand")
        self.segment_consumption = [i * self.yearly_demand_change[self.years_from_start] for i in self.segment_consumption]
        self.years_from_start += 1

        # load to change each year due to certain scenario

