"""gen_co.py: Agent which represents a generation company"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"

from mesa import Agent

from elecsim.src.plants.nuclear import Nuclear
# from elecsim.src.power_exchange.power_exchange import tender_bids

class GenCo(Agent):

    def __init__(self, plants=[]):
        self.plants = plants

    def step(self):
        print("Stepping")
        self.invest()
        # self.make_bid()

    def make_bid(self):
        print("Number of plants = "+str(len(self.plants))+"")
        print("Plants: " + str(self.plants))
        bids = []
        for i in range(len(self.plants)):
            plant = self.plants[i]
            yearly_cost = (plant.down_payment/plant.lifetime + plant.ann_cost + plant.operating_cost)/(plant.capacity*plant.min_running)
            bid_price = yearly_cost*1.1
            # print(yearly_cost)
            print("Sending bid")
            bids.append(Bid(plant, bid_price))
        return bids

    # def purchase_fuel(self):

    def invest(self):
        print("Purchasing nuclear power plant." + str(self))
        plant_to_invest = Nuclear()
        self.plants.append(plant_to_invest)
        print("Built plant: "+str(plant_to_invest.__repr__()))



class Bid:

    def __init__(self, plant, bid_price):
        self.plant = plant
        self.bid_price = bid_price

    def __str__(self):
        return "Plant type: " + self.plant.type + ", Capacity: " +str(self.plant.capacity)+ ", Min running time: " +str(self.plant.min_running)+", Bid Price: " +str(self.bid_price)+""
