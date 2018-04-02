"""demand.py: Agent which simulates the demand of the UK"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"

from mesa import Agent


class Demand(Agent):

    def __init__(self, load_duration_curve):
        """
        An agent representing UK electricity demand
        :param load_duration_curve: A series representing the load duration curve
        """
        self.load_duration_curve = load_duration_curve

    def step(self):
        print("Stepping demand")
        pass
        # load to change each year due to certain scenario

