from src.role.plants.lcoe_calculation import LCOECalculation
from src.plants.fuel.fuel_registry.fuel_registry import fuel_registry, plant_type_to_fuel
from src.data_manipulation.data_modifications.extrapolation_interpolate import ExtrapolateInterpolate
from src.scenario.scenario_data import carbon_cost
from itertools import zip_longest

import logging
logging = logging.getLogger(__name__)

"""
File name: fuel_lcoe_calculation
Date created: 18/12/2018
Feature: #Enter feature description here
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"

class FuelPlantCostCalculations(LCOECalculation):

    def __init__(self, plant_type, capacity_mw, construction_year, average_load_factor, efficiency, pre_dev_period, construction_period, operating_period, pre_dev_spend_years, construction_spend_years, pre_dev_cost_per_mw, construction_cost_per_mw, infrastructure, fixed_o_and_m_per_mw, variable_o_and_m_per_mwh, insurance_cost_per_mw, connection_cost_per_mw):
        super().__init__(capacity_mw=capacity_mw, construction_year=construction_year, average_load_factor=average_load_factor, pre_dev_period=pre_dev_period, construction_period=construction_period, operating_period=operating_period, pre_dev_spend_years=pre_dev_spend_years, construction_spend_years=construction_spend_years, pre_dev_cost_per_mw=pre_dev_cost_per_mw, construction_cost_per_mw=construction_cost_per_mw, infrastructure=infrastructure, fixed_o_and_m_per_mw=fixed_o_and_m_per_mw, variable_o_and_m_per_mwh=variable_o_and_m_per_mwh, insurance_cost_per_mw=insurance_cost_per_mw, connection_cost_per_mw=connection_cost_per_mw)
        self.efficiency = efficiency
        # Finds fuel plant_type of power plant eg. CCGT power plant plant_type returns gas.
        fuel_string = plant_type_to_fuel(plant_type, self.construction_year)
        # Fuel object, containing information on fuel.
        self.fuel = fuel_registry(fuel_string)

    def calculate_lcoe(self, discount_rate):
        """
        Function which calculates the levelised cost of electricity for this power plant instance at a
        specified discount rate.

        :param discount_rate: The discount rate that is used for the calculation of the levelised cost of electricity.
        :return: Returns LCOE value for power plant
        """

        # Calculations of capital expenditure, operating expenditure, total expected electricity expenditure and plant_type cost
        # This is used to estimate a LCOE price.
        elec_gen, total_costs = self.calculate_total_costs()

        # Costs discounted using discount_rate variable.
        disc_costs = self._discount_data(total_costs, discount_rate)
        disc_elec = self._discount_data(elec_gen, discount_rate)

        # Sum total costs over life time of plant
        disc_total_costs = sum(disc_costs)
        disc_total_elec = sum(disc_elec)

        # LCOE calculated
        lcoe = disc_total_costs/disc_total_elec

        return lcoe

    def calculate_total_costs(self, estimated_fuel_prices=None, estimated_carbon_prices=None):
        capex = self._capex()
        opex = self._opex_cost()
        elec_gen = self._electricity_generated()
        fuel_costs = self._fuel_costs(elec_gen)
        carbon_costs = self._carbon_costs()
        total_costs = self._total_costs(capex, opex, fuel_costs, carbon_costs)

        return elec_gen, total_costs

    def _total_costs(self, capex, opex, fuel_costs, carbon_costs):
        """
        Function which uses addition to calculate total costs from capital expenditure, operating expenditure, fuel costs,
        and carbon costs for plant_type costs over the lifetime of the power plant.

        :param capex: Capital expenditure per year
        :param opex: Operating expenditure per year
        :param fuel_costs: _fuel_costs per year
        :return: Total costs over lifetime of power plant
        """

        # Addition of operating expenditure and plant_type costs, followed by operating expenditure, plant_type costs and capital expenditure.
        opex_fuel = [sum(x) for x in zip_longest(opex, fuel_costs, fillvalue=0)]

        opex_fuel_remove_0 = opex_fuel[int(self.construction_period+self.pre_dev_period):]
        capex.extend(opex_fuel_remove_0)
        sum_of_opex_fuel_capex = capex.copy()
        sum_of_carbon_opex_fuel_capex = [sum(x) for x in zip(sum_of_opex_fuel_capex, carbon_costs)]

        return sum_of_carbon_opex_fuel_capex

    def _fuel_costs(self, electricity_generated, fuel_price=None):
        """
        Calculates the plant_type costs per year based on plant efficiency, electricity generated and endogenous gas prices
        :param electricity_generated: Electricity generated per year
        :return: Returns estimated cost of plant_type per year
        """
        beginning_year_operation = self.construction_year
        end_of_lifetime_year = int(beginning_year_operation)+int(self.operating_period)+int(self.pre_dev_period+self.construction_period)
        years_of_plant_operation = range(int(beginning_year_operation), end_of_lifetime_year)

        if fuel_price is None:
            this_fuel_price = self.fuel.fuel_price[self.fuel.fuel_price.Fuel == self.fuel.fuel_type].dropna()
        else:
            this_fuel_price = fuel_price



        fuel_extrapolation = ExtrapolateInterpolate(this_fuel_price.Year, this_fuel_price.value)
        fuel_price = [(float(fuel_extrapolation(i)) * elec_gen)/self.efficiency for i, elec_gen in zip(years_of_plant_operation, electricity_generated)]

        return fuel_price

    def _carbon_emitted(self):
        """
        Calculates projected tonnes of CO2 emitted by power plant per year
        :return: A list containing tonnes of CO2 emitted per year
        """
        carbon_emitted = [self.fuel.mwh_to_co2e_conversion_factor * (elec_gen/self.efficiency) for elec_gen in self._electricity_generated()]
        return carbon_emitted

    def _carbon_costs(self, carbon_price = None):
        """
        Costs of carbon emissions based on carbon tax
        :return: Projected carbon costs per year in a list.
        """

        if carbon_price is not None:
            carbon_taxation_years = carbon_price
        else:
            year_of_beginning_operation = self.construction_year+self.pre_dev_period+self.construction_period
            carbon_taxation_years = carbon_cost[carbon_cost.year.between(int(self.construction_year), int(year_of_beginning_operation+self.operating_period-1))]

        carbon_emitted = self._carbon_emitted()

        carbon_costs = [carbon_tax * carb_emit for carbon_tax, carb_emit in zip(list(carbon_taxation_years.price), carbon_emitted)]
        return carbon_costs

    def _carbon_cost_total(self, carbon_costs):
        """
        Calculates the total cost of carbon over the lifetime of the power plant.
        :return: total carbon costs
        """
        carbon_costs_total = sum(carbon_costs)

        return carbon_costs_total

    def total_income(self, expected_sale_price):
        beginning_year_operation = self.construction_year
        end_of_lifetime_year = int(beginning_year_operation)+int(self.operating_period)+int(self.pre_dev_period+self.construction_period)
        years_of_plant_operation = range(int(beginning_year_operation), end_of_lifetime_year)

        yearly_return = self.capacity_mw*self.average_load_factor*365*24*expected_sale_price
        returns = [yearly_return]*(len(years_of_plant_operation)-int(self.construction_period+self.pre_dev_period))
        years_not_running = [0]*int(self.construction_period+self.pre_dev_period)
        expected_returns = years_not_running + returns
        return expected_returns


