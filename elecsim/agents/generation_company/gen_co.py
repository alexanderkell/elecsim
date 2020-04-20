import logging
import math
from random import gauss
import numpy as np
from functools import lru_cache
from mesa import Agent
# from linetimer import CodeTimer

from elecsim.market.electricity.bid import Bid
from elecsim.plants.availability_factors.availability_factor_calculations import get_availability_factor
from elecsim.plants.fuel.capacity_factor.capacity_factor_calculations import get_capacity_factor
from elecsim.plants.plant_costs.estimate_costs.estimate_costs import create_power_plant, create_power_plant_group
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
        if elecsim.scenario.scenario_data.investment_mechanism != "RL" and self.model.step_number % self.model.market_time_splices == 0 and self.model.step_number != 0 and self.model.continue_investing < 3 and self.model.over_invested == False:
            continue_investing, over_invested = self.invest()
            if over_invested:
                self.model.over_invested = True
            if continue_investing == 1:
                self.model.continue_investing += continue_investing
                logger.debug(self.model.continue_investing)
            else:
                self.model.continue_investing = 0


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
            bid = self.create_bid(plant, predict, segment_hour, self.model.step_number)
            if bid:
                bids.append(bid)
        return bids

    @lru_cache(100000)
    def create_bid(self, plant, predict, segment_hour, step_number):
        future_plant_operating = False
        if predict is True:
            YEARS_IN_FUTURE_TO_PREDICT_SUPPLY = elecsim.scenario.scenario_data.years_for_agents_to_predict_forward
            future_plant_operating = plant.check_if_operating_in_certain_year(self.model.year_number, YEARS_IN_FUTURE_TO_PREDICT_SUPPLY)

            if isinstance(plant, FuelPlant):
                if future_plant_operating:
                    price = self._get_predicted_short_run_marginal_cost(plant)
                else:
                #     price = plant.short_run_marginal_cost(self.model, self)
                    return None
            else:
                price = plant.short_run_marginal_cost(self.model, self)
        else:
            price = plant.short_run_marginal_cost(self.model, self)
        marked_up_price = price * elecsim.scenario.scenario_data.bid_mark_up
        if plant.is_operating or future_plant_operating:
            if plant.plant_type in ['Offshore', 'Onshore', 'PV', 'Hydro', "Nuclear"]:
                capacity_factor, availability = _create_bid_for_capacity_factor_available_plants(
                    self.model.market_time_splices, plant, segment_hour)
                # logger.info(_create_bid_for_capacity_factor_available_plants.cache_info())
                return Bid(self, plant, segment_hour, capacity_factor * availability * plant.capacity_mw, marked_up_price,
                        self.model.year_number)
            elif isinstance(plant, FuelPlant):
                if plant.capacity_fulfilled[segment_hour] < plant.capacity_mw:
                    return self._create_bid_for_fuel_plant(marked_up_price, plant, segment_hour)
            elif plant.plant_type != 'Hydro_Store':
                return Bid(self, plant, segment_hour,
                        elecsim.scenario.scenario_data.non_fuel_plant_availability * plant.capacity_mw, marked_up_price,
                        self.model.year_number)

    def _create_bid_for_fuel_plant(self, marked_up_price, plant, segment_hour):
        availability_factor = get_availability_factor(plant_type=plant.plant_type,
                                                      construction_year=plant.construction_year)
        capacity_to_bid = availability_factor * plant.capacity_mw
        # logger.info("plant_type: {}, construction_year: {}, capacity_to_bid: {}, plant capacity: {}, availability factor: {}".format(plant.plant_type, plant.construction_year, capacity_to_bid, plant.capacity_mw, availability_factor))
        return Bid(self, plant, segment_hour, capacity_to_bid, marked_up_price, self.model.year_number)


    def _get_predicted_short_run_marginal_cost(self, plant):
        co2_price_predicted = self.forecast_attribute_price("co2")
        fuel_price_predicted = self.forecast_attribute_price(plant.fuel.fuel_type)
        price = plant.short_run_marginal_cost(self.model, self, fuel_price_predicted, co2_price_predicted)
        return price

    def invest(self):

        # capacity_of_invested_plants = 0
        lowest_upfront_cost = 0
        down_payment = 0
        counter = 0
        total_capacity = 0
        number_of_plants_to_purchase = 1
        # while self.money > lowest_upfront_cost and total_capacity < 1500:
        while self.money > lowest_upfront_cost:
        # while number_of_plants_to_purchase > 0:



            # counter += 1
            # if counter>3:
            #     break
            # potential_plant_data = npv_calculation.get_positive_npv_plants_list()
            potential_plant_data = get_most_profitable_plants_by_npv(self.model, self.difference_in_discount_rate,
                                                                 self.look_back_period)

            # logger.info("potential_plant_data: {}".format(potential_plant_data))
            if potential_plant_data:
                potential_plant_list = []
                for plant_data in potential_plant_data:
                    power_plant_trial = create_power_plant("invested_plant", self.model.year_number, plant_data[1], plant_data[0])
                    potential_plant_list.append(power_plant_trial)
                lowest_upfront_cost = min(plant.get_upfront_costs() * elecsim.scenario.scenario_data.upfront_investment_costs for plant in potential_plant_list)
            else:
                return 1, False

            for plant_data in potential_plant_list:

                # power_plant_trial = create_power_plant("invested_plant", self.model.year_number, plant_data[1], plant_data[0])
                power_plant_trial = create_power_plant("invested_plant", self.model.year_number, plant_data.plant_type, plant_data.capacity_mw)
                down_payment = power_plant_trial.get_upfront_costs() * elecsim.scenario.scenario_data.upfront_investment_costs
                number_of_plants_to_purchase = int(self.money/down_payment)
                if number_of_plants_to_purchase == 0:
                    continue

                capacity_to_purchase = number_of_plants_to_purchase * power_plant_trial.capacity_mw
                if capacity_to_purchase > 20000:
                    number_of_plants_to_purchase = int(20000/power_plant_trial.capacity_mw)

                power_plant_trial_group = create_power_plant_group(name="invested_plant_group", start_date=self.model.year_number, simplified_type=plant_data.plant_type, capacity=plant_data.capacity_mw, number_of_plants_to_purchase=number_of_plants_to_purchase)
                down_payment_of_plant_array = number_of_plants_to_purchase*down_payment
                # logger.info(create_power_plant.cache_info())
                if self.money > down_payment_of_plant_array and number_of_plants_to_purchase >= 1:
                    logger.debug("investing in {}, company: {}, size: {}, number: {}, self.money: {}".format(power_plant_trial_group.plant_type, self.name, power_plant_trial_group.capacity_mw, number_of_plants_to_purchase, self.money))
                    self.plants.append(power_plant_trial_group)
                    self.money -= down_payment_of_plant_array
                    total_capacity += power_plant_trial_group.capacity_mw
                    if total_capacity > 400000:  # 20000000:
                        return 1, True
                    break
        else:
            return 0, False

    def invest_RL(self, action):
        plant_list = elecsim.scenario.scenario_data.potential_plants_to_invest
        print("action: {}".format(action))
        # plant_string_to_invest = plant_list[action.item(0)]
        multiplier_of_100mw = 1
        # action = action - 1
        if action >= len(plant_list):
            multiplier_of_100mw = action//len(plant_list)
            action = action % len(plant_list)



        # print("len(plant_list): {}".format(len(plant_list)))
        # print("number_of_plants: {}".format(number_of_plants))
        # print("action: {}".format(action))

        plant_string_to_invest = plant_list[action]
        plant = elecsim.scenario.scenario_data.modern_plant_costs[elecsim.scenario.scenario_data.modern_plant_costs.Plant_Type.str.contains(plant_string_to_invest)]

        number_of_plants_needed = (multiplier_of_100mw*100)/(plant.Plant_Size.values[0])

        print("number_of_plants_needed: {}".format(number_of_plants_needed))
        print("MW required: {}".format(multiplier_of_100mw*100))
        print("plant.Plant_Size.values[0]: {}".format(plant.Plant_Size.values[0]))

        # For multi discrete action type
        # plant_group = create_power_plant_group("plant_RL_invested", self.model.year_number, plant.Type.values[0], plant.Plant_Size.values[0], action.item(1))
        # For discrete action type
        plant_group = create_power_plant_group("plant_RL_invested", self.model.year_number, plant.Type.values[0], plant.Plant_Size.values[0], number_of_plants_needed)

        self.plants.append(plant_group)


    def dismantle_old_plants(self):
        """
        Remove plants that are past their lifetime agent from plant list
        """

        def get_running_plants(plants):
            for plant in plants:
                if plant.construction_year + plant.operating_period + plant.construction_period + plant.pre_dev_period >= self.model.year_number:
                    yield plant
                else:
                    logger.debug("Taking the plant '{}' out of service, year of construction: {}".format(plant.name, plant.construction_year))
                    for bid in self.model.PowerExchange.stored_ordered_bids:
                        if bid.plant == plant:
                            del bid

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
        # income = sum((bid.price_per_mwh * bid.segment_hours) for plant in self.plants for bid in plant.accepted_bids if
        #              bid.partly_accepted or bid.bid_accepted)
        #
        # short_run_marginal_expenditure = sum((bid.segment_hours * bid.capacity_bid * plant.short_run_marginal_cost(model=self.model, genco=self)
        #                                       for plant in self.plants for bid in plant.accepted_bids if bid.partly_accepted or bid.bid_accepted if plant.is_operating == True))
        net_income = 0
        income = 0
        short_run_marginal_expenditure = 0
        for plant in self.plants:
            previous_segment_hour = 0
            if self.model.market_time_splices == 1:
                bids_ordered = reversed(plant.accepted_bids)
            else:
                bids_ordered = plant.accepted_bids
            for bid in bids_ordered:
                if bid.partly_accepted or bid.bid_accepted:
                    income += bid.price_per_mwh * (bid.segment_hours - previous_segment_hour) * bid.capacity_bid
                    if plant.is_operating:
                        srmc = plant.short_run_marginal_cost(model=self.model, genco=self)
                        short_run_marginal_expenditure += (bid.segment_hours - previous_segment_hour) * bid.capacity_bid * srmc
                previous_segment_hour = bid.segment_hours

            percentage_of_time_of_year = self.model.demand.segment_hours[-1]/8760
            logger.debug("percentage_of_time_of_year: {}".format(percentage_of_time_of_year))

            interest = [elecsim.scenario.scenario_data.nuclear_wacc if plant.plant_type == "Nuclear" else elecsim.scenario.scenario_data.non_nuclear_wacc for plant in self.plants]

            fixed_variable_costs = sum((plant.fixed_o_and_m_per_mw * plant.capacity_mw) for plant in self.plants if plant.is_operating is True)

            capital_loan_expenditure = sum(select_yearly_payback_payment_for_year(plant, interest_rate + self.difference_in_discount_rate, elecsim.scenario.scenario_data.upfront_investment_costs, self.model) for plant, interest_rate in zip(self.plants, interest))

            cashflow = income - short_run_marginal_expenditure*percentage_of_time_of_year - fixed_variable_costs*percentage_of_time_of_year + capital_loan_expenditure*percentage_of_time_of_year
            net_income += cashflow
        # logger.debug("income: {}, outflow: {}".format(income, short_run_marginal_expenditure/percentage_of_time_of_year - fixed_variable_costs/percentage_of_time_of_year + capital_loan_expenditure/percentage_of_time_of_year))
        logger.debug("cashflow: {} for {}".format(net_income, self.name))
        if not math.isnan(net_income):
            self.money += net_income

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


@lru_cache(64)
def get_renewable_availability(plant):
    if plant.plant_type == "Offshore":
        availability = elecsim.scenario.scenario_data.offshore_availability
    elif plant.plant_type == 'Onshore':
        availability = elecsim.scenario.scenario_data.onshore_availability
    elif plant.plant_type == "PV":
        availability = elecsim.scenario.scenario_data.pv_availability
    else:
        availability = elecsim.scenario.scenario_data.non_fuel_plant_availability
    return availability

@lru_cache(250000)
def _create_bid_for_capacity_factor_available_plants(market_time_splices, plant, segment_hour):
    capacity_factor = get_capacity_factor(market_time_splices, plant.plant_type, segment_hour)
    availability = get_renewable_availability(plant)
    return capacity_factor, availability
