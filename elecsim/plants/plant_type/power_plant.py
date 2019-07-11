"""power_plant.py: Class which represents a Power Plant"""

import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)
__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"


class PowerPlant(ABC):
    def __init__(self, name, plant_type, capacity_mw, construction_year, average_load_factor, pre_dev_period, construction_period, operating_period, pre_dev_spend_years, construction_spend_years, pre_dev_cost_per_mw, construction_cost_per_mw, infrastructure, fixed_o_and_m_per_mw, variable_o_and_m_per_mwh, insurance_cost_per_mw, connection_cost_per_mw):
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
        :param pre_dev_cost_per_mw: Cost of pre-development per kW of capacity
        :param construction_cost_per_mw: Cost of construction per kW of capacity
        :param infrastructure: Infrastructure cost in GBP
        :param fixed_o_and_m_per_mw: Fixed operation and maintenance cost
        :param variable_o_and_m_per_mwh: Variable operation and maintenance cost
        :param insurance_cost_per_mw: Insurance cost
        :param connection_cost_per_mw: Connection and use of system cost
        """

        # Data from BEIS
        self.name = name

        self.plant_type = plant_type

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

        self.is_operating = False


        #
        # self.min_running = min_running


        # Bids
        self.accepted_bids = []
        self.historical_bids = []

        self.capacity_fulfilled = {
            0.08: 0,
            460.75: 0,
            921.42: 0,
            1382.08: 0,
            1842.67: 0,
            2303.33: 0,
            2764: 0,
            3224.67: 0,
            3685.33: 0,
            4146: 0,
            4606.58: 0,
            5067.25: 0,
            5527.92: 0,
            5988.58: 0,
            6449.25: 0,
            6909.92: 0,
            7370.5: 0,
            7831.17: 0,
            8291.83: 0,
            8752.5: 0
        }

    # @property
    # def infrastructure(self):
    #     return self._infrastructure
    #
    # @infrastructure.setter
    # def infrastructure(self, value):
    #     self._infrastructure = value * constants.KW_TO_MW


    #     # Bids
    #     self.accepted_bids = []


    # def reset_plant_contract(self):
    #     self.capacity_fulfilled = {key: 0 for key in self.capacity_fulfilled}

    def delete_old_plant_bids(self):
        self.historical_bids.extend(self.accepted_bids)
        self.accepted_bids = []

    def get_upfront_costs(self):
        upfront_cost = self.capacity_mw*(self.pre_dev_cost_per_mw+self.construction_cost_per_mw) + self.infrastructure
        return upfront_cost

    @abstractmethod
    def short_run_marginal_cost(self, model, genco, fuel_price, co2_price):
        pass

    def get_fixed_annual_payments(self):
        pass

    def check_if_operating_in_certain_year(self, current_year, year_difference_from_model_year):
        year_operation_begins = self.get_year_of_operation()
        end_of_life = year_operation_begins + self.operating_period
        year_to_check = year_difference_from_model_year + current_year
        if year_operation_begins < year_to_check <= end_of_life:
            return True
        else:
            return False

    def get_year_of_operation(self):
        year_operation_begins = self.construction_year + self.pre_dev_period + self.construction_period
        return year_operation_begins
    
    def __str__(self):
        ret = "Name: {}. Type: {}. Capacity: {}.".format(self.name, self.plant_type, self.capacity_mw)
        return ret

    def __repr__(self):
        return 'PowerPlant({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})'.format(self.name, self.plant_type, self.capacity_mw, self.construction_year, self.average_load_factor, self.pre_dev_period, self.construction_period, self.operating_period, self.pre_dev_spend_years, self.construction_spend_years, self.pre_dev_cost_per_mw, self.construction_cost_per_mw, self.infrastructure, self.fixed_o_and_m_per_mw, self.variable_o_and_m_per_mwh, self.insurance_cost_per_mw, self.connection_cost_per_mw)

