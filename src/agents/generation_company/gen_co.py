from mesa import Agent

from src.market.electricity.bid import Bid
from src.role.investment.calculate_npv import CalculateNPV
import logging
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
        self.invest()
        self.reset_contracts()

    def calculate_bids(self, segment_hour, segment_value):
        """
        Function to generate the bids for each of the power plants owned by the generating company.
        The bids submitted are the fixed costs divided by lifetime of plant plus yearly variable costs plus a 10% margin
        :param segment_hour: Number of hours in which the current segment is required
        :param segment_value: Electricity consumption required for the specified number of hours
        :return: Bids returned for the available plants at the specified segment hour
        """
        bids = []
        for plant in self.plants:
            if plant.min_running <= segment_hour and plant.capacity_fulfilled < plant.capacity_mw:
                # price = ((plant.down_payment/plant.lifetime + plant.ann_cost + plant.operating_cost)/(plant.capacity*segment_hour))*1.1
                # price = plant.calculate_lcoe(self.discount_rate)
                price = plant.short_run_marginal_cost()
                marked_up_price = price*1.1
                bids.append(Bid(self, plant, segment_hour, plant.capacity_mw-plant.capacity_fulfilled, marked_up_price))
        return bids

    # def purchase_fuel(self):

    def invest(self):
        CalculateNPV(self.discount_rate, self.model.year_number, 70)

    def reset_contracts(self):
        """
        Function to reset the contracts of all plants
        :return: None
        """
        for i in range(len(self.plants)):
            self.plants[i].reset_plant_contract()

