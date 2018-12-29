import logging
from random import uniform

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
        # plant_data = plant_data[:150]
        financial_data = scenario.company_financials

        # Initialize generation companies using financial and plant data
        self.initialize_gencos(financial_data, plant_data)

        self.demand = Demand(self.unique_id_generator, scenario.segment_time, scenario.segment_demand_diff, scenario.yearly_demand_change)
        self.unique_id_generator+=1
        self.schedule.add(self.demand)

        # Create PowerExchange
        self.PowerExchange = PowerExchange(self)

        self.running = True

    def step(self):
        '''Advance model by one step'''
        self.schedule.step()

        self.PowerExchange.tender_bids(self.demand.segment_hours, self.demand.segment_consumption)

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
        companies_groups = plant_data.groupby('Company')
        company_financials = financial_data.groupby('Company')

        logger.info("Initialising generation companies with their power plants.")
        # Initialize generation companies with their respective power plants
        for gen_id, ((name, data), (_, financials)) in enumerate(zip(companies_groups, company_financials), 0):
            gen_co = GenCo(unique_id=gen_id, model=self, discount_rate=round(uniform(0.04,0.08),3), name=name, money=financials.cash_in_bank.iloc[0])
            self.unique_id_generator+=1
            # Add power plants to generation company portfolio
            for plant in data.itertuples():
                power_plant = create_power_plant(plant.Name, plant.Start_date, plant.Simplified_Type, plant.Capacity)
                gen_co.plants.append(power_plant)
            logger.debug('Adding generation company: {}'.format(gen_co.name))
            self.schedule.add(gen_co)
        logger.info("Added generation companies.")


