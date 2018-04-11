from mesa import Agent
from random import randint

from elecsim.src.plants.nuclear import Nuclear
from elecsim.src.power_exchange.bid import Bid

"""gen_co.py: Agent which represents a generation company"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"


class GenCo(Agent):

    def __init__(self, unique_id, model, plants=None, money=5000000):
        super().__init__(unique_id, model)
        if plants is None: plants = []
        self.plants = plants
        self.money = money

    def step(self):
        print("Stepping generation company "+str(self.unique_id))
        self.invest()
        self.reset_contracts()
        # self.make_bid()

    def calculate_bids(self, segment_hour, segment_value):
        # ldc_func = ldc.values.tolist()
        bid = []
        for i in range(len(self.plants)):
            plant = self.plants[i]
            if plant.min_running <= segment_hour and plant.capacity_fulfilled < plant.capacity:
                price = ((plant.down_payment/plant.lifetime + plant.ann_cost + plant.operating_cost)/(plant.capacity*segment_hour))*1.1
                bid.append(Bid(self, plant, segment_hour, plant.capacity-plant.capacity_fulfilled, price))
        return bid

    # def purchase_fuel(self):

    def invest(self):
        plant_to_invest = Nuclear(ann_cost=randint(100000000, 300000000))
        self.plants.append(plant_to_invest)

    def reset_contracts(self):
        for i in range(len(self.plants)):
            self.plants[i].reset_plant_contract()
