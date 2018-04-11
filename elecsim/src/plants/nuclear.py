"""nuclear.py: Class which represents a nuclear power plant"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"

from elecsim.src.plants.power_plant import PowerPlant


class Nuclear(PowerPlant):

    def __init__(self, min_running=5000, lifetime=40, down_payment=900000000, ann_cost=231000000, depreciation=25, operating_cost=75500000, capacity=1000, construction_time=8):
        # Fixed definitions
        self.type = "Nuclear"
        self.min_running = min_running
        self.lifetime = lifetime
        self.down_payment = down_payment
        self.ann_cost = ann_cost
        self.depreciation = depreciation
        self.operating_cost = operating_cost
        self.capacity = capacity
        self.construction_time = construction_time

        # Variable definitions
        self.capacity_fulfilled = 0

    def reset_plant_contract(self):
        self.capacity_fulfilled = 0

    def __str__(self):
        ret = 'Capacity Fulfilled: '+str(self.capacity_fulfilled) + '. Minimum running time: ' + str(self.min_running) + ', Lifetime: ' + str(self.lifetime) + ', Down payment: ' + str(self.down_payment) + ', Annualized investment cost: ' + str(self.ann_cost) + ', Depreciation time: ' + str(self.depreciation) + ', Operating Cost: ' + str(self.operating_cost) + ', Capacity: ' + str(self.capacity) + ', Construction Time: ' + str(self.construction_time) + ", Plant object: "+self.__repr__()+"."
        return ret
