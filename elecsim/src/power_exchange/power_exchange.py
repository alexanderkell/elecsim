"""power_exchange.py: Functionality to run power exchange"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"


from elecsim.src.agents.generation_company.gen_co import GenCo
from random import random

from mesa import Agent

class PowerEx(Agent):

    def __init__(self, model):
        super().__init__(model=model, unique_id=random)

    def tender_bids(self, agents, ldc):
        generator_companies = [x for x in agents if isinstance(x, GenCo)]  # Select on generation company agents
        for i in range(len(generator_companies)):
            print("Generator company number: "+str(i)+", Generator company: "+generator_companies[i].__repr__())
            bids = generator_companies[i].calculate_bids(ldc)
            for j in range(len(bids)):
                print(bids[j])
        # print(generator_companies)

        def sort_bid_price(obj):
            return obj.bid_price

        # print(generator_companies.sort(key=sort_bid_price))


