"""Model.py: Model for the electricity landscape world"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"

from mesa import Model
from mesa.time import RandomActivation

from elecsim.src import GenCo


class Model(Model):
    """
    Model for the electricity landscape world
    """

    def __init__(self):
        # Set up model objects
        self.schedule = RandomActivation(self)

        # Create generation company
        gen_co = GenCo()


        # Set running to true
        self.running = True
