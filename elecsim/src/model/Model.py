"""Model.py: Model for an area containing electricity consuming households"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"

from mesa import Model
from mesa.space import Grid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from elecsim.src.demandagents.HouseholdAgent import HouseholdAgent
from elecsim.src.data.data_import import read_smart_meter_data
import random

class World(Model):
    """
    Model for a world containing electricity consuming households
    """

    def __init__(self, height, width):
        """
        Create a new world of electricity consuming households.

        :param height: Height of the world
        :param width: Width of the world
        """

        # Initialize model parameters
        self.height = height
        self.width = width

        # Set up model objects
        self.schedule = RandomActivation(self)
        self.grid = Grid(height, width, torus=False)

        # Set up data
        self.data = read_smart_meter_data('/Users/b1017579/Documents/PhD/Projects/6. Agent Based Models/elecsim/elecsim/data/one_hour_30.csv')


        self.datacollector = DataCollector(
            model_reporters = {"AggregatedElectricity": lambda m: self.aggregated_elec_cons(m)}
        )

        # Place household in world for visualisation purposes
        for i in range(0, self.data.size):
            signal = list(self.data.iloc[i].tolist()[0])
            print(signal)
            household = HouseholdAgent(self, '0134T', (1, 1), False, signal)

            self.grid.place_agent(household, (random.randint(0,width-1), random.randint(0,height-1)))
            self.schedule.add(household)


        self.running=True

        self.datacollector.collect(self)



    def step(self):
        '''Advance model by one step.'''
        self.schedule.step()
        self.datacollector.collect(self)

    @staticmethod
    def aggregated_elec_cons(model):
        """
        Helper method to aggregate electricity consumption of all agents
        :param model: Model containing agents
        :return: Aggregated electricity consumption at timestep
        """

        agg_electricity_cons = 0
        for agent in model.schedule.agents:
            agg_electricity_cons += agent.current_elec
        return agg_electricity_cons
