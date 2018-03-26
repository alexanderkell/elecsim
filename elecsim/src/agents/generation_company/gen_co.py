"""gen_co.py: Agent which represents a generation company"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"

from mesa import Agent

from elecsim.src import Nuclear


class GenCo(Agent):

    def __init__(self, nuclear = []):
        self.nuclear = nuclear


    def step(self):
        self.invest()

    # def make_bid(self):


    # def purchase_fuel(self):


    def invest(self):
        self.nuclear.append(Nuclear(1,2,3,4,5,6,7,8))
