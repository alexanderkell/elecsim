import logging
import pandas as pd
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
        self.demand_ldc = self.demand.groupby('cluster').apply(lambda x: x.sort_values('capacity_factor', ascending=False).reset_index())
        self.demand_ldc.capacity_factor = self.demand_ldc.capacity_factor.values*elecsim.scenario.scenario_data.initial_max_demand_size

        self.segment_hours = 0
        self.segment_consumption = 0

        self.years_from_start = 0
        self.steps_from_start = 0
        self.year_segment_hours = 0
        self.year_segment_consumption = 0


    def step(self):
        logger.debug("Stepping demand")
        steps_since_year = self.model.step_number % self.model.market_time_splices

        if steps_since_year == 0:
            self.demand_ldc.capacity_factor = self.demand_ldc.capacity_factor * self.yearly_demand_change[self.years_from_start]
            self.year_segment_hours, self.year_segment_consumption = self.set_demand_for_year()

        grouped_days = self.demand_ldc.reset_index(drop=True).groupby("cluster")
        representative_day = grouped_days.get_group((list(grouped_days.groups)[steps_since_year]))

        self.segment_consumption = representative_day.capacity_factor.tolist()
        self.segment_hours = representative_day.cluster.cumsum().tolist()

        # self.steps_from_start += 1

        # load to change each year due to certain scenario

    def set_demand_for_year(self):

        # grouped_days = self.demand_ldc.reset_index(drop=True).groupby("cluster")

        demand_dataframe = self.demand_ldc.sort_values("capacity_factor", ascending=False)

        demand_dataframe['hour'] = demand_dataframe.cluster.cumsum()



        # year_segment_consumption = demand_dataframe.capacity_factor.tolist()
        # year_segment_hours = demand_dataframe.hour.tolist()

        year_segment_consumption = (pd.DataFrame(pd.cut(demand_dataframe.capacity_factor, 20*self.model.market_time_splices).apply(lambda x: x.right)).groupby("capacity_factor").first()).index.tolist()
        year_segment_hours = (pd.DataFrame(pd.cut(demand_dataframe.hour, 20*self.model.market_time_splices).apply(lambda x: x.right)).groupby("hour").first()).index.tolist()

        # final_day = 0
        # for _, day in grouped_days:
        #     year_segment_consumption.append(day.capacity_factor.tolist())
        #     segment_hours = [final_day + hour * day.counts.iloc[0] for hour in range(1, 25)]
        #     year_segment_hours.append(segment_hours)
        #     final_day = 24 * day.counts.iloc[0]

        # year_segment_consumption = demand_dataframe.

        return year_segment_hours, year_segment_consumption

