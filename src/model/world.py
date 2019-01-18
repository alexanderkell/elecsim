import logging
from random import uniform, randint

import numpy as np

from mesa import Model
from mesa.datacollection import DataCollector

from src.plants.plant_registry import PlantRegistry
from src.agents.demand.demand import Demand
from src.agents.generation_company.gen_co import GenCo
from src.market.electricity.power_exchange import PowerExchange
from src.mesa_addons.scheduler_addon import OrderedActivation
from src.plants.plant_costs.estimate_costs.estimate_costs import create_power_plant

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

    def __init__(self, scenario, initialization_year):
        # Set up model objects
        self.year_number = initialization_year
        self.step_number = 0
        self.unique_id_generator = 0

        self.schedule = OrderedActivation(self)

        # Import company data including financials and plant data
        plant_data = scenario.power_plants
        financial_data = scenario.company_financials

        # Initialize generation companies using financial and plant data
        self.initialize_gencos(financial_data, plant_data)

        self.demand = Demand(self.unique_id_generator, scenario.segment_time, scenario.segment_demand_diff, scenario.yearly_demand_change)
        self.unique_id_generator+=1
        self.schedule.add(self.demand)

        # Create PowerExchange
        self.PowerExchange = PowerExchange(self)
        self.running = True

        # Tender first bids to initialize the "price_duration_curve"
        # self.PowerExchange.tender_bids(self.demand.segment_hours, self.demand.segment_consumption)

    def step(self):
        '''Advance model by one step'''
        self.operate_constructed_plants()
        self.schedule.step()
        logger.info("Stepping year: {}".format(self.year_number))
        logger.info("number of plants: {}".format(len([plant for gencos in self.get_gencos() for plant in gencos.plants])))
        logger.info("number of operating plants: {}".format(len([plant for gencos in self.get_gencos() for plant in gencos.plants if plant.is_operating == True])))

        self.dismantle_old_plants()
        self.dismantle_unprofitable_plant()
        self.PowerExchange.tender_bids(self.demand.segment_hours, self.demand.segment_consumption)
        self.settle_gencos_financials()
        self.year_number += 1
        self.step_number +=1

    def initialize_gencos(self, financial_data, plant_data):
        """
        Creates generation company agents based on financial data and power plants owned. Estimates cost parameters
         of each power plant if data not for power plant not available.
        :param financial_data: Data containing information about generation company's financial status
        :param plant_data: Data containing information about generation company's plants owned, start year and name.
        """
        # Initialising generator company data
        financial_data.cash_in_bank = financial_data.cash_in_bank.replace("nan", np.nan)
        financial_data.cash_in_bank = financial_data.cash_in_bank.fillna(0)
        companies_groups = plant_data.groupby('Company')
        company_financials = financial_data.groupby('Company')

        logger.info("Initialising generation companies with their power plants.")
        # Initialize generation companies with their respective power plants
        for gen_id, ((name, data), (_, financials)) in enumerate(zip(companies_groups, company_financials), 0):
            assert financials.Company.iloc[0] == name
            gen_co = GenCo(unique_id=gen_id, model=self, difference_in_discount_rate=round(uniform(-0.03, 0.03), 3), look_back_period=randint(3, 7), name=name, money=financials.cash_in_bank.iloc[0])
            self.unique_id_generator+=1
            # Add power plants to generation company portfolio
            for plant in data.itertuples():
                power_plant = create_power_plant(plant.Name, plant.Start_date, plant.Simplified_Type, plant.Capacity)
                gen_co.plants.append(power_plant)
            logger.info('Adding generation company: {}'.format(gen_co.name))
            self.schedule.add(gen_co)
        logger.info("Added generation companies.")


    def get_running_plants(self, plants):
        for plant in plants:
            if plant.construction_year<=1990 and plant.name != "invested_plant":
                # Reset old plants that have been modernised with new construction year
                plant.construction_year = randint(self.year_number-15, self.year_number)
                yield plant
            elif plant.construction_year + plant.operating_period + plant.construction_period + plant.pre_dev_period >= self.year_number:
                yield plant
            else:
                logger.info("Taking the plant '{}' out of service, year of construction: {}".format(plant.name,
                                                                        plant.construction_year))
                continue


    def dismantle_old_plants(self):
        """
        Remove plants that are past their lifetime agent from each agent from their plant list
        """

        gencos = self.get_gencos()

        for genco in gencos:
            plants_filtered = list(self.get_running_plants(genco.plants))
            genco.plants = plants_filtered

    def dismantle_unprofitable_plant(self):

        gencos = self.get_gencos()

        for genco in gencos:
            profitable_plants = list(self.get_profitable_plants(genco.plants))
            genco.plants = profitable_plants

    def get_profitable_plants(self, plants):
            for plant in plants:
                if self.step_number > 7 and plant.get_year_of_operation() + 7 > self.year_number:
                # if self.step_number > 4 and plant.construction_period+plant.pre_dev_period+plant.construction_year+4>self.year_number:
                    historic_bids = plant.historical_bids
                    # for historic_bid in historic_bids:
                    #     logger.debug("2. historic_bid: {}".format(historic_bid))
                    years_to_look_into = list(range(self.year_number,self.year_number-7,-1))
                    bids_to_check = list(filter(lambda x: x.year_of_bid in years_to_look_into, historic_bids))
                    total_income_in_last_five_years = sum(bid.price_per_mwh for bid in bids_to_check)
                    if total_income_in_last_five_years > 0:
                        yield plant
                    else:
                        logger.debug("Taking plant: {} out of service.".format(plant.name))
                else:
                    yield plant

    def operate_constructed_plants(self):

        gencos = self.get_gencos()
        logger.debug("gencos: {}".format(gencos))
        for genco in gencos:
            logger.debug("genco plants: {}".format(genco.plants))
            for plant in genco.plants:
                # logger.debug("plant: {}, year_number: {}, construction year+constructioon_period+predev: {}".format(plant, self.year_number, plant.construction_year + plant.construction_period + plant.pre_dev_period))
                if plant.construction_year <= 2018:
                    plant.is_operating = True
                elif (plant.is_operating is False) and (self.year_number >= plant.construction_year + plant.construction_period + plant.pre_dev_period):
                    plant.is_operating = True

    def settle_gencos_financials(self):
        gencos = self.get_gencos()
        for genco in gencos:
            genco.settle_accounts()
            genco.delete_old_bids()


    def get_gencos(self):
        gencos = [genco for genco in self.schedule.agents if isinstance(genco, GenCo)]
        return gencos
