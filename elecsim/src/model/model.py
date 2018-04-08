"""Model.py: Model for the electricity landscape world"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"

from mesa import Model
# from mesa.time import RandomActivation
from elecsim.src.mesaaddons.scheduler_addon import OrderedActivation

from elecsim.src.agents.generation_company.gen_co import GenCo
from elecsim.src.agents.demand.demand import Demand
from elecsim.src.power_exchange.power_exchange import PowerEx

import pandas as pd


class Model(Model):
    """
    Model for the electricity landscape world
    """

    def __init__(self):
        # Set up model objects
        # self.schedule = RandomActivation(self)
        self.schedule = OrderedActivation(self)

        # Create demand agent
        ldc = pd.read_csv('/Users/b1017579/Documents/PhD/Projects/6. Agent Based Models/elecsim/elecsim/Data/ldc_diff.csv')
        print(ldc.head())

        self.demand = Demand(ldc)
        self.schedule.add(self.demand)

        # Create PowerExchange
        self.PowerExchange = PowerEx(self)
        self.schedule.add(self.PowerExchange)

        # Create and add generation companies
        for i in range(3):
            gen_co = GenCo(i,self)
            self.schedule.add(gen_co)

        # Set running to true
        self.running = True

    def step(self):
        '''Advance model by one step'''
        self.schedule.step()

        self.PowerExchange.tender_bids(self.schedule.agents, self.demand.load_duration_curve)
