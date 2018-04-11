"""power_exchange.py: Functionality to run power exchange"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"


from elecsim.src.agents.generation_company.gen_co import GenCo
from random import random


from mesa import Agent
from itertools import chain

class PowerEx(Agent):

    def __init__(self, model):
        super().__init__(model=model, unique_id=random)

    def tender_bids(self, agents, segment_hours, segment_values):
        generator_companies = [x for x in agents if isinstance(x, GenCo)]  # Select on generation company agents
        for j in range(len(segment_hours)):
            bids = []
            for i in range(len(generator_companies)):
                bids.append(generator_companies[i].calculate_bids(segment_hours[j], segment_values[j]))
            bids = list(chain.from_iterable(bids))
            sorted_bids = self.sort_bids(bids)
            self.bids_response(sorted_bids, segment_values[j])
        # self.accept_bids(sorted_bids)

    def sort_bids(self, bids):
        sorted_bids = sorted(bids, key=lambda x: x.price_per_mw)
        return(sorted_bids)

    def bids_response(self, bids, capacity_required):
        print("Segement electricity demand: "+str(capacity_required))
        for i in range(len(bids)):
            # print("Bid #"+str(i)+": "+str(bids[i])+" repr: "+bids[i].plant.__repr__())
            if capacity_required > bids[i].capacity_bid:
                bids[i].accept_bid()
                capacity_required -= bids[i].capacity_bid
            elif bids[i].capacity_bid > capacity_required > 0:
                bids[i].partly_accept_bid(capacity_required)
                capacity_required = 0
            else:
                bids[i].reject_bid()
            print("Capacity required: "+str(capacity_required))



    def step(self):
        print("Stepping power exchange")

