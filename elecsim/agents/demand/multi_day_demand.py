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

    def __init__(self, model, unique_id, multi_year_data):
        super().__init__(model=model, unique_id=unique_id)

        self.yearly_demand_change = elecsim.scenario.scenario_data.yearly_demand_change
        self.demand = multi_year_data[multi_year_data.data_type == "load"]
        self.demand_ldc = self.demand.groupby('cluster').apply(lambda x: x.sort_values('capacity_factor', ascending=True).reset_index())

        self.segment_hours = 0
        self.segment_consumption = 0

        self.years_from_start = 0
        self.steps_from_start = 0

    def step(self):
        logger.debug("Stepping demand")
        steps_since_year = self.model.step_number % self.model.market_time_splices

        if steps_since_year == 0:
            self.demand_ldc.capacity_factor = self.demand_ldc.capacity_factor * self.yearly_demand_change[self.years_from_start]

        logger.info("self.demand_ldc: \n{}".format(self.demand_ldc))
        grouped_days = self.demand_ldc.reset_index(drop=True).groupby("cluster")

        representative_day = grouped_days.get_group((list(grouped_days.groups)[steps_since_year]))

        self.segment_consumption = representative_day.capacity_factor.tolist()
        self.segment_hours = representative_day.level_0.iloc[0] * representative_day.counts.tolist()

        # self.steps_from_start += 1

        # load to change each year due to certain scenario

    def get_demand_for_year(self):

        grouped_days = self.demand_ldc.reset_index(drop=True).groupby("cluster")

        year_segment_consumption = []
        year_segment_hours = []

        logger.info("self.demand_ldc: {}".format(grouped_days))

        for _, day in grouped_days:
            year_segment_consumption.append(day.capacity_factor.tolist())
            segment_hours = [hour * day.counts.iloc[0] for hour in range(24)]
            year_segment_hours.append(segment_hours)


        return year_segment_hours, year_segment_consumption

