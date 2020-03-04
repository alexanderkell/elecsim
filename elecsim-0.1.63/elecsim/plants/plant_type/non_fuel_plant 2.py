from functools import lru_cache

from elecsim.plants.plant_type.power_plant import PowerPlant
from elecsim.role.plants.costs.non_fuel_cost_calculations import NonFuelCostCalculation

""" no_fuel_plant.py: Child class of power plant which contains functions for a power plant that does not require fuel"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"


class NonFuelPlant(PowerPlant):

    def __init__(self, name, plant_type, construction_year, capacity_mw, average_load_factor, pre_dev_period, construction_period, operating_period, pre_dev_spend_years, construction_spend_years, pre_dev_cost_per_mw, construction_cost_per_mw, infrastructure, fixed_o_and_m_per_mw, variable_o_and_m_per_mwh, insurance_cost_per_mw, connection_cost_per_mw, efficiency):
        """
        Power plant of type that does not use plant_type.
        """
        super().__init__(name, plant_type, capacity_mw, construction_year, average_load_factor, pre_dev_period, construction_period, operating_period, pre_dev_spend_years, construction_spend_years, pre_dev_cost_per_mw, construction_cost_per_mw, infrastructure, fixed_o_and_m_per_mw, variable_o_and_m_per_mwh, insurance_cost_per_mw, connection_cost_per_mw)

        self.efficiency = efficiency
        self.min_running = 0

    def calculate_lcoe(self, discount_rate):
        lcoe_object = NonFuelCostCalculation(capacity_mw=self.capacity_mw, construction_year=self.construction_year, average_load_factor=self.average_load_factor, efficiency=self.efficiency, pre_dev_period=self.pre_dev_period, construction_period=self.construction_period, operating_period=self.operating_period, pre_dev_spend_years=self.pre_dev_spend_years, construction_spend_years=self.construction_spend_years, pre_dev_cost_per_mw=self.pre_dev_cost_per_mw, construction_cost_per_mw=self.construction_cost_per_mw, infrastructure=self.infrastructure, fixed_o_and_m_per_mw=self.fixed_o_and_m_per_mw, variable_o_and_m_per_mwh=self.variable_o_and_m_per_mwh, insurance_cost_per_mw=self.insurance_cost_per_mw, connection_cost_per_mw=self.connection_cost_per_mw)
        lcoe = lcoe_object.calculate_lcoe(discount_rate)
        return lcoe

    @lru_cache(maxsize=1024)
    def short_run_marginal_cost(self, model, genco, fuel_price=None, co2_price=None):
        plant_cost_calculations = NonFuelCostCalculation(capacity_mw=self.capacity_mw, construction_year=self.construction_year, average_load_factor=self.average_load_factor, efficiency=self.efficiency, pre_dev_period=self.pre_dev_period, construction_period=self.construction_period, operating_period=self.operating_period, pre_dev_spend_years=self.pre_dev_spend_years, construction_spend_years=self.construction_spend_years, pre_dev_cost_per_mw=self.pre_dev_cost_per_mw, construction_cost_per_mw=self.construction_cost_per_mw, infrastructure=self.infrastructure, fixed_o_and_m_per_mw=self.fixed_o_and_m_per_mw, variable_o_and_m_per_mwh=self.variable_o_and_m_per_mwh, insurance_cost_per_mw=self.insurance_cost_per_mw, connection_cost_per_mw=self.connection_cost_per_mw)
        marginal_cost = plant_cost_calculations.calculate_short_run_marginal_cost(model)
        return marginal_cost
