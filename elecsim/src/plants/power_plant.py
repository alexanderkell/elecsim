"""power_plant.py: Class which represents a photovoltaic farm"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"


class PowerPlant:

    def __init__(self, name, type, capacity, efficiency, pre_dev_period, construction_period, operating_period, pre_dev_spend_years, construction_spend_years, pre_dev_cost, construction_cost, infrastructure, fixed_o_and_m, variable_o_and_m, insurance_cost, connection_cost):
        """
        PowerPlant class which are built and operated by generation companies
        :param name: Name of power plant
        :param type: Type of power plant
        :param capacity: Capacity of power plant (MW)
        :param efficiency: Efficiency of using fuel
        :param pre_dev_period: Amount of time construction spends in pre-development
        :param construction_period: Amount of time construction spends in construction
        :param operating_period: How long the power plant remains operational
        :param pre_dev_spend_years: Percentage of costs that are spread over each year of pre-development
        :param construction_spend_years: Percentage of costs that are spread over each year of construction
        :param pre_dev_cost: Cost of pre-development
        :param construction_cost: Cost of construction
        :param infrastructure: Infrastructure cost
        :param fixed_o_and_m: Fixed operation and maintenance cost
        :param variable_o_and_m: Variable operation and maintenance cost
        :param insurance_cost: Insurance cost
        :param connection_cost: Connection and use of system cost
        """

        self.name = name

        self.type = type

        self.capacity = capacity

        self.efficiency = efficiency

        self.pre_dev_period = pre_dev_period
        self.pre_dev_spend_years = pre_dev_spend_years

        self.construction_period = construction_period
        self.construction_spend_years = construction_spend_years

        self.operating_period = operating_period

        self.pre_dev_cost = pre_dev_cost

        self.construction_cost = construction_cost

        self.infrastructure = infrastructure

        self.fixed_o_and_m = fixed_o_and_m

        self.variable_o_and_m = variable_o_and_m

        self.insurance_cost = insurance_cost

        self.connection_cost = connection_cost


        # Bids
        self.accepted_bids = []



    # def __init__(self, name, constructionStartTime, min_running, lifetime, down_payment, ann_cost, depreciation, operating_cost, capacity, construction_time, carbon_emissions, efficiency):
    #     # Fixed definitions
    #
    #     #
    #     self.name = name
    #
    #     self.type = type
    #
    #
    #
    #     # Construction details
    #     self.constructionStartTime = constructionStartTime
    #
    #
    #     self.min_running = min_running
    #     self.lifetime = lifetime
    #     self.down_payment = down_payment
    #     self.ann_cost = ann_cost
    #     self.depreciation = depreciation
    #     self.operating_cost = operating_cost
    #     self.capacity = capacity
    #     self.construction_time = construction_time
    #     self.efficiency = efficiency
    #
    #
    #     # Variable definitions
    #     self.capacity_fulfilled = 0
    #     self.CO2_emissions = carbon_emissions
    #
    #     # Bids
    #     self.accepted_bids = []

    def reset_plant_contract(self):
        self.capacity_fulfilled = 0




    def __str__(self):
        ret = 'Variable Parameters: '+str(self.capacity_fulfilled) + '. Fixed Parameters: Minimum running time: ' + str(self.min_running) + ', Lifetime: ' + str(self.lifetime) + ', Down payment: ' + str(self.down_payment) + ', Annualized investment cost: ' + str(self.ann_cost) + ', Depreciation time: ' + str(self.depreciation) + ', Operating Cost: ' + str(self.operating_cost) + ', Capacity: ' + str(self.capacity) + ', Construction Time: ' + str(self.construction_time) + "."
        return ret











