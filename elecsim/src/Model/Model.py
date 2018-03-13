"""Model.py: Model for an area containing electricity consuming households"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"

from mesa import Model
from mesa.space import Grid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector

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
        self.grid = Grid(height, width, torus=False)
        self.schedule = RandomActivation(self)


    def step(self):
        '''Advance model by one step.'''
        self.schedule.step()

