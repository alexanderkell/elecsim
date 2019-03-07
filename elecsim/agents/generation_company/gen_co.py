import logging
import math
from random import gauss

from mesa import Agent

from elecsim.market.electricity.bid import Bid
from elecsim.plants.availability_factors.availability_factor_calculations import get_availability_factor
from elecsim.plants.fuel.capacity_factor.capacity_factor_calculations import get_capacity_factor
from elecsim.plants.plant_costs.estimate_costs.estimate_costs import create_power_plant
from elecsim.plants.plant_type.fuel_plant import FuelPlant
from elecsim.role.investment.calculate_npv import get_most_profitable_plants_by_npv
from elecsim.role.investment.calculate_npv import select_yearly_payback_payment_for_year
from elecsim.role.market.latest_market_data import LatestMarketData
# from elecsim.scen_error.scenario_data import bid_mark_up, pv_availability, offshore_availability, onshore_availability, non_fuel_plant_availability
# from elecsim.scen_error.scenario_data import nuclear_wacc, non_nuclear_wacc, upfront_investment_costs, years_for_agents_to_predict_forward

import elecsim.scenario.scenario_data

logger = logging.getLogger(__name__)

"""gen_co.py: Agent which represents a generation company"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"


class GenCo(Agent):
    def __init__(self, unique_id, model, name, difference_in_discount_rate, look_back_period, plants=None,
                 money=5000000):
        """
        Agent which defines a generating company
        :param unique_id: Unique ID for the generating company
        :param model:  Model which defines the world that the agent lives in
        :param name: Name of generating company
        :param plants: Plants which the generating company is initialised with
        :param money: Money which the agent is initialised with
        """
        super().__init__(unique_id, model)
        if plants is None:
            plants = []

        self.name = name
        self.plants = plants
        self.money = money

        self.difference_in_discount_rate = difference_in_discount_rate
        self.look_back_period = look_back_period

        self.gas_price_modifier = 0
        self.coal_price_modifier = 0

    def step(self):
        logger.debug("Stepping generation company: {}".format(self.name))
        logger.debug("Amount of money: {}".format(self.money))
        self.delete_old_bids()
        self.invest()
        # self.reset_contracts()
        self.purchase_fuel()

    # def calculate_non_fuel_bids(self, segment_hour):
    #     bids = []
    #     renewable_plants = [renewable_plant for renewable_plant in self.plants if isinstance(renewable_plant, NonFuelPlant)]
    #     for plant in renewable_plants:
    #         marked_up_price = plant.short_run_marginal_cost(self.model)*1.1
    #         bids.append(Bid(self, plant, segment_hour, plant.capacity_mw, marked_up_price))
    #     return bids


    def calculate_bids(self, segment_hour, predict=False):
        """
        Function to generate the bids for each of the power plants owned by the generating company.
        The bids submitted are the fixed costs divided by lifetime of plant plus yearly variable costs plus a 10% margin
        :param segment_hour: Number of hours in which the current segment is required
        :param segment_demand: Electricity consumption required for the specified number of hours
        :return: Bids returned for the available plants at the specified segment hour
        """

        bids = []

        for plant in self.plants:
            future_plant_operating = False
            if predict is True:
                if isinstance(plant, FuelPlant):
                    YEARS_IN_FUTURE_TO_PREDICT_SUPPLY = 7
                    future_plant_operating = plant.check_if_operating_in_certain_year(self.model.year_number, YEARS_IN_FUTURE_TO_PREDICT_SUPPLY)
                    if future_plant_operating:
                        co2_price_predicted = self.forecast_attribute_price("co2")
                        fuel_price_predicted = self.forecast_attribute_price(plant.fuel.fuel_type)
                        price = plant.short_run_marginal_cost(self.model, self, fuel_price_predicted, co2_price_predicted)
                    else:
                        # price = plant.short_run_marginal_cost(self.model, self)
                        continue
                else:
                    price = plant.short_run_marginal_cost(self.model, self)
            else:
                price = plant.short_run_marginal_cost(self.model, self)
            marked_up_price = price * elecsim.scenario.scenario_data.bid_mark_up
            if plant.is_operating or future_plant_operating:
                if plant.plant_type in ['Offshore', 'Onshore', 'PV', 'Hydro']:
                    capacity_factor = get_capacity_factor(plant.plant_type, segment_hour)

                    availability = self.get_renewable_availability(plant)

                    bids.append(
                        Bid(self, plant, segment_hour, capacity_factor * availability * plant.capacity_mw,
                            marked_up_price, self.model.year_number)
                    )
                elif isinstance(plant, FuelPlant):
                    if plant.capacity_fulfilled[segment_hour] < plant.capacity_mw:
                        availability_factor = get_availability_factor(plant_type=plant.plant_type, construction_year=plant.construction_year)
                        capacity_to_bid = availability_factor * plant.capacity_mw

                        # logger.info("plant_type: {}, construction_year: {}, capacity_to_bid: {}, plant capacity: {}, availability factor: {}".format(plant.plant_type, plant.construction_year, capacity_to_bid, plant.capacity_mw, availability_factor))
                        bids.append(
                            Bid(self, plant, segment_hour, capacity_to_bid, marked_up_price, self.model.year_number)
                        )
                elif plant.plant_type != 'Hydro_Store':
                    bids.append(
                        Bid(self, plant, segment_hour, elecsim.scenario.scenario_data.non_fuel_plant_availability * plant.capacity_mw, marked_up_price, self.model.year_number)

                    )
        return bids

    def get_renewable_availability(self, plant):
        if plant.plant_type == "Offshore":
            availability = elecsim.scenario.scenario_data.offshore_availability
        elif plant.plant_type == 'Onshore':
            availability = elecsim.scenario.scenario_data.onshore_availability
        elif plant.plant_type == "PV":
            availability = elecsim.scenario.scenario_data.pv_availability
        else:
            availability = elecsim.scenario.scenario_data.non_fuel_plant_availability
        return availability

    def invest(self):
        lowest_upfront_cost = 0
        down_payment = 0
        counter =0
        total_capacity = 0
        # while self.money > lowest_upfront_cost and total_capacity < 1500:
        while self.money > lowest_upfront_cost:

            counter += 1
            # if counter>3:
            #     break
            # potential_plant_data = npv_calculation.get_positive_npv_plants_list()
            potential_plant_data = get_most_profitable_plants_by_npv(self.model, self.difference_in_discount_rate,
                                                                     self.look_back_period)
            if potential_plant_data:
                potential_plant_list = []
                for plant_data in potential_plant_data:
                    power_plant_trial = create_power_plant("invested_plant", self.model.year_number, plant_data[1], plant_data[0])
                    potential_plant_list.append(power_plant_trial)
                    lowest_upfront_cost = min(plant.get_upfront_costs() * elecsim.scenario.scenario_data.upfront_investment_costs for plant in potential_plant_list)
            else:
                break

            for plant_data in potential_plant_data:
                power_plant_trial = create_power_plant("invested_plant", self.model.year_number, plant_data[1], plant_data[0])
                down_payment = power_plant_trial.get_upfront_costs() * elecsim.scenario.scenario_data.upfront_investment_costs
                if self.money > down_payment:
                    logger.debug("investing in {} self.money: {}, down_payment: {}".format(power_plant_trial.plant_type, self.money, down_payment))
                    self.plants.append(power_plant_trial)
                    self.money -= down_payment
                    total_capacity += power_plant_trial.capacity_mw
                    break


    def dismantle_old_plants(self):
        """
        Remove plants that are past their lifetime agent from plant list
        """

        def get_running_plants(plants):
            for plant in plants:
                if plant.construction_year + plant.operating_period + plant.construction_period + plant.pre_dev_period >= self.model.year_number:
                    yield plant
                else:
                    logger.debug("Taking the plant '{}' out of service, year of construction: {}".format(plant.name,
                                                                                                        plant.construction_year))
                    continue

        plants_filtered = list(get_running_plants(self.plants))
        self.plants = plants_filtered

    # def pay_money(self):
    #     # self.money -=
    #     # fixed_costs = sum(plant for plant in self.plants)
    #     # expenditure = sum(bid for plant in self.plants for bid in plant.bids)
    #
    #     for plant in self.plants:
    #         pass

    def settle_accounts(self):
        income = sum((bid.price_per_mwh * bid.segment_hours) for plant in self.plants for bid in plant.accepted_bids if
                     bid.partly_accepted or bid.bid_accepted)

        short_run_marginal_expenditure = sum((bid.segment_hours * bid.capacity_bid * plant.short_run_marginal_cost(model=self.model, genco=self)
                                              for plant in self.plants for bid in plant.accepted_bids if bid.partly_accepted or bid.bid_accepted if plant.is_operating==True))

        interest = [elecsim.scenario.scenario_data.nuclear_wacc if plant.plant_type == "Nuclear" else elecsim.scenario.scenario_data.non_nuclear_wacc for plant in self.plants]

        fixed_variable_costs = sum((plant.fixed_o_and_m_per_mw * plant.capacity_mw)*-1 for plant in self.plants if plant.is_operating==True)

        capital_loan_expenditure = sum(select_yearly_payback_payment_for_year(plant, interest_rate + self.difference_in_discount_rate, elecsim.scenario.scenario_data.upfront_investment_costs, self.model)*-1 for plant, interest_rate in zip(self.plants, interest))

        cashflow = income - short_run_marginal_expenditure - fixed_variable_costs - capital_loan_expenditure
        if not math.isnan(cashflow):
            self.money += cashflow

    # def reset_contracts(self):
    #     """
    #     Function to reset the contracts of all plants
    #     :return: None
    #     """
    #     for plant in self.plants:
    #         plant.reset_plant_contract()

    def delete_old_bids(self):
        for plant in self.plants:
            plant.delete_old_plant_bids()

    def purchase_fuel(self):
        if any(plant.plant_type == "CCGT" for plant in self.plants):
            self.purchase_gas()
        if any(plant.plant_type == "Coal" for plant in self.plants):
            self.purchase_coal()

    def purchase_gas(self):
        self.gas_price_modifier = gauss(mu=-0.010028, sigma=0.634514)

    def purchase_coal(self):
        self.coal_price_modifier = gauss(mu=-0.042884, sigma=3.400331)

    def forecast_demand_change(self):
        latest_market_data = LatestMarketData(self.model)
        demand_change_predicted = latest_market_data.agent_forecast_value("demand", self.look_back_period, elecsim.scenario.scenario_data.years_for_agents_to_predict_forward)
        return demand_change_predicted

    def forecast_attribute_price(self, fuel_type):
        latest_market_data = LatestMarketData(self.model)
        predicted_fuel_price = latest_market_data.agent_forecast_value(fuel_type, self.look_back_period, elecsim.scenario.scenario_data.years_for_agents_to_predict_forward)
        return predicted_fuel_price
