"""power_exchange.py: Functionality to run power exchange"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"

from itertools import chain
from random import random

from mesa import Agent

from src.agents.generation_company.gen_co import GenCo


class PowerExchange(Agent):

    def __init__(self, model):
        """
        Power exchange agent which contains functionality to tender and respond to bids
        :param model: Model in which the agent is contained in
        """

        super().__init__(model=model, unique_id=random)

    def tender_bids(self, agents, segment_hours, segment_values):
        """
        Function which iterates through the generator companies, requests their bids, orders them in order of price,
        and accepts bids
        :param agents: All agents from simulation model
        :param segment_hours: Value for number of hours particular electricity generation is required
        :param segment_values: Size of electricity consumption required
        :return: None
        """
        generator_companies = [x for x in agents if isinstance(x, GenCo)]  # Select of generation company agents
        for j in range(len(segment_hours)):
            bids = []
            for i in range(len(generator_companies)):
                bids.append(generator_companies[i].calculate_bids(segment_hours[j], segment_values[j]))
            bids = list(chain.from_iterable(bids))
            sorted_bids = self.sort_bids(bids)
            self.bids_response(sorted_bids, segment_values[j])
        # self.accept_bids(sorted_bids)

    def sort_bids(self, bids):
        """
        Sorts bids in order of price
        :param bids: Bid objects
        :return: Return bids in order of price
        """
        sorted_bids = sorted(bids, key=lambda x: x.price_per_mwh)
        return(sorted_bids)

    def bids_response(self, bids, capacity_required):
        """
        Response to bids based upon price and capacity required. Accepts bids in order of cheapest generator.
        Continues to accept bids until capacity is met for those hours.
        :param bids: Bid objects
        :param capacity_required: Capacity required for this segment
        :return:
        """
        print("Segement electricity demand: "+str(capacity_required))
        for i in range(len(bids)):
            if capacity_required > bids[i].capacity_bid:
                bids[i].accept_bid()
                capacity_required -= bids[i].capacity_bid
            elif bids[i].capacity_bid > capacity_required > 0:
                bids[i].partially_accept_bid(capacity_required)
                capacity_required = 0
            else:
                bids[i].reject_bid()
            print("Capacity required: "+str(capacity_required))



    def step(self):
        print("Stepping power exchange")

