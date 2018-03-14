"""Model.py: Model for an area containing electricity consuming households"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"

from mesa import Model
from mesa.space import Grid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from elecsim.src.Agents.HouseholdAgent import HouseholdAgent

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

        # Place household in world for visualisation purposes
        household = HouseholdAgent(self, '0134T', (1, 1), False, [1, 2, 3, 2, 1])
        self.grid.place_agent(household, (1, 1))
        self.schedule.add(household)
        self.running=True

        self.datacollector = DataCollector(
            agent_reporters={"electricity_cons": lambda household: household.electricity_cons}
        )


    def step(self):
        '''Advance model by one step.'''
        self.datacollector.collect(self)
        self.schedule.step()

