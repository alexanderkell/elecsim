import logging
from itertools import chain

import pandas as pd

from elecsim.market.electricity.bid import Bid
import elecsim.scenario.scenario_data

logger = logging.getLogger(__name__)



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
        self.price_duration_curve = pd.DataFrame(columns = ["year", "segment_hour", "segment_demand", "accepted_price"])

    def tender_bids(self, segment_hours, segment_demand, predict=False):
        """
        Function which iterates through the generator companies, requests their bids, orders them in order of price,
        and accepts bids.
        :param agents: All agents from simulation model.
        :param segment_hours: Value for number of hours particular electricity generation is required.
        :param segment_demand: Size of electricity consumption required.
        :param predict: Boolean that states whether the bids being tendered are for predicting price duration curve or whether it is for real bids.
        :return: None
        """
        agent = self.model.schedule.agents
        # generator_companies = [x for x in agent if isinstance(x, GenCo)]  # Selection of generation company agents
        generator_companies = [x for x in agent if hasattr(x, 'plants')]  # Selection of generation company agents

        # self.adjust_load_duration_curve_for_renewables()
        for segment_hour, segment_demand in zip(segment_hours, segment_demand):
            bids = []
            for generation_company in generator_companies:
                bids.append(generation_company.calculate_bids(segment_hour, predict))
            sorted_bids = self._sort_bids(bids)
            accepted_bids = self._respond_to_bids(sorted_bids, segment_hour, segment_demand)

            logger.debug("segment hour: {}".format(segment_hour))
            self._accept_bids(accepted_bids)
            highest_bid = max(bid.price_per_mwh for bid in accepted_bids)

            self._create_load_duration_price_curve(segment_hour, segment_demand, highest_bid)

        self.price_duration_curve = pd.DataFrame(self.hold_duration_curve_prices)
        if predict:
            logger.debug("predicted self.price_duration_curve: {}".format(self.price_duration_curve))
        else:
            logger.info("actual self.price_duration_curve: {}".format(self.price_duration_curve))

        return self.price_duration_curve[self.price_duration_curve.year == self.model.year_number].accepted_price.mean()

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

    def _respond_to_bids(self, bids, segment_hour, capacity_required):
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
                bid.accept_bid(segment_hour)
                capacity_required -= bid.capacity_bid
                accepted_bids.append(bid)
                bid.plant.accepted_bids.append(bid)
                logger.debug('bid ACCEPTED: price: {}, year: {}, capacity required: {}, capacity: {}, capacity_bid: {}, type: {}, name {}'.format(bid.price_per_mwh, bid.plant.construction_year, capacity_required, bid.plant.capacity_mw, bid.capacity_bid, bid.plant.plant_type,  bid.plant.name))
            elif bid.capacity_bid > capacity_required > 0:
                bid.partially_accept_bid(segment_hour, capacity_required)
                capacity_required = 0
                accepted_bids.append(bid)
                bid.plant.accepted_bids.append(bid)
                logger.debug('bid PARTIALLY ACCEPTED: price: {}, year: {}, capacity required: {}, capacity: {}, capacity_bid: {}, type: {}, name {}'.format(bid.price_per_mwh, bid.plant.construction_year, capacity_required, bid.plant.capacity_mw, bid.capacity_bid, bid.plant.plant_type,  bid.plant.name))
            else:
                bid.reject_bid(segment_hour=segment_hour)
                logger.debug('bid REJECTED: price: {}, year: {}, capacity required: {}, capacity: {}, capacity_bid: {}, type: {}, name {}'.format(bid.price_per_mwh, bid.plant.construction_year, capacity_required, bid.plant.capacity_mw, bid.capacity_bid, bid.plant.plant_type,  bid.plant.name))
        if capacity_required > 0:
            accepted_bids.append(Bid(None, None, segment_hour, 0, elecsim.scenario.scenario_data.lost_load, self.model.year_number))
        return accepted_bids

