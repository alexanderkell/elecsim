"""nuclear.py: Class which represents a nuclear power plant"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"

from elecsim.src.plants.power_plant import PowerPlant


class Nuclear(PowerPlant):

    def __init__(self, min_running=5000, lifetime=40, down_payment=900000000, ann_cost=231000000, depreciation=25, operating_cost=75500000, capacity=1000, construction_time=8, carbon_emissions=50):
        # Initialise power plant
        super().__init__(min_running, lifetime, down_payment, ann_cost, depreciation, operating_cost, capacity, construction_time, carbon_emissions)




    def __str__(self):
        ret = 'Capacity Fulfilled: '+str(self.capacity_fulfilled) + '. Minimum running time: ' + str(self.min_running) + ', Lifetime: ' + str(self.lifetime) + ', Down payment: ' + str(self.down_payment) + ', Annualized investment cost: ' + str(self.ann_cost) + ', Depreciation time: ' + str(self.depreciation) + ', Operating Cost: ' + str(self.operating_cost) + ', Capacity: ' + str(self.capacity) + ', Construction Time: ' + str(self.construction_time) + ", Plant object: "+self.__repr__()+"."
        return ret
