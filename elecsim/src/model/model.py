"""Model.py: Model for the electricity landscape world"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"

from mesa import Model
from elecsim.src.mesaaddons.scheduler_addon import OrderedActivation

from elecsim.src.agents.generation_company.gen_co import GenCo
from elecsim.src.agents.demand.demand import Demand
from elecsim.src.power_exchange.power_exchange import PowerEx

import elecsim.src.scenario.scenario_data as Scen

import pandas as pd


class Model(Model):
    """
    Model for the electricity landscape world
    """

    def __init__(self, demand):
        # Set up model objects
        self.schedule = OrderedActivation(self)

        self.demand = Demand(Scen.segment_time, Scen.segment, Scen.yearly_demand_change)
        self.schedule.add(self.demand)

        # Create PowerExchange
        self.PowerExchange = PowerEx(self)
        self.schedule.add(self.PowerExchange)

        # Create and add generation companies
        for i in range(Scen.number_of_gencos):
            gen_co = GenCo(i, self, Scen.generators_owned[i], Scen.starting_money_of_gencos[i],)
            self.schedule.add(gen_co)

        # Set running to true
        self.running = True

    def step(self):
        '''Advance model by one step'''
        self.schedule.step()

        self.PowerExchange.tender_bids(self.schedule.agents, self.demand.segment_hours, self.demand.segment_consumption)
