"""power_plant.py: Class which represents a photovoltaic farm"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"


class PowerPlant:

    def __init__(self, name, plant_type, capacity_mw, load_factor, efficiency, pre_dev_period, construction_period, operating_period, pre_dev_spend_years, construction_spend_years, pre_dev_cost_per_kw, construction_cost_per_kw, infrastructure, fixed_o_and_m_per_mw, variable_o_and_m_per_mwh, insurance_cost_per_kw, connection_cost_per_kw, min_running):
        """
        PowerPlant class which are built and operated by generation companies
        :param name: Name of power plant
        :param plant_type: Type of power plant
        :param capacity_mw: Capacity of power plant (MW)
        :param load_factor: Average amount of time that power plant is used

        :param pre_dev_period: Amount of time construction spends in pre-development
        :param construction_period: Amount of time construction spends in construction
        :param operating_period: How long the power plant remains operational
        :param pre_dev_spend_years: Percentage of costs that are spread over each year of pre-development
        :param construction_spend_years: Percentage of costs that are spread over each year of construction
        :param pre_dev_cost_per_kw: Cost of pre-development per kW of capacity
        :param construction_cost_per_kw: Cost of construction per kW of capacity
        :param infrastructure: Infrastructure cost
        :param fixed_o_and_m_per_mw: Fixed operation and maintenance cost
        :param variable_o_and_m_per_mwh: Variable operation and maintenance cost
        :param insurance_cost_per_kw: Insurance cost
        :param connection_cost_per_kw: Connection and use of system cost
        """

        # Data from BEIS
        self.name = name

        self.type = plant_type

        self.capacity_mw = capacity_mw

        self.load_factor = load_factor

        self.efficiency = efficiency

        self.pre_dev_period = pre_dev_period
        self.pre_dev_spend_years = pre_dev_spend_years

        self.construction_period = construction_period
        self.construction_spend_years = construction_spend_years

        self.pre_dev_cost_per_kw = pre_dev_cost_per_kw

        self.construction_cost_per_kw = construction_cost_per_kw

        self.operating_period = operating_period

        self.infrastructure = infrastructure

        self.fixed_o_and_m_per_mw = fixed_o_and_m_per_mw

        self.variable_o_and_m_per_mwh = variable_o_and_m_per_mwh

        self.insurance_cost_per_kw = insurance_cost_per_kw

        self.connection_cost_per_kw = connection_cost_per_kw

        #
        self.min_running = min_running


        # Bids
        self.accepted_bids = []



    # def __init__(self, name, constructionStartTime, min_running, lifetime, down_payment, ann_cost, depreciation, operating_cost, capacity, construction_time, carbon_emissions, efficiency):
    #     # Fixed definitions
    #
    #     #
    #     self.name = name
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

    def capex(self):
        """
        Calculation of capital expenditure, which includes insurance, building and pre-development costs
        :return: Capital expenditure cost
        """
        construction_cost_total = self.construction_cost_per_kw * 1000 * self.capacity_mw # Total construction costs for power plant
        pre_dev_cost_total = self.pre_dev_cost_per_kw * 1000 * self.capacity_mw # Total construction costs for power plant

        pre_dev_spend_per_year = [x*pre_dev_cost_total for x in self.pre_dev_spend_years]  # Creates a list containing pre development spend per year
        construction_spend_per_year = [x*construction_cost_total for x in self.construction_spend_years]  # Creates a list containing construction spend per year

        infrastructure_gbp = self.infrastructure * 1000
        construction_spend_per_year[-1] += infrastructure_gbp  # Infrastructure cost is taken into account in the final year of construction

        capex = pre_dev_spend_per_year + construction_spend_per_year
        return capex

    def opex(self):
        """
        Calculation of operating expenditure, which includes fixed and variable costs
        :return: Operating expenditure cost
        """
        # Opex
        insurance_cost_total = self.insurance_cost_per_kw * self.capacity_mw  # Calculation of insurance cost for this instance of a power plant
        variable_o_and_m_cost_per_year = self.variable_o_and_m_per_mwh * self.capacity_mw * 365 * 24 * self.load_factor  # Variable cost is calculated as a function of time plant is utilised in a year
        fixed_o_and_m_per_mw_cost_total = self.fixed_o_and_m_per_mw * self.capacity_mw  # Fixed cost calculated for this instance of power plant

        opex_year = insurance_cost_total + variable_o_and_m_cost_per_year + fixed_o_and_m_per_mw_cost_total  # Total opex is calculated
        opex = [opex_year] * self.operating_period  # Operating expenditure repeated
        return opex

    def electricity_generated(self):
        """
        Estimates the amount of electricity generated over the lifetime of the project based on the average load factor
        :return: Returns a list containing the electricity generated per year
        """
        elec_gen = [self.capacity_mw * self.load_factor * 24 * 365] * self.operating_period
        return elec_gen




    def __str__(self):
        # ret = 'Variable Parameters: '+str(self.capacity_fulfilled) + '. Fixed Parameters: Minimum running time: ' + str(self.min_running) + ', Lifetime: ' + str(self.lifetime) + ', Down payment: ' + str(self.down_payment) + ', Annualized investment cost: ' + str(self.ann_cost) + ', Depreciation time: ' + str(self.depreciation) + ', Operating Cost: ' + str(self.operating_cost) + ', Capacity: ' + str(self.capacity) + ', Construction Time: ' + str(self.construction_time) + "."
        ret = "Name: "+self.name+". Type: "+self.type+". Capacity: "+str(self.capacity_mw)
        return ret











