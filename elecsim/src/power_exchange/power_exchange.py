"""power_exchange.py: Functionality to run power exchange"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"


from elecsim.src.agents.generation_company.gen_co import GenCo
from elecsim.src.power_exchange.bid import Bid
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
        sorted_bids = self.sort_bid_price(bids)
        self.accept_bids(sorted_bids)

    def sort_bid_price(self, bids):
        all_bids = []
        print("bids: "+str(bids))
        for k in range(len(bids[0].ldc_bids)):
            ordered_bids = []
            for l in range(len(bids)):
                # if len(bids[l].ldc_bids[k]) > 2:
                ordered_bids.append([bids[l].gen_co, bids[l].plant, bids[l].ldc_bids[k]])
                print(ordered_bids[l][2][2])
            ordered_bids = sorted(ordered_bids, key=lambda x: x[2][2])
            # print("Capacity + all bids etc: "+str([ordered_bids[1][2][0], ordered_bids]))
            all_bids.append([ordered_bids[1][2][0],ordered_bids])
        print("all_bids: " +str(all_bids))
        return all_bids

    def accept_bids(self, bids):
        for i in range(len(bids)):
            print("Capacity required: "+str(bids[i][0]))
            print("First bid: "+str(bids[i][1][0][2][2]))
            print("First bid capacity: "+str(bids[i][1][0][1].capacity))

            capacity_required = bids[i][0]
            while capacity_required > 0:
                capacity_required = bids[i][0]
                for j in range(len(bids[i][1])):
                    station_capacity = bids[i][1][j][1].capacity
                    if capacity_required > station_capacity:
                        capacity_required = capacity_required - station_capacity
                        bids[i][1][j][1].capacity_fulfilled = station_capacity
                        print(bids[i][1][j][1].capacity_fulfilled)
                        print(capacity_required)
                    elif capacity_required < station_capacity and capacity_required > 0:
                        bids[i][1][j][1].capacity_fulfilled = capacity_required
                        capacity_required = 0
                    else:
                        print("Error")


    def step(self):
        print("Stepping power exchange")

