import datetime as dt
import logging
import os
from random import uniform, randint, sample
from time import perf_counter
import importlib.util
import time
import dropbox

import numpy as np
import pandas as pd
from mesa import Model
from mesa.datacollection import DataCollector
import pickle
from ray.rllib.utils.policy_client import PolicyClient

from elecsim.plants.fuel.capacity_factor.capacity_factor_calculations import get_capacity_factor

from elecsim.agents.demand.demand import Demand
from elecsim.agents.demand.multi_day_demand import MultiDayDemand
from elecsim.agents.generation_company.gen_co import GenCo
from elecsim.constants import ROOT_DIR
from elecsim.market.electricity.market.power_exchange import PowerExchange
from elecsim.mesa_addons.scheduler_addon import OrderedActivation
from elecsim.plants.plant_costs.estimate_costs.estimate_costs import create_power_plant
from elecsim.plants.plant_type.fuel_plant import FuelPlant
import elecsim.data_manipulation.data_modifications.scenario_modifier as scen_mod
from elecsim.role.market.latest_market_data import LatestMarketData

import elecsim.scenario.scenario_data

import os

logger = logging.getLogger(__name__)


"""Model.py: Model for the electricity landscape world"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"

class World(Model):
    """
    Model for the electricity landscape world
    """

    def __init__(self, initialization_year, scenario_file=None, fitting_params=None, long_term_fitting_params=None, future_price_uncertainty_m = None, future_price_uncertainty_c = None, carbon_price_scenario=None, demand_change=None, demand_distribution=None, number_of_steps=32, total_demand=None, number_of_agents=None, market_time_splices=1, data_folder=None, time_run=False, nuclear_subsidy=None, highest_demand=None, log_level="warning", client_rl=None, distribution_name = None):
        """
        Initialize an electricity market in a particular country. Provides the ability to change scenarios from this constructor.
        :param int initialization_year: Year to begin simulation.
        :param list: float carbon_price_scenario: Scenario containing carbon price for each year of simulation.
        :param list: float demand_change: Scenario containing change in demand between each year of simulation.
        :param int number_of_steps: Total number of years to run scenario.
        :param int total_demand: Total size of country's demand.
        :param str data_folder: Directory and folder to save run data to
        :param bool time_run:
        :param str log_level:
        """

        self.start = perf_counter()
        logger.info("start: {}".format(self.start))
        # Set up model objects
        self.year_number = initialization_year
        self.years_from_start = 0
        self.step_number = 0
        self.unique_id_generator = 0
        self.time_run = time_run
        self.max_number_of_steps = number_of_steps
        self.average_electricity_price = 0
        self.market_time_splices = market_time_splices

        self.nuclear_subsidy = nuclear_subsidy

        self.set_log_level(log_level)

        self.overwrite_scenario_file(scenario_file)

        self.override_highest_demand(highest_demand)
        self.override_carbon_scenario(carbon_price_scenario)
        self.override_demand_change(demand_change)

        self.demand_distribution_uncertainty = demand_distribution
        self.distribution_name = distribution_name

        self.override_total_demand(total_demand, number_of_agents)

        self.schedule = OrderedActivation(self)

        # Import company data including financials and plant data
        plant_data = elecsim.scenario.scenario_data.power_plants
        financial_data = elecsim.scenario.scenario_data.company_financials

        # Initialize generation companies using financial and plant data
        self.initialize_gencos(financial_data, plant_data)

        self.last_added_plant = None
        self.last_added_plant_bids = None

        # Create PowerExchange

        if self.market_time_splices == 1:
            self.PowerExchange = PowerExchange(self, demand_distribution)
            self.demand = Demand(self, self.unique_id_generator, elecsim.scenario.scenario_data.segment_time, elecsim.scenario.scenario_data.segment_demand_diff)
        elif self.market_time_splices > 1:
            self.PowerExchange = PowerExchange(self, demand_distribution)
            # self.PowerExchange = HighTemporalExchange(self)
            self.demand = MultiDayDemand(self, self.unique_id_generator, elecsim.scenario.scenario_data.multi_year_data)
        else:
            raise ValueError("market_time_splices must be equal to or larger than 1.")


        self.running = True
        self.beginning_of_year = False

        self.continue_investing = 0
        self.over_invested = False

        self.unique_id_generator += 1
        self.schedule.add(self.demand)
        self.create_data_loggers(data_folder)

        if elecsim.scenario.scenario_data.investment_mechanism == "RL":
            # self.client = PolicyClient("http://rllibserver:9900")
            self.client = client_rl
            self.eid = self.client.start_episode(training_enabled=True)
            self.intial_obs = LatestMarketData(self).get_RL_investment_observations()
            # logger.info("self.intial_obs: {}".format(self.intial_obs))
        elif elecsim.scenario.scenario_data.investment_mechanism == "future_price_fit":
            self.future_price_uncertainty_m = future_price_uncertainty_m
            self.future_price_uncertainty_c = future_price_uncertainty_c
            if fitting_params is not None:
                self.fitting_params = fitting_params
            elif long_term_fitting_params is not None:
                self.long_term_fitting_params = long_term_fitting_params
                self.fitting_params = None
            else:
                raise ValueError("If using future_price_fit you must enter a value for long_term_fitting_params or fitting_params in the constructor of World")


    def step(self, carbon_price=None):
        '''Advance model by one step'''
        self.beginning_of_year = False

        if self.step_number % self.market_time_splices == 0:
            self.start = time.perf_counter()
            self.operate_constructed_plants()
            if self.step_number != 0:
                self.year_number += 1
                self.years_from_start += 1
                # self.operate_constructed_plants()
                self.beginning_of_year = True
                # logger.info("year: {}".format(self.year_number))
                print("{}:".format(self.year_number), end='', flush=True)
            else:
                print("{}:".format(self.year_number), end='', flush=True)

        obs = self.schedule.step()
        self.operate_constructed_plants()

        if self.over_invested:
            return self.datacollector.get_model_vars_dataframe(), self.over_invested

        self.continue_investing = 0
        if carbon_price is not None:
            elecsim.scenario.scenario_data.carbon_price_scenario[self.year_number + 1] = carbon_price
        else:
            elecsim.scenario.scenario_data.carbon_price_scenario = elecsim.scenario.scenario_data.carbon_price_scenario

        if self.beginning_of_year:
            self.dismantle_old_plants()
            self.dismantle_unprofitable_plants()

        self.average_electricity_price = self.PowerExchange.tender_bids(self.demand.segment_hours, self.demand.segment_consumption).accepted_price.mean()
        self.PowerExchange.price_duration_curve = []

        carbon_emitted = self.get_carbon_emitted(self)
        self.settle_gencos_financials()

        self.datacollector.collect(self)
        self.delete_old_bids()

        self.step_number += 1
        print(".", end='', flush=True)

        self.write_scenario_data()

        if isinstance(self.average_electricity_price, np.ndarray):
            self.average_electricity_price = self.average_electricity_price[0]

        if self.step_number % self.market_time_splices == 0:
            end = time.perf_counter()
            print("time taken: {}".format(end-self.start))
            # get_capacity_factor.cache_clear()

        if self.step_number == self.max_number_of_steps and elecsim.scenario.scenario_data.investment_mechanism == "RL":
            obs = LatestMarketData(self).get_RL_investment_observations()
            self.client.end_episode(self.eid, observation=obs)
            del self.client

        logger.debug(self.datacollector.get_model_vars_dataframe())
        return abs(self.average_electricity_price), abs(carbon_emitted)
        # return self.datacollector.get_model_vars_dataframe(), self.over_invested

    def initialize_gencos(self, financial_data, plant_data):
        """
        Creates generation company agents based on financial data and power plants owned. Estimates cost parameters
         of each power plant if data not for power plant not available.
        :param financial_data: Data containing information about generation company's financial status
        :param plant_data: Data containing information about generation company's plants owned, start year and name.
        """

        financial_data = pd.merge(financial_data, plant_data, on="Company", how="inner")
        financial_data = financial_data[['Company', 'cash_in_bank']]

        # Initialising generator company data
        financial_data.cash_in_bank = financial_data.cash_in_bank.replace("nan", np.nan)
        financial_data.cash_in_bank = financial_data.cash_in_bank.fillna(0)
        companies_groups = plant_data.groupby('Company')
        company_financials = financial_data.groupby('Company')

        logger.info("Initialising generation companies with their power plants.")

        # Initialize generation companies with their respective power plants
        for gen_id, ((name, data), (_, financials)) in enumerate(zip(companies_groups, company_financials), 0):
            if financials.Company.iloc[0] != name:
                raise ValueError("Company financials name ({}) and agent name ({}) do not match.".format(financials.Company.iloc[0], name))

            gen_co = GenCo(unique_id=gen_id, model=self, difference_in_discount_rate=round(uniform(-0.03, 0.03), 3), look_back_period=randint(3, 7), name=name, money=financials.cash_in_bank.iloc[0])
            self.unique_id_generator += 1
            # Add power plants to generation company portfolio
            # parent_directory = os.path.dirname(os.getcwd())
            pickle_directory = "{}/../elecsim/data/processed/pickled_data/power_plants/".format(ROOT_DIR)
            for plant in data.itertuples():
                try:
                    power_plant = pickle.load(open("{}{}-{}.pickle".format(pickle_directory, plant.Name, plant.Start_date), "rb"))
                except (OSError, IOError, FileNotFoundError) as e:
                    logger.info("plant: {}".format(plant))
                    power_plant = create_power_plant(plant.Name, plant.Start_date, plant.Simplified_Type, plant.Capacity)
                    pickle.dump(power_plant, open("{}{}-{}.pickle".format(pickle_directory, plant.Name, plant.Start_date), "wb"))
                gen_co.plants.append(power_plant)
            logger.debug('Adding generation company: {}'.format(gen_co.name))
            self.schedule.add(gen_co)
        logger.info("Added generation companies.")


    def get_running_plants(self, plants):
        for plant in plants:
            # if plant.name in elecsim.scenario.scenario_data.known_plant_retirements:

            if plant.construction_year <= 1990 and plant.name != "invested_plant" and plant.name not in elecsim.scenario.scenario_data.known_plant_retirements:
                # Reset old plants that have been modernised with new construction year
                plant.construction_year = randint(self.year_number-15, self.year_number)
                # yield plant
            elif plant.name in elecsim.scenario.scenario_data.known_plant_retirements:
                plant.construction_year = elecsim.scenario.scenario_data.known_plant_retirements[plant.name] - (plant.operating_period + plant.construction_period + plant.pre_dev_period) - 1
                logger.info("plant.name: {}, plant.construction_year: {}".format(plant.name, plant.construction_year))

            if plant.construction_year + plant.operating_period + plant.construction_period + plant.pre_dev_period >= self.year_number:
                yield plant
            else:
                logger.debug("Taking the plant '{}' out of service, year of construction: {}".format(plant.name,
                                                                        plant.construction_year))



    def dismantle_old_plants(self):
        """
        Remove plants that are past their lifetime agent from each agent from their plant list
        """

        gencos = self.get_gencos()

        for genco in gencos:
            plants_filtered = list(self.get_running_plants(genco.plants))
            genco.plants = plants_filtered

    def dismantle_unprofitable_plants(self):

        gencos = self.get_gencos()

        for genco in gencos:
            profitable_plants = list(self.filter_plants_with_no_income(genco.plants))
            genco.plants = profitable_plants

    def filter_plants_with_no_income(self, plants):
            for plant in plants:
                if (self.year_number > 7) and (plant.get_year_of_operation() + 7 < self.year_number):
                    historic_bids = plant.historical_bids
                    # logger.info("historic_bids {}".format(historic_bids))
                    # years_to_look_into = list(range(self.year_number,self.year_number-7,-1))

                    seven_years_previous = self.year_number-7
                    if historic_bids:
                        if historic_bids[-1].year_of_bid > seven_years_previous:
                            yield plant
                        else:
                            logger.debug("Plant {}, type {} is unprofitable. Last accepted bid: {}".format(plant.name, plant.plant_type, historic_bids[-1].year_of_bid))
                            for bid in plant.accepted_bids:
                                del bid
                    else:
                        logger.debug("Plant {}, type {} is unprofitable.".format(plant.name, plant.plant_type))
                        for bid in plant.accepted_bids:
                            del bid
                    # bids_to_check = list(filter(lambda x: x.year_of_bid in years_to_look_into, historic_bids))
                    # total_income_in_previous_years = sum(bid.price_per_mwh for bid in bids_to_check)
                    # for bids in reversed(historic_bids):
                    #     logger.info("bids.year_of_bid: {}".format(bids.year_of_bid))

                    # if total_income_in_previous_years > 0:
                    #     yield plant
                    # else:
                    #     logger.debug("Taking plant: {} out of service.".format(plant.name))
                else:
                    yield plant

    def get_profitable_plants(self, plants):
        for plant in plants:
            if self.step_number > 7 and plant.get_year_of_operation() + 7 > self.year_number:
                historic_bids = plant.historical_bids
                pass

    def operate_constructed_plants(self, minimum_operation_year=2018):
        gencos = self.get_gencos()
        logger.debug("gencos: {}".format(gencos))
        for genco in gencos:
            logger.debug("genco plants: {}".format(genco.plants))
            for plant in genco.plants:
                # logger.debug("plant: {}, year_number: {}, construction year+constructioon_period+predev: {}".format(plant, self.year_number, plant.construction_year + plant.construction_period + plant.pre_dev_period))
                if plant.construction_year <= minimum_operation_year:
                    plant.is_operating = True
                elif (plant.is_operating is False) and (self.year_number >= plant.construction_year + plant.construction_period + plant.pre_dev_period):
                    plant.is_operating = True

    def overwrite_scenario_file(self, scenario_file):
        if scenario_file:
            split_directory = scenario_file.split("/")
            file_name = split_directory[-1]
            spec = importlib.util.spec_from_file_location(file_name, scenario_file)
            scenario_import = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(scenario_import)
            scen_mod.overwrite_scenario_file(scenario_import)

    def settle_gencos_financials(self):
        gencos = self.get_gencos()
        for genco in gencos:
            genco.settle_accounts()
            # genco.delete_old_bids()

    def delete_old_bids(self):
        gencos = self.get_gencos()
        for genco in gencos:
            genco.delete_old_bids()

    def get_gencos(self):
        gencos = [genco for genco in self.schedule.agents if isinstance(genco, GenCo)]
        return gencos

    def clear_all_bids(self):
        gencos = self.get_gencos()
        for genco in gencos:
            genco.delete_old_bids()

    @staticmethod
    def get_capacity_of_plants(model, plant_type):
        gencos = model.get_gencos()
        plants = [plant for genco in gencos for plant in genco.plants if plant.plant_type == plant_type and plant.is_operating]
        total_capacity = sum(plant.capacity_mw for plant in plants)

        return total_capacity


    @staticmethod
    def get_all_plants(model):
        gencos = model.get_gencos()
        plants = [plant for genco in gencos for plant in genco.plants]
        return plants


    @staticmethod
    def get_current_carbon_tax(model):
        carbon_tax = elecsim.scenario.scenario_data.carbon_price_scenario[model.years_from_start]
        return carbon_tax

    @staticmethod
    def get_genco_wealth(model):
        gencos = model.get_gencos()
        total_wealth = 0
        for genco in gencos:
            total_wealth += genco.money
        return total_wealth

    @staticmethod
    def get_electricity_cost(model):
        return model.average_electricity_price

    @staticmethod
    def get_carbon_emitted(model):
        gencos = model.get_gencos()
        bids = World.get_accepted_bids(gencos, FuelPlant)
        
        carbon_emitted = sum(bid.capacity_bid * bid.plant.fuel.co2_density for bid in bids if isinstance(bid.plant, FuelPlant))
        return carbon_emitted

    @staticmethod
    def get_accepted_bid_capacity(model, plant_type):
        gencos = model.get_gencos()
        plants = [plant for genco in gencos for plant in genco.plants if plant.plant_type == plant_type and plant.is_operating]
        capacity_contributed = sum(bid.capacity_bid for plant in plants for bid in plant.accepted_bids)
        return capacity_contributed

    @staticmethod
    def get_accepted_bid_capacity_per_segment_hour(model):
        gencos = model.get_gencos()
        plants = [plant for genco in gencos for plant in genco.plants if plant.is_operating]
        # capacity_contributed = [ if bid.segment_hours==]
        bids_dataframe = [bid.to_dict() for plant in plants for bid in plant.accepted_bids]
        return bids_dataframe


    @staticmethod
    def get_accepted_bids(gencos, plant_type=None):
        if plant_type:
            bids = list(
                accepted_bids for genco in gencos for plants in genco.plants for accepted_bids in plants.accepted_bids if
                isinstance(plants, plant_type))
        else:
            bids = list(
                accepted_bids for genco in gencos for plants in genco.plants for accepted_bids in plants.accepted_bids)

        return bids

    def stratify_data(self, demand):
        power_plants = elecsim.scenario.scenario_data.power_plants
        frac_to_scale = demand/power_plants.Capacity.sum()

        stratified_sample = power_plants.groupby(['Fuel'], as_index=False).apply(lambda x: x.sample(frac=frac_to_scale, replace=True))
        return stratified_sample




    def set_log_level(self, log_level):
        if log_level.lower() == "warning":
            logging.basicConfig(level=logging.WARNING)
        elif log_level.lower() == "info":
            logging.basicConfig(level=logging.INFO)
        elif log_level.lower() == "debug":
            logging.basicConfig(level=logging.DEBUG)
        else:
            raise ValueError("log_level must be warning, info or debug and not {}".format(log_level))

    def create_data_loggers(self, data_folder):
        self.data_folder = data_folder
        self.datacollector = DataCollector(
            model_reporters={"contributed_CCGT": lambda m: self.get_accepted_bid_capacity(m, "CCGT"),
                             "contributed_Coal": lambda m: self.get_accepted_bid_capacity(m, "Coal"),
                             "contributed_Onshore": lambda m: self.get_accepted_bid_capacity(m, "Onshore"),
                             "contributed_Offshore": lambda m: self.get_accepted_bid_capacity(m, "Offshore"),
                             "contributed_PV": lambda m: self.get_accepted_bid_capacity(m, "PV"),
                             "contributed_Nuclear": lambda m: self.get_accepted_bid_capacity(m, "Nuclear"),
                             "contributed_Recip_gas": lambda m: self.get_accepted_bid_capacity(m, "Recip_gas"),
                             "contributed_Biomass": lambda m: self.get_accepted_bid_capacity(m, "Biomass"),

                             # "hourly_accepted_bids": lambda m: self.get_accepted_bid_capacity_per_segment_hour(m),

                             "total_CCGT": lambda m: self.get_capacity_of_plants(m, "CCGT"),
                             "total_Coal": lambda m: self.get_capacity_of_plants(m, "Coal"),
                             "total_Onshore": lambda m: self.get_capacity_of_plants(m, "Onshore"),
                             "total_Offshore": lambda m: self.get_capacity_of_plants(m, "Offshore"),
                             "total_PV": lambda m: self.get_capacity_of_plants(m, "PV"),
                             "total_Nuclear": lambda m: self.get_capacity_of_plants(m, "Nuclear"),
                             "total_Recip_gas": lambda m: self.get_capacity_of_plants(m, "Recip_gas"),
                             "Carbon_tax": lambda m: self.get_current_carbon_tax(m),
                             "total_genco_wealth": lambda m: self.get_genco_wealth(m),
                             "Electricity_cost": lambda m: self.get_electricity_cost(m),
                             "Carbon_emitted": lambda m: self.get_carbon_emitted(m)
                             }

        )

    def override_total_demand(self, total_demand, number_of_agents=None):
        self.total_demand = total_demand
        if total_demand is not None:
            elecsim.scenario.scenario_data.power_plants = self.stratify_data(total_demand)
            demand_modifier = (elecsim.scenario.scenario_data.power_plants.Capacity.sum() /
                               elecsim.scenario.scenario_data.segment_demand_diff[-1]) / 1.6
            logger.info("demand_modifier: {}".format(demand_modifier))
            logger.info(
                "total available capacity: {}".format(elecsim.scenario.scenario_data.power_plants.Capacity.sum()))
            elecsim.scenario.scenario_data.segment_demand_diff = [demand_modifier * demand for demand in
                                                                    elecsim.scenario.scenario_data.segment_demand_diff]

            if number_of_agents is not None:
                total_plants = len(elecsim.scenario.scenario_data.power_plants)
                fraction_to_replace = total_plants/number_of_agents
                company_names = sample(list(elecsim.scenario.scenario_data.power_plants.Company.unique()), number_of_agents)

                company_name_repeated = np.repeat(company_names, int(fraction_to_replace))
                company_name_repeated = np.append(company_name_repeated, np.array(["company_{}".format(number_of_agents-1) for i in range(100)]))

                elecsim.scenario.scenario_data.power_plants.Company = company_name_repeated[:total_plants]

    def override_highest_demand(self, highest_demand):
        if highest_demand:
            elecsim.scenario.scenario_data.initial_max_demand_size = highest_demand

    def override_demand_change(self, demand_change):
        if demand_change:
            elecsim.scenario.scenario_data.yearly_demand_change = demand_change[1:]
            self.demand_change_name = str(demand_change[0]).replace(".", '')
        else:
            self.demand_change_name = "none"

    def override_carbon_scenario(self, carbon_price_scenario):
        if carbon_price_scenario:
            elecsim.scenario.scenario_data.carbon_price_scenario = carbon_price_scenario[1:]
            self.carbon_scenario_name = str(carbon_price_scenario[0]).replace(".", '')
        else:
            self.carbon_scenario_name = "none"

    def write_scenario_data(self):
        if self.step_number == self.max_number_of_steps:
            parent_directory = os.path.dirname(os.getcwd())

            directory = "{}/{}/".format(parent_directory, self.data_folder)
            if not os.path.exists(directory):
                os.makedirs(directory)

            filename = "demand_{}-carbon_{}-datetime_{}-capacity_{}-demand_distribution_{}.csv".format(
                                                                                               self.demand_change_name,
                                                                                               self.carbon_scenario_name,
                                                                                               dt.datetime.now().strftime(
                                                                                                   '%Y-%m-%d_%H-%M-%S'),
                                                                                               elecsim.scenario.scenario_data.segment_demand_diff[
                                                                                                   -1], self.distribution_name)

            directory_filename = "{}/{}.csv".format(directory, filename)

            results_df = self.datacollector.get_model_vars_dataframe()
            results_df.to_csv(directory_filename)

            class TransferData:
                def __init__(self, access_token):
                    self.access_token = access_token

                def upload_file(self, file_from, file_to):
                    """upload a file to Dropbox using API v2
                    """
                    dbx = dropbox.Dropbox(self.access_token)

                    with open(file_from, 'rb') as f:
                        dbx.files_upload(f.read(), file_to)

            access_token = 'J0BrnIaGJ78AAAAAAABLCd6RWS4T1JQwhKCtYcdWTdyE--pvA0-DfNIt4OUnUZQx'
            transferData = TransferData(access_token)

            file_from = "/{}".format(directory_filename)
            file_to = "/{}".format(filename)

            # API v2
            transferData.upload_file(file_from, file_to)






        if self.step_number == self.max_number_of_steps:
            end = perf_counter()
            time_elapased = end - self.start

            self.write_timing_results(end, time_elapased)

    def write_timing_results(self, end, time_elapased):
        if self.time_run:
            timings_data = pd.DataFrame(
                {"time": [time_elapased], "carbon": [elecsim.scenario.scenario_data.carbon_price_scenario[0]],
                 'installed_capacity': [elecsim.scenario.scenario_data.power_plants.Capacity.sum()],
                 'datetime': [dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')]})

            parent_directory = os.path.dirname(os.getcwd())

            with open("{}/{}/timing.csv".format(ROOT_DIR, self.data_folder), 'a') as f:
                timings_data.to_csv(f, header=False)
            logger.info("end: {}".format(end))
            logger.info("time_elapsed: {}, carbon: {}, size: {}".format(time_elapased,
                                                                    elecsim.scenario.scenario_data.carbon_price_scenario[
                                                                        0],
                                                                    elecsim.scenario.scenario_data.power_plants.Capacity.sum()))

