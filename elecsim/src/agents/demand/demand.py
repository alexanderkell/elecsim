"""demand.py: Agent which simulates the demand of the UK"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"

from mesa import Agent


class Demand(Agent):

    def __init__(self, segment_hours, segment_consumption):
        """
        An agent representing UK electricity demand
        :param segment_hours: A series representing the load duration curve
        """
        self.segment_hours = segment_hours
        self.segment_consumption = segment_consumption

    def step(self):
        print("Stepping demand")
        pass
        # load to change each year due to certain scenario

