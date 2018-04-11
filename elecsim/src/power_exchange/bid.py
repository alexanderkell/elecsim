"""Bid.py: A class which holds information for each bid"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"


class Bid:

    def __init__(self, gen_co, plant, segment_hours, capacity_bid, price_per_mw):
        self.gen_co = gen_co
        self.plant = plant
        self.segment_hours = segment_hours
        self.capacity_bid = capacity_bid
        self.price_per_mw = price_per_mw

        self.bid_accepted = False
        self.bid_rejected = False
        self.partly_accepted = False

    def reject_bid(self):
        self.plant.capacity_fulfilled = 0
        self.bid_rejected=True

    def accept_bid(self):
        self.plant.capacity_fulfilled = self.plant.capacity_fulfilled + self.capacity_bid
        self.bid_accepted = True
        print("Bid accepted: "+str(self.plant))

    def partly_accept_bid(self, demand_fulfilled):
        self.plant.capacity_fulfilled = self.plant.capacity_fulfilled + demand_fulfilled
        self.partly_accepted = True
        print("Bid partly accepted: "+str(self.plant))

    def __str__(self):
        return "Plant type: " + self.plant.type + ", Min running time: " +str(self.plant.min_running)+", Number of hours: "+str(self.segment_hours)+", Capacity Bid: "+str(self.capacity_bid)+", Price per MW: "+str(self.price_per_mw)+", Plant: "+self.plant.__repr__()
