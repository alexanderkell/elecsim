"""Household.py: An agent representing a household in each city"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"

from mesa import Agent
from random import *

class HouseholdAgent(Agent):
    """
    An agent representing an electricity consuming household
    Attributes:
        x,y: Grid coordinates
        unique_id: Unique identifier for a household
        storage: Variable to store whether the household has an energy storage device
        electricty_cons: Electricity consumption variable
    """

    def __init__(self, unique_id, pos, storage, electricity_cons):
        super().__init__(unique_id, pos)
        self.pos = pos
        self.storage = storage
        self.electricity_cons = electricity_cons

    def step(self):
        if self.storage == False:
            if bool(random.getrandbits(1)):
                self.storage = True

