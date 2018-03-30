"""Model.py: Model for the electricity landscape world"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"

from mesa import Model
from mesa.time import RandomActivation

from elecsim.src.agents.generation_company.gen_co import GenCo
from elecsim.src.agents.demand.demand import Demand
from elecsim.src.power_exchange.power_exchange import tender_bids

import pandas as pd

class Model(Model):
    """
    Model for the electricity landscape world
    """

    def __init__(self):
        # Set up model objects
        self.schedule = RandomActivation(self)

        # Create and add generation company
        for i in range(3):
            gen_co = GenCo()
            self.schedule.add(gen_co)

        # Create demand agent

        self.ldc = pd.read_csv('/Users/b1017579/Documents/PhD/Projects/6. Agent Based Models/elecsim/elecsim/Data/load_dur_sample.csv')
        # print(ldc.demand)
        demand = Demand(self.ldc.demand)
        self.schedule.add(demand)

        # Set running to true
        self.running = True

    def step(self):
        '''Advance model by one step'''
        self.schedule.step()

        tender_bids(self.schedule.agents, self.ldc)
