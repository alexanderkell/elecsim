"""power_plant.py: Class which represents a Power Plant"""

import constants as constants

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"


class PowerPlant:
    def __init__(self, name, plant_type, capacity_mw, construction_year, average_load_factor, pre_dev_period, construction_period, operating_period, pre_dev_spend_years, construction_spend_years, pre_dev_cost_per_kw, construction_cost_per_kw, infrastructure, fixed_o_and_m_per_mw, variable_o_and_m_per_mwh, insurance_cost_per_kw, connection_cost_per_kw):
        """
        PowerPlant class which are built and operated by generation companies
        :param name: Name of power plant
        :param plant_type: Type of power plant
        :param capacity_mw: Capacity of power plant (MW)
        :param construction_year: Year that the power plant was constructed
        :param average_load_factor: Average amount of time that power plant is used
        :param pre_dev_period: Amount of time construction spends in pre-development
        :param construction_period: Amount of time construction spends in construction
        :param construction_spend_years: Percentage of costs that are spread over each year of construction
        :param pre_dev_spend_years: Percentage of costs that are spread over each year of pre-development
        :param operating_period: How long the power plant remains operational
        :param pre_dev_cost_per_kw: Cost of pre-development per kW of capacity
        :param construction_cost_per_kw: Cost of construction per kW of capacity
        :param infrastructure: Infrastructure cost in GBP
        :param fixed_o_and_m_per_mw: Fixed operation and maintenance cost
        :param variable_o_and_m_per_mwh: Variable operation and maintenance cost
        :param insurance_cost_per_kw: Insurance cost
        :param connection_cost_per_kw: Connection and use of system cost
        """

        # Data from BEIS
        self.name = name

        self.type = plant_type

        self.capacity_mw = capacity_mw

        self.construction_year = construction_year

        self.average_load_factor = average_load_factor

        self.pre_dev_period = pre_dev_period
        self.pre_dev_spend_years = pre_dev_spend_years

        self.construction_period = construction_period
        self.construction_spend_years = construction_spend_years

        self.pre_dev_cost_per_kw = pre_dev_cost_per_kw

        self.construction_cost_per_kw = construction_cost_per_kw

        self.operating_period = operating_period

        self._infrastructure = infrastructure

        self.fixed_o_and_m_per_mw = fixed_o_and_m_per_mw

        self.variable_o_and_m_per_mwh = variable_o_and_m_per_mwh

        self.insurance_cost_per_kw = insurance_cost_per_kw

        self.connection_cost_per_kw = connection_cost_per_kw

        #
        # self.min_running = min_running


        # Bids
        self.accepted_bids = []

    @property
    def infrastructure(self):
        return self._infrastructure

    @infrastructure.setter
    def infrastructure(self, value):
        self._infrastructure = value * constants.KW_TO_MW_CONV

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


    def discounted_variable(self, variable, discount_rate):
        discount_multiplier = [1]

        for _ in range(len(variable)):
            discount_multiplier.extend([discount_multiplier[-1]/(1+discount_rate)])

        discounted_var = [a*b for a,b in zip(variable, discount_multiplier)]
        return discounted_var

    def pre_dev_yearly_spend(self):
        """
        Calculate the yearly pre-development spend
        :return: List containing the spend per year for pre-development costs.
        """
        pre_dev_cost_total = self.pre_dev_cost_per_kw * constants.KW_TO_MW_CONV * self.capacity_mw # Total construction costs for power plant

        pre_dev_spend_per_year = [x*pre_dev_cost_total for x in self.pre_dev_spend_years]  # Creates a list containing pre development spend per year

        return pre_dev_spend_per_year

    def construction_yearly_spend(self):
        """

        Calculate the cost of yearly construction spend. Includes infrastructure cost during the final year of construction.
        :return: List containing spend per year for construction
        """

        construction_cost_total = self.construction_cost_per_kw * constants.KW_TO_MW_CONV * self.capacity_mw # Total construction costs for power plant
        construction_spend_per_year = [x*construction_cost_total for x in self.construction_spend_years]  # Creates a list containing construction spend per year

        return construction_spend_per_year
        # infrastructure_gbp = self.infrastructure
        # construction_spend_per_year[-1] += infrastructure_gbp  # Infrastructure cost is taken into account in the final year of construction

        # return construction_spend_per_year

    def capex(self):
        """
        Calculation of capital expenditure, which includes insurance, building and pre-development costs. This is done
        by adding pre-development yearly cost with construction yearly spend.
        :return: Capital expenditure cost
        """
        capex = self.pre_dev_yearly_spend() + self.construction_yearly_spend()
        capex[-1]+=self.infrastructure
        return capex

    def insurance_cost(self):
        """
        Calculates the yearly insurance cost
        :return: List containing insurance cost for each year of the operating period
        """
        insurance_cost_total = [self.insurance_cost_per_kw * self.capacity_mw] * int(self.operating_period) # Calculation of insurance cost for this instance of a power plant
        return insurance_cost_total

    def variable_o_and_m_cost(self):
        """
        Calculates the operating and maintenance cost per year. Makes an assumption based on average load factor.
        :return: List containing variable operating and maintenance cost for each year of the operating period.
        """
        variable_o_and_m_cost_per_year = self.variable_o_and_m_per_mwh * self.capacity_mw * 365 * 24 * self.average_load_factor  # Variable cost is calculated as a function of time plant is utilised in a year
        variable_o_and_m_cost_per_year = [variable_o_and_m_cost_per_year] * int(self.operating_period)
        return variable_o_and_m_cost_per_year

    def fixed_o_and_m_cost(self):
        """
        Calculates the fixed operating and maintenance cost per year.
        :return: List containing fixed operating and maintenance cost for each year of the operating period.
        """
        fixed_o_and_m_per_mw_cost_total = self.fixed_o_and_m_per_mw * self.capacity_mw  # Fixed cost calculated for this instance of power plant
        fixed_o_and_m_per_mw_cost_total = [fixed_o_and_m_per_mw_cost_total] * int(self.operating_period)
        return fixed_o_and_m_per_mw_cost_total

    def opex(self):
        """
        Calculation of operating expenditure, which includes fixed and variable costs
        :return: Operating expenditure cost
        """

        insur_cost = self.insurance_cost()
        var_o_and_m_cost = self.variable_o_and_m_cost()
        fixed_o_and_m_cost = self.fixed_o_and_m_cost()

        opex = [0]*int(self.pre_dev_period+self.construction_period) + [sum(x) for x in zip(insur_cost, var_o_and_m_cost, fixed_o_and_m_cost)]

        return opex

    def electricity_generated(self):
        """
        Estimates the amount of electricity generated over the lifetime of the project based on the average load factor
        :return: Returns a list containing the electricity generated per year
        """
        HOURS_PER_DAY = 24
        DAYS_PER_YEAR = 356

        elec_gen = [self.capacity_mw * self.average_load_factor * HOURS_PER_DAY * DAYS_PER_YEAR] * int(self.operating_period)
        elec_gen = [self.pre_dev_period+self.construction_period]+elec_gen

        return elec_gen

    def __str__(self):
        ret = "Name: {}. Type: {}. Capacity: {}.".format(self.name, self.type, self.capacity_mw)
        return ret

    def __repr__(self):
        return 'PowerPlant({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})'.format(self.name, self.type, self.capacity_mw, self.construction_year, self.average_load_factor, self.pre_dev_period, self.construction_period, self.operating_period, self.pre_dev_spend_years, self.construction_spend_years, self.pre_dev_cost_per_kw, self.construction_cost_per_kw, self._infrastructure, self.fixed_o_and_m_per_mw, self.variable_o_and_m_per_mwh, self.insurance_cost_per_kw, self.connection_cost_per_kw)

