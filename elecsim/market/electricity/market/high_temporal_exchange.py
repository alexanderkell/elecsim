from elecsim.market.electricity.power_exchange import PowerExchange

"""power_exchange.py: Functionality to run power exchange"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"

class HighTemporalExchange(PowerExchange):

    def __init__(self, model):
        super().__init__(model)
        self.model = model

    def tender_bids(self):
        pass

