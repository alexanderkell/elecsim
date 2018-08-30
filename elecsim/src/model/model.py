"""Model.py: Model for the electricity landscape world"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"

from mesa import Model
from elecsim.src.mesa_addons.scheduler_addon import OrderedActivation

from elecsim.src.agents.generation_company.gen_co import GenCo
from elecsim.src.agents.demand.demand import Demand
from elecsim.src.power_exchange.power_exchange import PowerEx
from elecsim.src.data.uk_gencos_and_plants import company_names

import pandas as pd


class Model(Model):
    """
    Model for the electricity landscape world
    """

    def __init__(self, scenario):
        # Set up model objects
        self.schedule = OrderedActivation(self)

        self.demand = Demand(1 ,scenario.segment_time, scenario.segment, scenario.yearly_demand_change)
        self.schedule.add(self.demand)

        # Create PowerExchange
        self.PowerExchange = PowerEx(self)
        self.schedule.add(self.PowerExchange)

        # # Create and add generation companies
        # for i in range(scenario.number_of_gencos):
        #     gen_co = GenCo(i, self, scenario.generators_owned[i], scenario.starting_money_of_gencos[i], )
        #     self.schedule.add(gen_co)

        plant_data=scenario.power_plants
        names = company_names(plant_data)

        for i in range(len(names)):
            gen_co = GenCo(i, self, name=names[i])
            rows = plant_data.loc[plant_data['Company'] == names[i]]
            plants = []
            for j in range(len(rows)):
                # plants.append()
                print(rows.iloc[j])
                print(rows.iloc[j].Name)
                print(rows.iloc[j].Fuel)
                print(rows.iloc[j].Capacity)
                print(rows.iloc[j].Start_date)
            self.schedule.add(gen_co)
            print('-------------- NEW COMPANY --------------')
        # Set running to true
        self.running = True

    def step(self):
        '''Advance model by one step'''
        self.schedule.step()

        self.PowerExchange.tender_bids(self.schedule.agents, self.demand.segment_hours, self.demand.segment_consumption)
