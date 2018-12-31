import logging

from mesa import Agent

from src.market.electricity.bid import Bid
from src.plants.fuel.capacity_factor.capacity_factor_calculations import get_capacity_factor
from src.role.investment.calculate_npv import CalculateNPV
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
        :param name
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
        self.dismantle_old_plants()
        self.operate_constructed_plants()
        self.invest()
        self.reset_contracts()

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
            no_fuel_required=False
            if plant.plant_type in ['Offshore', 'Onshore', 'PV']:
                no_fuel_required = True
            if plant.min_running <= segment_hour and plant.capacity_fulfilled < plant.capacity_mw:
                price = plant.short_run_marginal_cost(self.model)
                marked_up_price = price*1.1
                if no_fuel_required:
                    # capacity_calculator = CapacityFactorCalculations(plant.plant_type)
                    logger.debug("segment value: {}".format(segment_demand))
                    capacity_factor = get_capacity_factor(plant.plant_type, segment_hour)
                    bids.append(Bid(self, plant, segment_hour, capacity_factor*(plant.capacity_mw-plant.capacity_fulfilled), marked_up_price))
                else:
                    bids.append(Bid(self, plant, segment_hour, plant.capacity_mw-plant.capacity_fulfilled, marked_up_price))

        return bids

    # def purchase_fuel(self):

    def invest(self):

        self.model

        CalculateNPV(self.discount_rate, self.model.year_number, 70)

    def dismantle_old_plants(self):
        """
        Remove plants that are past their lifetime agent from plant list
        """
        def get_running_plants(plants):
            for plant in plants:
                if plant.construction_year + plant.operating_period + plant.construction_period + plant.pre_dev_period >= self.model.year_number:
                    logger.info("Taking the plant '{}' out of service, year of construction: {}".format(plant.name, plant.construction_year))
                    yield plant
                else:
                    continue

        plants_filtered = list(get_running_plants(self.plants))
        self.plants = plants_filtered

    def operate_constructed_plants(self):
        for plant in self.plants:
            if plant.is_operating is False and self.model.year_number >= plant.construction_year + plant.construction_period + plant.pre_dev_period:
                plant.is_operating = True

    def reset_contracts(self):
        """
        Function to reset the contracts of all plants
        :return: None
        """
        for i in range(len(self.plants)):
            self.plants[i].reset_plant_contract()

