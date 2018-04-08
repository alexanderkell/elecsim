"""Bid.py: A class which holds information for each bid"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"


class Bid:

    def __init__(self, plant, ldc_bids, gen_co):
        self.gen_co = gen_co
        self.plant = plant
        self.ldc_bids = ldc_bids

    def __str__(self):
        return "Plant type: " + self.plant.type + ", Min running time: " +str(self.plant.min_running)+", Bids: "+str(self.ldc_bids)
