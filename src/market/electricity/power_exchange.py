from itertools import chain
from mesa import Agent

import pandas as pd
import logging

logger = logging.getLogger(__name__)

from src.agents.generation_company.gen_co import GenCo
from src.role.market.world_plant_capacity import WorldPlantCapacity



"""power_exchange.py: Functionality to run power exchange"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"


class PowerExchange:
    def __init__(self, model):
        """
        Power exchange agent which contains functionality to tender and respond to bids.
        :param model: Model in which the agents are contained in.
        """
        self.model = model
        self.hold_duration_curve_prices = []
        self.load_duration_curve_prices = pd.DataFrame(columns = ["year", "segment_hour", "segment_demand", "accepted_price"])

    def tender_bids(self, segment_hours, segment_demand):
        """
        Function which iterates through the generator companies, requests their bids, orders them in order of price,
        and accepts bids.
        :param agents: All agents from simulation model.
        :param segment_hours: Value for number of hours particular electricity generation is required.
        :param segment_demand: Size of electricity consumption required.
        :return: None
        """
        agent = self.model.schedule.agents
        generator_companies = [x for x in agent if isinstance(x, GenCo)]  # Select of generation company agents
        
        for segment_hour, segment_demand in zip(segment_hours, segment_demand):
            bids = []
            for generation_company in generator_companies:
                bids.append(generation_company.calculate_bids(segment_hour, segment_demand))
            sorted_bids = self._sort_bids(bids)
            accepted_bids = self._respond_to_bids(sorted_bids, segment_demand)

            logger.debug("segment hour: {}".format(segment_hour))
            self._accept_bids(accepted_bids)
            highest_bid = accepted_bids[-1].price_per_mwh
            self._create_load_duration_price_curve(segment_hour, segment_demand, highest_bid)

        self.load_duration_curve_prices = pd.DataFrame(self.hold_duration_curve_prices)

    def adjust_load_duration_curve_for_renewables(self):

        onshore_plants = WorldPlantCapacity(self.model).get_renewable_by_type("Onshore")
        total_onshore_capacity = sum(onshore_plant.capacity_mw for onshore_plant in onshore_plants)

        offshore_plants = WorldPlantCapacity(self.model).get_renewable_by_type("Offshore")
        total_offshore_capacity = sum(offshore_plant.capacity_mw for offshore_plant in offshore_plants)

        pv_plants = WorldPlantCapacity(self.model).get_renewable_by_type("PV")
        total_pv_capacity = sum(pv_plant.capacity_mw for pv_plant in pv_plants)



        # agent = self.model.schedule.agents
        #
        # generator_companies = [x for x in agent if isinstance(x, GenCo)]  # Select of generation company agents
        #
        # renewable_bids = []
        # for genco in generator_companies:
        #     renewable_bids.append(genco.calculate_non_fuel_bids())
        #
        # [demand for demand in segment_demand]


    def _create_load_duration_price_curve(self, segment_hour, segment_demand, accepted_price):
        segment_price_data = {
                'year': self.model.year_number,
                'segment_hour': segment_hour,
                'segment_demand': segment_demand,
                'accepted_price': accepted_price
            }

        self.hold_duration_curve_prices.append(segment_price_data)


    @staticmethod
    def _accept_bids(accepted_bids):
        highest_accepted_bid = accepted_bids[-1].price_per_mwh
        logger.info("Highest accepted bid price: {}".format(highest_accepted_bid))
        for bids in accepted_bids:
            logger.debug("bid price: {}, plant name: {}, plant capacity: {}".format(bids.price_per_mwh, bids.plant.name, bids.plant.capacity_mw))
            bids.price_per_mwh = highest_accepted_bid

    @staticmethod
    def _sort_bids(bids):
        """
        Sorts bids in order of price
        :param bids: Bid objects
        :return: Return bids in order of price
        """
        bids = list(chain.from_iterable(bids))
        sorted_bids = sorted(bids, key=lambda x: x.price_per_mwh)
        return sorted_bids

    @staticmethod
    def _respond_to_bids(bids, capacity_required):
        """
        Response to bids based upon price and capacity required. Accepts bids in order of cheapest generator.
        Continues to accept bids until capacity is met for those hours.
        :param bids: Bid objects
        :param capacity_required: Capacity required for this segment
        :return:
        """
        accepted_bids = []
        for bid in bids:
            if capacity_required > bid.capacity_bid:
                bid.accept_bid()
                capacity_required -= bid.capacity_bid
                accepted_bids.append(bid)
            elif bid.capacity_bid > capacity_required > 0:
                bid.partially_accept_bid(capacity_required)
                capacity_required = 0
                accepted_bids.append(bid)
            else:
                bid.reject_bid()
        return accepted_bids
