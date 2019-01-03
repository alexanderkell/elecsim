import logging

from mesa import Agent

from src.plants.plant_type.fuel_plant import FuelPlant

from src.market.electricity.bid import Bid
from src.plants.fuel.capacity_factor.capacity_factor_calculations import get_capacity_factor
from src.role.investment.calculate_npv import CalculateNPV
from src.role.investment.expected_load_duration_prices import LoadDurationPrices
from src.role.market.latest_market_data import LatestMarketData

logger = logging.getLogger(__name__)

"""gen_co.py: Agent which represents a generation company"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"


class GenCo(Agent):
    def __init__(self, unique_id, model, name, discount_rate, plants=None, money=5000000):
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

        self.discount_rate = discount_rate

    def step(self):
        logger.debug("Stepping generation company: {}".format(self.name))
        # self.dismantle_old_plants()
        self.operate_constructed_plants()
        self.invest()
        self.reset_contracts()

    # def calculate_non_fuel_bids(self, segment_hour):
    #     bids = []
    #     renewable_plants = [renewable_plant for renewable_plant in self.plants if isinstance(renewable_plant, NonFuelPlant)]
    #     for plant in renewable_plants:
    #         marked_up_price = plant.short_run_marginal_cost(self.model)*1.1
    #         bids.append(Bid(self, plant, segment_hour, plant.capacity_mw, marked_up_price))
    #     return bids


    def calculate_bids(self, segment_hour, segment_demand):
        """
        Function to generate the bids for each of the power plants owned by the generating company.
        The bids submitted are the fixed costs divided by lifetime of plant plus yearly variable costs plus a 10% margin
        :param segment_hour: Number of hours in which the current segment is required
        :param segment_demand: Electricity consumption required for the specified number of hours
        :return: Bids returned for the available plants at the specified segment hour
        """

        bids = []

        for plant in self.plants:
            price = plant.short_run_marginal_cost(self.model)
            marked_up_price = price * 1.1
            if isinstance(plant, FuelPlant):
                if plant.capacity_fulfilled[segment_hour] < plant.capacity_mw:
                # if plant.min_running <= segment_hour and plant.capacity_fulfilled[segment_hour] < plant.capacity_mw:
                    bids.append(
                        Bid(self, plant, segment_hour, plant.capacity_mw - plant.capacity_fulfilled[segment_hour], marked_up_price)
                    )
            elif plant.plant_type in ['Offshore', 'Onshore', 'PV']:
                capacity_factor = get_capacity_factor(plant.plant_type, segment_hour)
                bids.append(
                    Bid(self, plant, segment_hour, capacity_factor * (plant.capacity_mw - plant.capacity_fulfilled[segment_hour]), marked_up_price)
                )

        return bids

    def invest(self):
        logger.debug("TESTING TESTING")
        # load_duration_prices = LoadDurationPrices(model=self.model)
        # load_duration_prices.get_load_curve_price_predictions(reference_year=self.model.year_number+1, look_back_years=5)
        #
        # logger.debug("Load duration prices: {}".format(load_duration_prices))

        # LOOK_BACK_YEARS = 4
        #
        # load_duration_price_predictor = LoadDurationPrices(model=self.model)
        # load_duration_prices = load_duration_price_predictor.get_load_curve_price_predictions(LOOK_BACK_YEARS,
        #                                                                                       self.model.year_number + 1)
        # CalculateNPV(self.model, self.discount_rate, self.model.year_number, 5, 70).get_expected_load_factor(load_duration_prices)


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

