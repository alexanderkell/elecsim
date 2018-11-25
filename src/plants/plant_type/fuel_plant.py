""" fuel_plant.py: Child class of power plant which contains functions for a power plant which consumes fuel.
                    Most notably, the functinos contain the ability to calculate the cost of fuel.
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"

from src.plants import PowerPlant
from src.plants import fuel_registry, plant_type_to_fuel


class FuelPlant(PowerPlant):

    def __init__(self, name, plant_type, capacity_mw, construction_year, average_load_factor, efficiency, pre_dev_period, construction_period, operating_period, pre_dev_spend_years, construction_spend_years, pre_dev_cost_per_kw, construction_cost_per_kw, infrastructure, fixed_o_and_m_per_mw, variable_o_and_m_per_mwh, insurance_cost_per_kw, connection_cost_per_kw):
        """
        Initialisation of plant_type power plant object.
        :param efficiency: Efficiency of power plant at converting plant_type energy into electrical energy.
        :param fuel: Type of plant_type that the power plant consumes.
        """
        super().__init__(name=name, type=plant_type, capacity_mw=capacity_mw, average_load_factor=average_load_factor, pre_dev_period=pre_dev_period, construction_period=construction_period, operating_period=operating_period, pre_dev_spend_years=pre_dev_spend_years, construction_spend_years=construction_spend_years, pre_dev_cost_per_kw=pre_dev_cost_per_kw, construction_cost_per_kw=construction_cost_per_kw, infrastructure=infrastructure, fixed_o_and_m_per_mw=fixed_o_and_m_per_mw, variable_o_and_m_per_mwh=variable_o_and_m_per_mwh, insurance_cost_per_kw=insurance_cost_per_kw, connection_cost_per_kw=connection_cost_per_kw, construction_year=construction_year)
        self.efficiency = efficiency
        # Finds fuel type of power plant eg. CCGT power plant type returns gas.
        fuel_string = plant_type_to_fuel(plant_type)
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
        capex = self.capex()
        opex = self.opex()
        elec_gen = self.electricity_generated()
        fuel_costs = self.fuel_costs(elec_gen)
        total_costs = self.total_costs(capex, opex, fuel_costs)

        # Costs discounted using discount_rate variable.
        disc_costs = self.discounted_variable(total_costs, discount_rate)
        disc_elec = self.discounted_variable(elec_gen, discount_rate)

        # All costs summed
        disc_total_costs = sum(disc_costs)
        disc_total_elec = sum(disc_elec)

        # LCOE calculated
        lcoe = disc_total_costs/disc_total_elec

        return lcoe

    def total_costs(self, capex, opex, fuel_costs):
        """
        Function which uses addition to calculate total costs from capital expenditure, operating expenditure and
        plant_type costs over the lifetime of the power plant.

        :param capex: Capital expenditure per year
        :param opex: Operating expenditure per year
        :param fuel_costs: fuel_costs per year
        :return: Total costs over lifetime of power plant
        """

        # Addition of operating expenditure and plant_type costs, followed by operating expenditure, plant_type costs and capital expenditure.
        opex_fuel = [sum(x) for x in zip(opex, fuel_costs)]
        capex.extend(opex_fuel)
        total_costs = [sum(x) for x in zip(opex_fuel, capex)]

        return total_costs

    def fuel_costs(self, electricity_generated):
        """
        Calculates the plant_type costs per year based on plant efficiency, electricity generated and endogenous gas prices
        :param electricity_generated: Electricity generated per year
        :return: Returns estimated cost of plant_type per year
        """

        fuel_costs = [0]*int(self.pre_dev_period+self.construction_period)+[(self.fuel.fuel_price[i] * electricity_generated[i])/self.efficiency for i in range(int(self.operating_period))]
        return fuel_costs

    def __repr__(self):
        return 'PowerPlant({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})'.format(self.name, self.type, self.capacity_mw, self.construction_year, self.average_load_factor, self.pre_dev_period, self.construction_period, self.operating_period, self.pre_dev_spend_years, self.construction_spend_years, self.pre_dev_cost_per_kw, self.construction_cost_per_kw, self._infrastructure, self.fixed_o_and_m_per_mw, self.variable_o_and_m_per_mwh, self.insurance_cost_per_kw, self.connection_cost_per_kw)


