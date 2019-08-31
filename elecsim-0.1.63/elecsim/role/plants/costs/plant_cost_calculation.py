import logging

from elecsim import constants as constants

logger = logging.getLogger(__name__)
"""
File name: calculate_lcoe
Date created: 18/12/2018
Feature: #Enter feature description here
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"


class PlantCostCalculations:
    def __init__(self, capacity_mw, construction_year, average_load_factor, pre_dev_period, construction_period, operating_period, pre_dev_spend_years, construction_spend_years, pre_dev_cost_per_mw, construction_cost_per_mw, infrastructure, fixed_o_and_m_per_mw, variable_o_and_m_per_mwh, insurance_cost_per_mw, connection_cost_per_mw):
        self.capacity_mw = capacity_mw

        self.construction_year = construction_year

        self.average_load_factor = average_load_factor

        self.pre_dev_period = pre_dev_period
        self.pre_dev_spend_years = pre_dev_spend_years

        self.construction_period = construction_period
        self.construction_spend_years = construction_spend_years

        self.pre_dev_cost_per_mw = pre_dev_cost_per_mw

        self.construction_cost_per_mw = construction_cost_per_mw

        self.operating_period = operating_period

        self.infrastructure = infrastructure

        self.fixed_o_and_m_per_mw = fixed_o_and_m_per_mw

        self.variable_o_and_m_per_mwh = variable_o_and_m_per_mwh

        self.insurance_cost_per_mw = insurance_cost_per_mw

        self.connection_cost_per_mw = connection_cost_per_mw

    @property
    def infrastructure(self):
        return self._infrastructure

    @infrastructure.setter
    def infrastructure(self, value):
        self._infrastructure = value * constants.KW_TO_MW

    def _discount_data(self, variable, discount_rate):
        discount_multiplier = [1]

        for _ in range(len(variable)):
            discount_multiplier.extend([discount_multiplier[-1]/(1+discount_rate)])

        discounted_var = [a*b for a,b in zip(variable, discount_multiplier)]
        return discounted_var

    def _pre_dev_yearly_spend(self):
        """
        Calculate the yearly pre-development spend
        :return: List containing the spend per year for pre-development costs.
        """
        pre_dev_cost_total = self.pre_dev_cost_per_mw * self.capacity_mw # Total construction costs for power plant

        pre_dev_spend_per_year = [x*pre_dev_cost_total for x in self.pre_dev_spend_years]  # Creates a list containing pre development spend per year

        return pre_dev_spend_per_year

    def _construction_yearly_spend(self):
        """

        Calculate the cost of yearly construction spend. Includes infrastructure cost during the final year of construction.
        :return: List containing spend per year for construction
        """

        construction_cost_total = self.construction_cost_per_mw * self.capacity_mw # Total construction costs for power plant
        construction_spend_per_year = [x*construction_cost_total for x in self.construction_spend_years]  # Creates a list containing construction spend per year

        return construction_spend_per_year
        # infrastructure_gbp = self.infrastructure
        # construction_spend_per_year[-1] += infrastructure_gbp  # Infrastructure cost is taken into account in the final year of construction

        # return construction_spend_per_year

    def _capex(self):
        """
        Calculation of capital expenditure, which includes insurance, building and pre-development costs. This is done
        by adding pre-development yearly cost with construction yearly spend.
        :return: Capital expenditure cost
        """
        capex = self._pre_dev_yearly_spend() + self._construction_yearly_spend()
        capex[-1]+=self.infrastructure
        return capex

    def _insurance_cost(self):
        """
        Calculates the yearly insurance cost
        :return: List containing insurance cost for each year of the operating period
        """
        insurance_cost_total = [0] * int(self.pre_dev_period+self.construction_period) +[self.insurance_cost_per_mw * self.capacity_mw] * int(self.operating_period) # Calculation of insurance cost for this instance of a power plant
        return insurance_cost_total

    def _variable_o_and_m_cost(self):
        """
        Calculates the operating and maintenance cost per year. Makes an assumption based on average load factor.
        :return: List containing variable operating and maintenance cost for each year of the operating period.
        """
        variable_o_and_m_cost_per_year = self.variable_o_and_m_per_mwh * self.capacity_mw * 365 * 24 * self.average_load_factor  # Variable cost is calculated as a function of time plant is utilised in a year
        variable_o_and_m_cost_per_year = [0] * int(self.pre_dev_period+self.construction_period) + [variable_o_and_m_cost_per_year] * int(self.operating_period)
        return variable_o_and_m_cost_per_year

    def _fixed_o_and_m_cost(self):
        """
        Calculates the fixed operating and maintenance cost per year.
        :return: List containing fixed operating and maintenance cost for each year of the operating period.
        """
        fixed_o_and_m_per_mw_cost_total = self.fixed_o_and_m_per_mw * self.capacity_mw  # Fixed cost calculated for this instance of power plant
        fixed_o_and_m_per_mw_cost_total = [0] * int(self.pre_dev_period+self.construction_period) + [fixed_o_and_m_per_mw_cost_total] * int(self.operating_period)
        return fixed_o_and_m_per_mw_cost_total

    def _opex_cost(self):
        """
        Calculation of operating expenditure, which includes fixed and variable costs
        :return: Operating expenditure cost
        """

        insur_cost = self._insurance_cost()
        var_o_and_m_cost = self._variable_o_and_m_cost()
        fixed_o_and_m_cost = self._fixed_o_and_m_cost()

        opex = [sum(x) for x in zip(insur_cost, var_o_and_m_cost, fixed_o_and_m_cost)]

        return opex

    def _electricity_generated(self):
        """
        Estimates the amount of electricity generated over the lifetime of the project based on the average load factor
        :return: Returns a list containing the electricity generated per year
        """
        HOURS_IN_DAY = constants.HOURS_IN_DAY
        DAYS_IN_YEAR = constants.DAYS_IN_YEAR

        elec_gen = [self.capacity_mw * self.average_load_factor * HOURS_IN_DAY * DAYS_IN_YEAR] * int(self.operating_period)
        elec_gen = [0] * int(self.pre_dev_period+self.construction_period) + elec_gen

        return elec_gen

    def total_income(self, expected_sale_price):
        beginning_year_operation = self.construction_year
        end_of_lifetime_year = int(beginning_year_operation)+int(self.operating_period)+int(self.pre_dev_period+self.construction_period)
        years_of_plant_operation = range(int(beginning_year_operation), end_of_lifetime_year)

        yearly_return = self.capacity_mw*self.average_load_factor*365*24*expected_sale_price
        returns = [yearly_return]*(len(years_of_plant_operation)-int(self.construction_period+self.pre_dev_period))
        years_not_running = [0]*int(self.construction_period+self.pre_dev_period)
        expected_returns = years_not_running + returns
        return expected_returns

    def calculate_yearly_outflow(self):

        pre_development_cost = self.pre_dev_cost_per_mw * self.pre_dev_spend_years * self.capacity_mw
        construction_cost = self.pre_dev

        capital_cost = self.capacity_mw * (self.pre_dev_cost_per_mw + self.construction_cost_per_mw) + self.infrastructure
        logger.debug("capital cost: {}".format(capital_cost))
        yearly_capital_cost = capital_cost / self.operating_period
        logger.debug("yearly capital cost: {}".format(yearly_capital_cost))

        yearly_fixed_costs = self.capacity_mw* (self.fixed_o_and_m_per_mw + self.insurance_cost_per_mw + self.connection_cost_per_mw)

        logger.debug("yearly fixed costs: {}".format(yearly_fixed_costs))

        negative_yearly_cash_flow = yearly_fixed_costs + yearly_capital_cost
        return negative_yearly_cash_flow
