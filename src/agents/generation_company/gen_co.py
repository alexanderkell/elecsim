import logging

from mesa import Agent

from src.plants.plant_type.non_fuel_plant import NonFuelPlant
from src.plants.plant_type.fuel_plant import FuelPlant
# import src.plants.plant_type.fuel_plant
from src.market.electricity.bid import Bid
from src.plants.fuel.capacity_factor.capacity_factor_calculations import get_capacity_factor
from src.role.investment.expected_load_duration_prices import LoadDurationPrices
from src.role.market.latest_market_data import LatestMarketData
from src.role.plants.costs.fuel_plant_cost_calculations import FuelPlantCostCalculations
from src.plants.plant_costs.estimate_costs.estimate_costs import create_power_plant
from src.role.investment.calculate_npv import CalculateNPV, get_most_profitable_plants_by_npv
from inspect import signature
from src.role.market.latest_market_data import LatestMarketData
from src.role.investment.predict_load_duration_prices import PredictPriceDurationCurve

from src.data_manipulation.data_modifications.inverse_transform_sampling import sample_from_custom_distribution


from src.scenario.scenario_data import bid_mark_up, non_fuel_plant_availability, fuel_plant_availability
from random import gauss


logger = logging.getLogger(__name__)

"""gen_co.py: Agent which represents a generation company"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"


class GenCo(Agent):
    def __init__(self, unique_id, model, name, difference_in_discount_rate, look_back_period, plants=None, money=5000000):
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
        logger.info("Stepping generation company: {}".format(self.name))
        # self.dismantle_old_plants()
        self.operate_constructed_plants()
        # self.collect_money()
        self.invest()
        self.reset_contracts()
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
            if predict is True:
                if isinstance(plant, FuelPlant):
                    co2_price_predicted = self.forecast_attribute_price("co2")
                    fuel_price_predicted = self.forecast_attribute_price(plant.fuel.fuel_type)
                    price = plant.short_run_marginal_cost(self.model, self, fuel_price_predicted, co2_price_predicted)
                else:
                    price = plant.short_run_marginal_cost(self.model, self)
            else:
                price = plant.short_run_marginal_cost(self.model, self)
            marked_up_price = price * bid_mark_up



            if plant.plant_type in ['Offshore', 'Onshore', 'PV']:
                capacity_factor = get_capacity_factor(plant.plant_type, segment_hour)
                bids.append(
                    Bid(self, plant, segment_hour, capacity_factor * non_fuel_plant_availability * plant.capacity_mw, marked_up_price)
                )
            elif isinstance(plant, FuelPlant):
                if plant.capacity_fulfilled[segment_hour] < plant.capacity_mw:
                    # capacity_to_bid = fuel_plant_availability * (plant.capacity_mw - plant.capacity_fulfilled[segment_hour])
                    capacity_to_bid = fuel_plant_availability * plant.capacity_mw
                    bids.append(
                        Bid(self, plant, segment_hour, capacity_to_bid, marked_up_price)
                    )
            else:
                    bids.append(
                        # Bid(self, plant, segment_hour, non_fuel_plant_availability * (plant.capacity_mw - plant.capacity_fulfilled[segment_hour]), marked_up_price)
                        Bid(self, plant, segment_hour, non_fuel_plant_availability * plant.capacity_mw, marked_up_price)

                    )


            #
            # if isinstance(plant, FuelPlant):
            #     if plant.capacity_fulfilled[segment_hour] < plant.capacity_mw:
            #         bids.append(
            #             Bid(self, plant, segment_hour, fuel_plant_availability * (plant.capacity_mw - plant.capacity_fulfilled[segment_hour]), marked_up_price)
            #         )
            # elif plant.plant_type in ['Offshore', 'Onshore', 'PV']:
            #     capacity_factor = get_capacity_factor(plant.plant_type, segment_hour)
            #     bids.append(
            #         Bid(self, plant, segment_hour, capacity_factor * non_fuel_plant_availability * (plant.capacity_mw - plant.capacity_fulfilled[segment_hour]), marked_up_price)
            #     )
        return bids

    def invest(self):
        UPFRONT_INVESTMENT_COSTS = 0.25
        total_upfront_cost = 0
        logger.info("Investing")
        # while self.money > total_upfront_cost:
        logger.debug("self.money: {}, total_upfront_cost: {}".format(self.money, total_upfront_cost))
        # potential_plant_data = npv_calculation.get_affordable_plant_generator()
        potential_plant_data = get_most_profitable_plants_by_npv(self.model, self.difference_in_discount_rate, self.look_back_period)


        for plant_data in potential_plant_data:
            power_plant_trial = create_power_plant("plant", self.model.year_number, plant_data[1], plant_data[0])
            total_upfront_cost = power_plant_trial.get_upfront_costs()*UPFRONT_INVESTMENT_COSTS

            if self.money > total_upfront_cost:
                self.plants.append(power_plant_trial)
                self.money -= total_upfront_cost
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
                    logger.info("Taking the plant '{}' out of service, year of construction: {}".format(plant.name,
                                                                                                        plant.construction_year))
                    continue

        plants_filtered = list(get_running_plants(self.plants))
        self.plants = plants_filtered

    def operate_constructed_plants(self):
        for plant in self.plants:
            if plant.is_operating is False and self.model.year_number >= plant.construction_year + plant.construction_period + plant.pre_dev_period:
                plant.is_operating = True

    def pay_money(self):
        # self.money -=
        # fixed_costs = sum(plant for plant in self.plants)
        # expenditure = sum(bid for plant in self.plants for bid in plant.bids)

        for plant in self.plants:
            pass

    def collect_money(self):
        income = sum((bid.price_per_mwh * bid.segment_hours) for plant in self.plants for bid in plant.bids if
                     bid.partly_accepted or bid.bid_accepted)
        self.money += income

    def reset_contracts(self):
        """
        Function to reset the contracts of all plants
        :return: None
        """
        for plant in self.plants:
            plant.reset_plant_contract()

    def purchase_fuel(self):
        if any(plant.plant_type=="CCGT" for plant in self.plants):
            self.purchase_gas()
        if any(plant.plant_type=="Coal" for plant in self.plants):
            self.purchase_coal()

    def purchase_gas(self):
        self.gas_price_modifier = gauss(mu=0, sigma=0.9678)
        # self.gas_price_modifier = sample_from_custom_distribution([2,  1,  1,  0,  0,  4, 10,  7, 13, 13,  8,  6,  1,  2,  1,  1,  0,
        #  0,  0,  1], [[-2.67136237, -2.36374281, -2.05612326, -1.7485037 , -1.44088415,
        # -1.13326459, -0.82564504, -0.51802548, -0.21040593,  0.09721363,
        #  0.40483318,  0.71245274,  1.0200723 ,  1.32769185,  1.63531141,
        #  1.94293096,  2.25055052,  2.55817007,  2.86578963,  3.17340918,
        #  3.48102874]], 1)

        # division = [-2.67136237, -2.36374281, -2.05612326, -1.7485037 , -1.44088415,
        # -1.13326459, -0.82564504, -0.51802548, -0.21040593,  0.09721363,
        #  0.40483318,  0.71245274,  1.0200723 ,  1.32769185,  1.63531141,
        #  1.94293096,  2.25055052,  2.55817007,  2.86578963,  3.17340918,
        #  3.48102874]
        # count = [2,  1,  1,  0,  0,  4, 10,  7, 13, 13,  8,  6,  1,  2,  1,  1,  0,
        #  0,  0,  1]
        # self.gas_price_modifier = sample_from_custom_distribution(count, division, 1)

    def purchase_coal(self):
        self.coal_price_modifier = gauss(mu=0, sigma=0.9678)


    def forecast_demand_change(self):
        latest_market_data = LatestMarketData(self.model)
        demand_change_predicted = latest_market_data.agent_forecast_value("demand", self.look_back_period)
        return demand_change_predicted

    def forecast_attribute_price(self, fuel_type):
        latest_market_data = LatestMarketData(self.model)
        uranium_price_predicted = latest_market_data.agent_forecast_value(fuel_type, self.look_back_period)
        return uranium_price_predicted

