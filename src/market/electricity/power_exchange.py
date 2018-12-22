from itertools import chain
from random import random

from mesa import Agent

import logging
logger = logging.getLogger(__name__)


from src.agents.generation_company.gen_co import GenCo



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

        # super().__init__(model=model, unique_id=unique_id)
        self.model = model

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
        for j in range(len(segment_hours)):
            bids = []
            for generation_company in generator_companies:
                bids.append(generation_company.calculate_bids(segment_hours[j], segment_values[j]))
            bids = list(chain.from_iterable(bids))
            sorted_bids = self.sort_bids(bids)
            self.bids_response(sorted_bids, segment_values[j])
        # self.accept_bids(sorted_bids)

    @staticmethod
    def sort_bids(bids):
        """
        Sorts bids in order of price
        :param bids: Bid objects
        :return: Return bids in order of price
        """
        sorted_bids = sorted(bids, key=lambda x: x.price_per_mwh)
        return sorted_bids

    @staticmethod
    def bids_response(bids, capacity_required):
        """
        Response to bids based upon price and capacity required. Accepts bids in order of cheapest generator.
        Continues to accept bids until capacity is met for those hours.
        :param bids: Bid objects
        :param capacity_required: Capacity required for this segment
        :return:
        """
        logger.info("Segment electricity demand: {}".format(capacity_required))
        for bid in bids:
            if capacity_required > bid.capacity_bid:
                bid.accept_bid()
                capacity_required -= bid.capacity_bid
            elif bid.capacity_bid > capacity_required > 0:
                bid.partially_accept_bid(capacity_required)
                capacity_required = 0
            else:
                bid.reject_bid()

    def step(self):
        logger.debug("Stepping power exchange")

