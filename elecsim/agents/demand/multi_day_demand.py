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
    """ An agent representing UK electricity demand by selecting representative days.
    """

    def __init__(self, unique_id, multi_year_data):
        super().__init__(unique_id=unique_id)

        self.yearly_demand_change = elecsim.scenario.scenario_data.yearly_demand_change
        self.demand = multi_year_data[multi_year_data.data_type == "load"]
        self.demand_ldc = self.demand.groupby('cluster').apply(lambda x: x.sort_values('capacity_factor', ascending=True).reset_index())

        self.years_from_start = 0

    def step(self):
        logger.debug("Stepping demand")
        self.demand_ldc.capacity_factor = self.demand_ldc.capacity_factor * self.yearly_demand_change[self.years_from_start]
        self.years_from_start += 1

        # load to change each year due to certain scenario

