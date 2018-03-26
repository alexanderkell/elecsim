"""gas.py: Agent which represents a gas power plant"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"

from mesa import Agent

class gas(Agent):

    def __init__(self, min_running, lifetime, down_payment, ann_cost, depreciation, operating_cost, max_load, construction_time):
        self.min_running = min_running
        self.lifetime = lifetime
        self.down_payment = down_payment
        self.ann_cost = ann_cost
        self.depreciation = depreciation
        self.operating_cost = operating_cost
        self.max_load = max_load
        self.construction_time = construction_time

        def step(self):

