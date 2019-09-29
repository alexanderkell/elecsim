import logging
logger = logging.getLogger(__name__)

"""Bid.py: A class which holds information for each bid"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"


class Bid:

    def __init__(self, gen_co, plant, segment_hours, capacity_bid, price_per_mwh, year_of_bid):
        """Bid class that contains all the information related to the creation of bids

        :param gen_co: Generation company from which the bid originates from
        :param plant: Power plant from which the bid originates from
        :param segment_hours: Number of hours sent for bid
        :param capacity_bid: Electricity consumption bid amount
        :param price_per_mwh: Price bid per Megawatt Hour
        """
        self.gen_co = gen_co
        self.plant = plant
        self.segment_hours = segment_hours
        self.capacity_bid = capacity_bid
        self.price_per_mwh = price_per_mwh
        self.year_of_bid = year_of_bid
        self.price_bid = price_per_mwh

        self.bid_accepted = False
        self.bid_rejected = False
        self.partly_accepted = False

    def reject_bid(self, segment_hour):
        """
        Function to be called when bid is rejected
        :return: None
        """
        self.plant.capacity_fulfilled[segment_hour] = 0
        self.bid_rejected = True

    def accept_bid(self, segment_hour):
        """
        Function to be called when bid is accepted
        :return: None
        """
        # Update capacity of plant once bid is accepted

        # segment_hour = str(segment_hour)
        self.plant.capacity_fulfilled[segment_hour] = self.capacity_bid

        self.bid_accepted = True
        self.plant.accepted_bids.append(self)

        if self.plant.plant_type == "Nuclear" and self.gen_co.model.nuclear_subsidy is not None:
            self.price_per_mwh += self.gen_co.model.nuclear_subsidy

    def partially_accept_bid(self, segment_hour, demand_fulfilled):
        """
        Function to be called when bid is partially accepted
        :param demand_fulfilled:
        :return: None
        """
        # Update capacity of plant once bid is partly accepted
        self.plant.capacity_fulfilled[segment_hour] = demand_fulfilled
        self.partly_accepted = True
        self.plant.accepted_bids.append(self)



    def __str__(self):
        return "Plant type: " + self.plant.plant_type + ", Min running time: " +str(self.plant.min_running)+", Number of hours: "+str(self.segment_hours)+", Capacity Bid: "+str(self.capacity_bid)+", Price per MW: "+str(self.price_per_mwh) + ", Price Bid: "+str(self.price_bid)+", Plant: " + self.plant.__repr__()

    def to_dict(self):
        return {
            'plant_type': self.plant.plant_type,
            'segment_hours': self.segment_hours,
            'capacity_bid': self.capacity_bid
        }
