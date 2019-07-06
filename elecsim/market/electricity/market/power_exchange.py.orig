import logging
from functools import lru_cache
from itertools import chain
# from linetimer import CodeTimer
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
        self.price_duration_curve = pd.DataFrame(columns=["year", "segment_hour", "segment_demand", "accepted_price"])

        self.stored_bids = {}
        self.stored_ordered_bids = {}

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
<<<<<<< HEAD

        self.hold_duration_curve_prices = []

=======
>>>>>>> 5f3c373861c398621fed06ebb3fe989ceb1733a9
        agent = self.model.schedule.agents
        generator_companies = [x for x in agent if hasattr(x, 'plants')]  # Selection of generation company agents

        for gen_co in generator_companies:
            for plant in gen_co.plants:
                plant.capacity_fulfilled = dict.fromkeys(segment_hours, 0)

        for segment_hour, segment_demand in zip(segment_hours, segment_demand):
            bids = []

            for generation_company in generator_companies:
                bids.append(generation_company.calculate_bids(segment_hour, predict))
                # logger.info(generation_company.calculate_bids.cache_info())
<<<<<<< HEAD

            sorted_bids = self._sort_bids(bids)
            if predict is False:

                logger.info("bids len: {}".format(len(sorted_bids)))
                # logger.info("total capacity of bids: {}".format(sum(bid.capacity_bid for bid in sorted_bids)))


            accepted_bids = self._respond_to_bids(sorted_bids, segment_hour, segment_demand)



            logger.debug("segment hour: {}".format(segment_hour))
            highest_bid = self._accept_bids(accepted_bids)
            # highest_bid = max(bid.price_per_mwh for bid in accepted_bids)
=======
            sorted_bids = self._sort_bids(bids)
            accepted_bids = self._respond_to_bids(sorted_bids, segment_hour, segment_demand)

            logger.debug("segment hour: {}".format(segment_hour))
            self._accept_bids(accepted_bids)
            highest_bid = max(bid.price_per_mwh for bid in accepted_bids)
>>>>>>> 5f3c373861c398621fed06ebb3fe989ceb1733a9

            self._create_load_duration_price_curve(segment_hour, segment_demand, highest_bid)

        self.price_duration_curve = pd.DataFrame(self.hold_duration_curve_prices)
        if predict:
<<<<<<< HEAD
            self.price_duration_curve = self.price_duration_curve[(self.price_duration_curve.year == self.model.year_number) & (self.price_duration_curve.day == self.model.step_number)]
            logger.debug("predicted self.price_duration_curve: {}".format(self.price_duration_curve))
        else:
            self.price_duration_curve = self.price_duration_curve[(self.price_duration_curve.year == self.model.year_number) & (self.price_duration_curve.day == self.model.step_number)]
            logger.info("actual self.price_duration_curve: {}".format(self.price_duration_curve))
=======
            logger.debug("predicted self.price_duration_curve: {}".format(self.price_duration_curve))
        else:
            self.price_duration_curve = self.price_duration_curve[(self.price_duration_curve.year == self.model.year_number) & (self.price_duration_curve.day == self.model.step_number)]
            logger.debug("actual self.price_duration_curve: {}".format(self.price_duration_curve))
>>>>>>> 5f3c373861c398621fed06ebb3fe989ceb1733a9

        return self.price_duration_curve[self.price_duration_curve.year == self.model.year_number].accepted_price.mean()



    # def tender_bids(self, segment_hours, segment_demand, predict=False):
    #     """
    #     Function which iterates through the generator companies, requests their bids, orders them in order of price,
    #     and accepts bids.
    #     :param agents: All agents from simulation model.
    #     :param segment_hours: Value for number of hours particular electricity generation is required.
    #     :param segment_demand: Size of electricity consumption required.
    #     :param predict: Boolean that states whether the bids being tendered are for predicting price duration curve or whether it is for real bids.
    #     :return: None
    #     """
    #     agent = self.model.schedule.agents
    #     generator_companies = [x for x in agent if hasattr(x, 'plants')]  # Selection of generation company agents
    #
    #     if self.model.beginning_of_year:
    #         self.hold_duration_curve_prices = []
    #
    #
    #     save = dict.fromkeys(segment_hours, 0)
    #     for gen_co in generator_companies:
    #         for plant in gen_co.plants:
    #             # plant.capacity_fulfilled = dict.fromkeys(segment_hours, 0)
    #             plant.capacity_fulfilled = save.copy()
    #
    #     for segment_hour, segment_demand in zip(segment_hours, segment_demand):
    #         bids = []
    #
    #         if segment_hour not in self.stored_bids or predict is False:
    #             sorted_bids = self._calculate_all_bids(bids, generator_companies, predict, segment_hour)
    #             self.stored_bids[segment_hour] = sorted_bids
    #         else:
    #             sorted_bids = self.stored_bids[segment_hour]
    #             if self.model.last_added_plant:
    #                 # logger.info(self.model.last_added_plant_bids)
    #
    #                 sorted_bids.append(self.model.last_added_plant[segment_hour])
    #
    #         accepted_bids = self._respond_to_bids(sorted_bids, segment_hour, segment_demand)
    #
    #         self.stored_ordered_bids[segment_hour] = accepted_bids
    #
    #         logger.debug("segment hour: {}".format(segment_hour))
    #
    #         self._accept_bids(accepted_bids)
    #         highest_bid = max(bid.price_per_mwh for bid in self.stored_ordered_bids[segment_hour] if bid.bid_accepted is True)
    #         self._create_load_duration_price_curve(segment_hour, segment_demand, highest_bid)
    #
    #     self.price_duration_curve = pd.DataFrame(self.hold_duration_curve_prices)
    #     if predict:
    #         self.price_duration_curve = self.price_duration_curve[(self.price_duration_curve.year == self.model.year_number)]
    #         logger.debug("predicted self.price_duration_curve: {}".format(self.price_duration_curve))
    #     else:
    #         self.price_duration_curve = self.price_duration_curve[(self.price_duration_curve.year == self.model.year_number) & (self.price_duration_curve.day == self.model.step_number)]
    #         logger.info("actual self.price_duration_curve: {}".format(self.price_duration_curve))
    #
    #     return self.price_duration_curve[self.price_duration_curve.year == self.model.year_number].accepted_price.mean()

    def _calculate_all_bids(self, bids, generator_companies, predict, segment_hour):
        # for generation_company in generator_companies:
        #     bids.append(generation_company.calculate_bids(segment_hour, predict))

        bids = [generation_company.calculate_bids(segment_hour, predict) for generation_company in generator_companies]
            # logger.info(generation_company.calculate_bids.cache_info())
        sorted_bids = self._sort_bids(bids)
        return sorted_bids

    def _create_load_duration_price_curve(self, segment_hour, segment_demand, accepted_price):
        segment_price_data = {
                'year': self.model.year_number,
                'day': self.model.step_number,
                'segment_hour': segment_hour,
                'segment_demand': segment_demand,
                'accepted_price': accepted_price
            }

        self.hold_duration_curve_prices.append(segment_price_data)

    @staticmethod
    def _accept_bids(accepted_bids):
<<<<<<< HEAD
        highest_accepted_bid = accepted_bids[-1].price_per_mwh
        for bid in accepted_bids:
            # logger.debug("bid price: {}, plant name: {}, plant capacity: {}".format(bids.price_per_mwh, bids.plant.name, bids.plant.capacity_mw))
            bid.price_per_mwh = highest_accepted_bid
        return highest_accepted_bid
=======
        # highest_accepted_bid = accepted_bids[-1].price_per_mwh
        highest_accepted_bid = max(bid.price_bid for bid in accepted_bids)

        for bid in accepted_bids:
            # logger.debug("bid price: {}, plant name: {}, plant capacity: {}".format(bids.price_per_mwh, bids.plant.name, bids.plant.capacity_mw))
            bid.price_per_mwh = highest_accepted_bid
>>>>>>> 5f3c373861c398621fed06ebb3fe989ceb1733a9

    @staticmethod
    def _sort_bids(bids, attribute="price_per_mwh"):
        """
        Sorts bids in order of price
        :param bids: Bid objects
        :return: Return bids in order of price
        """
        bids = list(chain.from_iterable(bids))
        sorted_bids = sorted(bids, key=lambda x: getattr(x, attribute))
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



#     def _respond_to_bids(self, bids, segment_hour, capacity_required):
#         """
#         Response to bids based upon price and capacity required. Accepts bids in order of cheapest generator.
#         Continues to accept bids until capacity is met for those hours.
#         :param bids: Bid objects.
#         :param capacity_required: Capacity required for this segment.
#         :return: Returns a list of bids which have been accepted.
#         """
#
#         if segment_hour not in self.stored_ordered_bids:
#             accepted_bids = NoHistoryBidResponder(bids, capacity_required, segment_hour).get_accepted_bids()
#         elif self.model.last_added_plant_bids is None:
#             accepted_bids = self.stored_ordered_bids[segment_hour]
#         elif segment_hour in self.stored_ordered_bids:
#             accepted_bids = HistoryBidResponder(self.stored_ordered_bids[segment_hour], capacity_required, segment_hour).get_accepted_bids(new_bid=self.model.last_added_plant_bids[segment_hour])
#         else:
#             accepted_bids = NoHistoryBidResponder(bids, capacity_required, segment_hour).get_accepted_bids()
#
#         return accepted_bids
#
#
# class BidResponder:
#
#     def __init__(self, bids, capacity_required, segment_hour):
#         self.capacity_required = capacity_required
#         self.segment_hour = segment_hour
#         self.bids = bids
#
#
# class HistoryBidResponder(BidResponder):
#
#     def __init__(self, bids, capacity_required, segment_hour):
#         super().__init__(bids=bids, capacity_required=capacity_required, segment_hour=segment_hour)
#
#     def get_accepted_bids(self, new_bid):
#         # logger.info("accepted_price: {}".format(self.bids[0].price_per_mwh))
#         # logger.info("new_bid: {}".format(new_bid))
#
#         if new_bid.price_bid < self.bids[0].price_per_mwh:
#             capacity_undercut = new_bid.capacity_bid
#             while capacity_undercut > 0:
#                 self.bids = PowerExchange._sort_bids([self.bids], "price_bid")
#                 most_expensive_bid_capacity = self.bids[-1].capacity_bid
#
#                 if self.bids[0].price_per_mwh == elecsim.scenario.scenario_data.lost_load:
#                     new_bid.accept_bid(self.segment_hour)
#                     self.bids.append(new_bid)
#                     capacity_undercut = 0
#                 elif capacity_undercut > most_expensive_bid_capacity:
#                     del self.bids[-1]
#                     capacity_undercut = capacity_undercut - most_expensive_bid_capacity
#                     new_bid.accept_bid(self.segment_hour)
#                     self.bids.append(new_bid)
#                 elif capacity_undercut < most_expensive_bid_capacity:
#                     self.bids[-1].capacity_bid = self.bids[-1].capacity_bid - capacity_undercut
#                     new_bid.partially_accept_bid(self.segment_hour, capacity_undercut)
#                     self.bids.append(new_bid)
#                     capacity_undercut = 0
#                 else:
#                     new_bid.reject_bid(segment_hour=self.segment_hour)
#                     capacity_undercut = 0
#
#             # if self.capacity_required > 0:
#             #     self.bids.append(Bid(None, None, self.segment_hour, 0, elecsim.scenario.scenario_data.lost_load, self.model.year_number))
#
#         return self.bids
#
#
# class NoHistoryBidResponder(BidResponder):
#
#     def __init__(self, bids, capacity_required, segment_hour):
#         super().__init__(bids=bids, capacity_required=capacity_required, segment_hour=segment_hour)
#
#     def get_accepted_bids(self):
#         accepted_bids = [bid for bid in (self.classify_bids(bid) for bid in self.bids) if bid is not None]
#         return accepted_bids
#
#     def classify_bids(self, bid):
#         if self.capacity_required > 0 and self.capacity_required > bid.capacity_bid:
#             bid.accept_bid(self.segment_hour)
#             self.capacity_required -= bid.capacity_bid
#             # accepted_bids.append(bid)
#             logger.debug(
#                 'bid ACCEPTED: price: {}, year: {}, capacity required: {}, capacity: {}, capacity_bid: {}, type: {}, name {}'.format(
#                     bid.price_per_mwh, bid.plant.construction_year, self.capacity_required, bid.plant.capacity_mw,
#                     bid.capacity_bid, bid.plant.plant_type, bid.plant.name))
#             return bid
#         elif bid.capacity_bid > self.capacity_required > 0:
#             bid.partially_accept_bid(self.segment_hour, self.capacity_required)
#             self.capacity_required = 0
#             # accepted_bids.append(bid)
#             logger.debug(
#                 'bid PARTIALLY ACCEPTED: price: {}, year: {}, capacity required: {}, capacity: {}, capacity_bid: {}, type: {}, name {}'.format(
#                     bid.price_per_mwh, bid.plant.construction_year, self.capacity_required, bid.plant.capacity_mw,
#                     bid.capacity_bid, bid.plant.plant_type, bid.plant.name))
#             return bid
#         else:
#             bid.reject_bid(segment_hour=self.segment_hour)
#             logger.debug(
#                 'bid REJECTED: price: {}, year: {}, capacity required: {}, capacity: {}, capacity_bid: {}, type: {}, name {}'.format(
#                     bid.price_per_mwh, bid.plant.construction_year, self.capacity_required, bid.plant.capacity_mw,
#                     bid.capacity_bid, bid.plant.plant_type, bid.plant.name))
#             return None
#         # return capacity_required
#
#
#
#
