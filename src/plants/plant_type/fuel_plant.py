from src.plants.plant_type.power_plant import PowerPlant
from src.plants.fuel.fuel_registry.fuel_registry import fuel_registry, plant_type_to_fuel
from src.scenario.scenario_data import carbon_cost_gbp
from itertools import zip_longest


""" fuel_plant.py: Child class of power plant which contains functions for a power plant which consumes fuel.
                    Most notably, the functinos contain the ability to calculate the cost of fuel.
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"


class FuelPlant(PowerPlant):

    def __init__(self, name, plant_type, capacity_mw, construction_year, average_load_factor, efficiency, pre_dev_period, construction_period, operating_period, pre_dev_spend_years, construction_spend_years, pre_dev_cost_per_mw, construction_cost_per_mw, infrastructure, fixed_o_and_m_per_mw, variable_o_and_m_per_mwh, insurance_cost_per_mw, connection_cost_per_mw):
        """
        Initialisation of plant_type power plant object.
        :param efficiency: Efficiency of power plant at converting plant_type energy into electrical energy.
        """
        super().__init__(name=name, plant_type=plant_type, capacity_mw=capacity_mw, average_load_factor=average_load_factor, pre_dev_period=pre_dev_period, construction_period=construction_period, operating_period=operating_period, pre_dev_spend_years=pre_dev_spend_years, construction_spend_years=construction_spend_years, pre_dev_cost_per_mw=pre_dev_cost_per_mw, construction_cost_per_mw=construction_cost_per_mw, infrastructure=infrastructure, fixed_o_and_m_per_mw=fixed_o_and_m_per_mw, variable_o_and_m_per_mwh=variable_o_and_m_per_mwh, insurance_cost_per_mw=insurance_cost_per_mw, connection_cost_per_mw=connection_cost_per_mw, construction_year=construction_year)
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
        carbon_costs = self.carbon_costs()

        total_costs = self.total_costs(capex, opex, fuel_costs, carbon_costs)

        # Costs discounted using discount_rate variable.
        disc_costs = self.discounted_variable(total_costs, discount_rate)
        disc_elec = self.discounted_variable(elec_gen, discount_rate)

        # All costs summed
        disc_total_costs = sum(disc_costs)
        disc_total_elec = sum(disc_elec)

        # LCOE calculated
        lcoe = disc_total_costs/disc_total_elec

        return lcoe

    def total_costs(self, capex, opex, fuel_costs, carbon_costs):
        """
        Function which uses addition to calculate total costs from capital expenditure, operating expenditure and
        plant_type costs over the lifetime of the power plant.

        :param capex: Capital expenditure per year
        :param opex: Operating expenditure per year
        :param fuel_costs: fuel_costs per year
        :return: Total costs over lifetime of power plant
        """

        # Addition of operating expenditure and plant_type costs, followed by operating expenditure, plant_type costs and capital expenditure.
        opex_fuel = [sum(x) for x in zip_longest(opex, fuel_costs, fillvalue=0)]

        opex_fuel_remove_0 = opex_fuel[int(self.construction_period+self.pre_dev_period):]
        capex.extend(opex_fuel_remove_0)
        sum_of_opex_fuel_capex = capex.copy()

        sum_of_carbon_opex_fuel_capex = [sum(x) for x in zip_longest(sum_of_opex_fuel_capex, carbon_costs)]

        return sum_of_carbon_opex_fuel_capex

    def fuel_costs(self, electricity_generated):
        """
        Calculates the plant_type costs per year based on plant efficiency, electricity generated and endogenous gas prices
        :param electricity_generated: Electricity generated per year
        :return: Returns estimated cost of plant_type per year
        """

        beginning_year_operation = self.construction_year
        end_of_lifetime_year = int(beginning_year_operation)+int(self.operating_period)+int(self.pre_dev_period+self.construction_period)
        years_of_plant_operation = range(int(beginning_year_operation), end_of_lifetime_year)

        this_fuel_price = self.fuel.fuel_price[self.fuel.fuel_price.Fuel == self.fuel.fuel_type]
        fuel_costs = [(float(this_fuel_price.iloc[0][str(i)]) * elec_gen)/self.efficiency for i, elec_gen in zip(years_of_plant_operation, electricity_generated)]
        return fuel_costs

    def carbon_emitted(self):
        """
        Calculates projected tonnes of CO2 emitted by power plant per year
        :return: A list containing tonnes of CO2 emitted per year
        """
        carbon_emitted = [self.fuel.mwh_to_co2e_conversion_factor*(elec_gen/self.efficiency) for elec_gen in self.electricity_generated()]
        return carbon_emitted

    def carbon_costs(self):
        """
        Costs of carbon emissions based on carbon tax
        :return: Projected carbon costs per year in a list.
        """
        carbon_emitted = self.carbon_emitted()

        years_of_operation = self.construction_year+self.pre_dev_period+self.construction_period
        range_of_operating_years = list(range(int(years_of_operation),int(years_of_operation+self.operating_period)))
        carbon_taxation_years = carbon_cost_gbp[carbon_cost_gbp.year.isin(range_of_operating_years)]
        print("carbon_cost_gbp {}".format(carbon_cost_gbp))
        print("range ofoperation years {}".format(range_of_operating_years))
        print("Carbon taxation years {}".format(carbon_taxation_years))
        carbon_costs = [carbon_tax * carb_emit for carbon_tax, carb_emit in zip(carbon_taxation_years.price, carbon_emitted)]

        return carbon_costs

    def carbon_cost_total(self, carbon_costs):
        """
        Calculates the total cost of carbon over the lifetime of the power plant.
        :return: total carbon costs
        """
        carbon_costs_total = sum(carbon_costs)

        return carbon_costs_total



    def __repr__(self):
        return 'PowerPlant({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})'.format(self.name, self.type, self.capacity_mw, self.construction_year, self.average_load_factor, self.pre_dev_period, self.construction_period, self.operating_period, self.pre_dev_spend_years, self.construction_spend_years, self.pre_dev_cost_per_mw, self.construction_cost_per_mw, self._infrastructure, self.fixed_o_and_m_per_mw, self.variable_o_and_m_per_mwh, self.insurance_cost_per_mw, self.connection_cost_per_mw)


