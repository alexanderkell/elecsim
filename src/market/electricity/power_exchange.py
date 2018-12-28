from itertools import chain
from mesa import Agent

import logging
logger = logging.getLogger(__name__)


from src.agents.generation_company.gen_co import GenCo



"""power_exchange.py: Functionality to run power exchange"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"


class PowerExchange(Agent):

    def __init__(self, unique_id, model):
        """
        Power exchange agent which contains functionality to tender and respond to bids.
        :param model: Model in which the agents are contained in.
        """

        super().__init__(model=model, unique_id=unique_id)

    def tender_bids(self, segment_hours, segment_values):
        """
        Function which iterates through the generator companies, requests their bids, orders them in order of price,
        and accepts bids.
        :param agents: All agents from simulation model.
        :param segment_hours: Value for number of hours particular electricity generation is required.
        :param segment_values: Size of electricity consumption required.
        :return: None
        """
        agent = self.model.schedule.agents

        generator_companies = [x for x in agent if isinstance(x, GenCo)]  # Select of generation company agents
        for seg_hour, seg_value in zip(segment_hours, segment_values):
            bids = []
            for generation_company in generator_companies:
                bids.append(generation_company.calculate_bids(seg_hour, seg_value))
            sorted_bids = self.sort_bids(bids)
            accepted_bids = self.respond_to_bids(sorted_bids, seg_value)
            self.accept_bids(accepted_bids)

    @staticmethod
    def accept_bids(accepted_bids):
        highest_accepted_bid = accepted_bids[-1].price_per_mwh
        logger.debug("Highest accepted bid price: {}".format(highest_accepted_bid))
        for bids in accepted_bids:
            bids.price_per_mwh = highest_accepted_bid



    @staticmethod
    def sort_bids(bids):
        """
        Sorts bids in order of price
        :param bids: Bid objects
        :return: Return bids in order of price
        """
        bids = list(chain.from_iterable(bids))
        sorted_bids = sorted(bids, key=lambda x: x.price_per_mwh)
        return sorted_bids

    @staticmethod
    def respond_to_bids(bids, capacity_required):
        """
        Response to bids based upon price and capacity required. Accepts bids in order of cheapest generator.
        Continues to accept bids until capacity is met for those hours.
        :param bids: Bid objects
        :param capacity_required: Capacity required for this segment
        :return:
        """
        logger.info("Segment electricity demand: {}".format(capacity_required))
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

    def step(self):
        logger.debug("Stepping power exchange")

