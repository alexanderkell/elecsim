from itertools import chain

import pandas as pd
import logging

logger = logging.getLogger(__name__)

from src.plants.fuel.capacity_factor.capacity_factor_calculations import get_capacity_factor
from src.agents.generation_company.gen_co import GenCo
from src.role.market.world_plant_capacity import WorldPlantCapacity



"""power_exchange.py: Functionality to run power exchange"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"


class PowerExchange:
    def __init__(self, model):
        """
        Power exchange agent which contains functionality to tender and respond to bids.
        :param model: Model in which the agents are contained in.
        """
        self.model = model
        self.hold_duration_curve_prices = []
        self.load_duration_curve_prices = pd.DataFrame(columns = ["year", "segment_hour", "segment_demand", "accepted_price"])

    def tender_bids(self, segment_hours, segment_demand):
        """
        Function which iterates through the generator companies, requests their bids, orders them in order of price,
        and accepts bids.
        :param agents: All agents from simulation model.
        :param segment_hours: Value for number of hours particular electricity generation is required.
        :param segment_demand: Size of electricity consumption required.
        :return: None
        """
        agent = self.model.schedule.agents
        generator_companies = [x for x in agent if isinstance(x, GenCo)]  # Select of generation company agents

        self.adjust_load_duration_curve_for_renewables()

        for segment_hour, segment_demand in zip(segment_hours, segment_demand):
            bids = []
            for generation_company in generator_companies:
                bids.append(generation_company.calculate_bids(segment_hour, segment_demand))
            sorted_bids = self._sort_bids(bids)
            accepted_bids = self._respond_to_bids(sorted_bids, segment_hour, segment_demand)

            logger.debug("segment hour: {}".format(segment_hour))
            self._accept_bids(accepted_bids)
            # highest_bid = accepted_bids[-1].price_per_mwh
            highest_bid = max(bid.price_per_mwh for bid in accepted_bids)

            self._create_load_duration_price_curve(segment_hour, segment_demand, highest_bid)

        self.load_duration_curve_prices = pd.DataFrame(self.hold_duration_curve_prices)

    def adjust_load_duration_curve_for_renewables(self):
        """
        Function which adjusts the load duration curve
        :return:
        """
        onshore_plants = WorldPlantCapacity(self.model).get_renewable_by_type("Onshore")
        total_onshore_capacity = [sum(onshore_plant.capacity_mw for onshore_plant in onshore_plants)]
        onshore_capacity_factor = [get_capacity_factor("Onshore", hour) for hour in self.model.demand.segment_hours]


        offshore_plants = WorldPlantCapacity(self.model).get_renewable_by_type("Offshore")
        total_offshore_capacity = [sum(offshore_plant.capacity_mw for offshore_plant in offshore_plants)]
        offshore_capacity_factor = [get_capacity_factor("Offshore", hour) for hour in self.model.demand.segment_hours]


        pv_plants = WorldPlantCapacity(self.model).get_renewable_by_type("PV")
        total_pv_capacity = [sum(pv_plant.capacity_mw for pv_plant in pv_plants)]
        pv_capacity_factor = [get_capacity_factor("PV", hour) for hour in self.model.demand.segment_hours]


        self.model.demand.segment_consumption = [segment_consumption * onshore_capacity * onshore_capacity_factor for segment_consumption, onshore_capacity, onshore_capacity_factor in zip(self.model.demand.segment_consumption, total_onshore_capacity, onshore_capacity_factor)]
        self.model.demand.segment_consumption = [segment_consumption * onshore_capacity * onshore_capacity_factor for segment_consumption, onshore_capacity, onshore_capacity_factor in zip(self.model.demand.segment_consumption, total_offshore_capacity, offshore_capacity_factor)]
        self.model.demand.segment_consumption = [segment_consumption * onshore_capacity * onshore_capacity_factor for segment_consumption, onshore_capacity, onshore_capacity_factor in zip(self.model.demand.segment_consumption, total_pv_capacity, pv_capacity_factor)]



    def _create_load_duration_price_curve(self, segment_hour, segment_demand, accepted_price):
        segment_price_data = {
                'year': self.model.year_number,
                'segment_hour': segment_hour,
                'segment_demand': segment_demand,
                'accepted_price': accepted_price
            }

        self.hold_duration_curve_prices.append(segment_price_data)


    @staticmethod
    def _accept_bids(accepted_bids):
        # highest_accepted_bid = accepted_bids[-1].price_per_mwh
        highest_accepted_bid = max(bid.price_per_mwh for bid in accepted_bids)
        logger.info("Highest accepted bid price: {}".format(highest_accepted_bid))
        for bids in accepted_bids:

            # logger.debug("bid price: {}, plant name: {}, plant capacity: {}".format(bids.price_per_mwh, bids.plant.name, bids.plant.capacity_mw))
            bids.price_per_mwh = highest_accepted_bid

    @staticmethod
    def _sort_bids(bids):
        """
        Sorts bids in order of price
        :param bids: Bid objects
        :return: Return bids in order of price
        """
        bids = list(chain.from_iterable(bids))
        sorted_bids = sorted(bids, key=lambda x: x.price_per_mwh)
        return sorted_bids

    @staticmethod
    def _respond_to_bids(bids, segement_hour, capacity_required):
        """
        Response to bids based upon price and capacity required. Accepts bids in order of cheapest generator.
        Continues to accept bids until capacity is met for those hours.
        :param bids: Bid objects.
        :param capacity_required: Capacity required for this segment.
        :return: Returns a list of bids which have been accepted.
        """
        accepted_bids = []

        for bid in bids:
            # logger.debug('bid: price: {}'.format(bid.price_per_mwh))
            if capacity_required > 0 and capacity_required > bid.capacity_bid:
                bid.accept_bid(segement_hour)
                capacity_required -= bid.capacity_bid
                accepted_bids.append(bid)
                logger.debug('bid ACCEPTED: price: {}, capacity required: {}, capacity: {}, type: {}, name {}'.format(bid.price_per_mwh, capacity_required, bid.plant.capacity_mw, bid.plant.plant_type,  bid.plant.name))
            elif bid.capacity_bid > capacity_required > 0:
                bid.partially_accept_bid(segement_hour, capacity_required)
                capacity_required = 0
                accepted_bids.append(bid)
                logger.debug('bid PARTIALLY accepted: price: {}, capacity required: {}, capacity: {}, type: {}, name {}'.format(bid.price_per_mwh, capacity_required, bid.plant.capacity_mw, bid.plant.plant_type,  bid.plant.name))
            else:
                bid.reject_bid(segment_hour=segement_hour)
                logger.debug('bid REJECTED: price: {}, capacity required: {}, capacity: {}, type: {}, name {}'.format(bid.price_per_mwh, capacity_required, bid.plant.capacity_mw, bid.plant.plant_type,  bid.plant.name))



        return accepted_bids
