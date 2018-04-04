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

    def tender_bids(self, agents, ldc):
        bids = []

        generator_companies = [x for x in agents if isinstance(x, GenCo)]  # Select on generation company agents
        for i in range(len(generator_companies)):
            print("Generator company number: "+str(i))
            # bids = generator_companies[i].calculate_bids(ldc)
            bids.append(generator_companies[i].calculate_bids(ldc))
        bids = list(chain.from_iterable(bids))
        # print(len(bids[0].ldc_bids))
        print(bids[0])
        self.sort_bid_price(bids)

    def sort_bid_price(self, bids):
        for k in range(len(bids[0].ldc_bids)):
            ordered_bids = []
            for l in range(len(bids)):
                # if len(bids[l].ldc_bids[k]) > 2:
                ordered_bids.append([bids[l].plant, bids[l].ldc_bids[k]])
                # print(bids[l])
            ordered_bids = sorted(ordered_bids, key=lambda x: x[1][2])
            print(ordered_bids)

        # print(generator_companies.sort(key=sort_bid_price))

    def step(self):
        print("Stepping power exchange")

