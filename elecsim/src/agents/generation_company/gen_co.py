from mesa import Agent

from elecsim.src.plants.nuclear import Nuclear


"""gen_co.py: Agent which represents a generation company"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"


class GenCo(Agent):

    def __init__(self, unique_id, model, plants=None):
        super().__init__(unique_id, model)
        if plants is None: plants = []
        self.plants = plants

    def step(self):
        print("Stepping generation company "+str(self.unique_id))
        self.invest()
        # self.make_bid()

    def calculate_bids(self, ldc):
        bids = []

        for i in range(len(self.plants)):
            plant = self.plants[i]
            yearly_max_cost = ((plant.down_payment/plant.lifetime + plant.ann_cost + plant.operating_cost)/(plant.capacity*plant.min_running))*1.1
            yearly_min_cost = ((plant.down_payment/plant.lifetime + plant.ann_cost + plant.operating_cost)/(plant.capacity*8760))*1.1
            # print(yearly_cost)
            print("Sending bid")
            bids.append(Bid(plant, yearly_max_cost, yearly_min_cost))
        return bids

    # def purchase_fuel(self):

    def invest(self):
        print("Purchasing nuclear power plant. " + str(self))
        plant_to_invest = Nuclear()
        self.plants.append(plant_to_invest)
        print("Built plant: "+str(plant_to_invest.__repr__())+" for company "+str(self))



class Bid:

    def __init__(self, plant, max_price, min_price):
        self.plant = plant
        self.max_price = max_price
        self.min_price = min_price

    def __str__(self):
        return "Plant type: " + self.plant.type + ", Capacity: " +str(self.plant.capacity)+ ", Min running time: " +str(self.plant.min_running)+", Max Price: " +str(self.max_price)+", Min Price: "+str(self.min_price)
