from mesa import Agent
from random import randint

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
        ldc_func = ldc.values.tolist()
        bid = []

        for i in range(len(self.plants)):
            plant = self.plants[i]
            bid_per_segment = ldc.values.tolist()
            final_bid = []
            for j in range(len(bid_per_segment)):
                if bid_per_segment[j][0] > plant.min_running:
                    final_bid.append(bid_per_segment[j] + [((plant.down_payment/plant.lifetime + plant.ann_cost + plant.operating_cost)/(plant.capacity*ldc_func[j][0]))*1.1])
            bid.append(Bid(plant,final_bid))
        return bid

    # def purchase_fuel(self):

    def invest(self):
        plant_to_invest = Nuclear(ann_cost=randint(100000000,300000000))
        self.plants.append(plant_to_invest)


class Bid:

    def __init__(self, plant, ldc_bids):
        self.plant = plant
        self.ldc_bids = ldc_bids


    def __str__(self):
        return "Plant type: " + self.plant.type + ", Min running time: " +str(self.plant.min_running)+", Bids: "+str(self.ldc_bids)
