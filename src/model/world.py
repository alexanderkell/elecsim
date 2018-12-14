from src.agents.demand.demand import Demand
from src.agents.generation_company.gen_co import GenCo
from src.data_manipulation.uk_gencos_and_plants import company_names
from src.plants.plant_costs.estimate_costs.estimate_costs import select_cost_estimator
from src.power_exchange.power_exchange import PowerEx
from src.plants.plant_type.plant_registry import PlantRegistry
from mesa import Model

import pandas as pd

from src.mesa_addons.scheduler_addon import OrderedActivation

"""Model.py: Model for the electricity landscape world"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"


class World(Model):
    """
    Model for the electricity landscape world
    """

    def __init__(self, scenario):
        # Set up model objects
        self.year_number = 0

        self.schedule = OrderedActivation(self)

        self.demand = Demand(1, scenario.segment_time, scenario.segment, scenario.yearly_demand_change)
        self.schedule.add(self.demand)

        # Create PowerExchange
        self.PowerExchange = PowerEx(self)
        self.schedule.add(self.PowerExchange)

        # Import company data including financials and plant data
        plant_data = scenario.power_plants
        financial_data = scenario.company_financials

        # Initialize generation companies using financial and plant data
        self.initialize_gencos(financial_data, plant_data)

        self.running = True

    def step(self):
        '''Advance model by one step'''
        self.schedule.step()

        # self.PowerExchange.tender_bids(self.schedule.agents, self.demand.segment_hours, self.demand.segment_consumption)

        self.year_number += 1

    def initialize_gencos(self, financial_data, plant_data):
        """
        Creates generation company agents based on financial data and power plants owned. Estimates cost parameters
         of each power plant if data not known.
        :param financial_data: Data containing information about generation company's financial status
        :param plant_data: Data containing information about generation company's plants owned, start year and name.
        """
        # Initializing generator company data
        companies_groups = plant_data.groupby('Company')
        company_financials = financial_data.groupby('Company')
        # Initialize generation companies with their respective power plants
        for gen_id, ((name, data), (_, financials)) in enumerate(zip(companies_groups, company_financials), 0):
            gen_co = GenCo(self, gen_id, name=name, money=financials.cash_in_bank.iloc[0])
            print("adding GenCo {} with cash {}".format(gen_co.name, gen_co.money))
            # Add power plants to generation company portfolio
            for plant in data.itertuples():
                estimated_cost_parameters = select_cost_estimator(start_year=plant.Start_date,
                                                                  plant_type=plant.Simplified_Type,
                                                                  capacity=plant.Capacity)
                power_plant_obj = PlantRegistry(plant.Simplified_Type).plant_type_to_plant_object()
                power_plant = power_plant_obj(name=plant.Name, plant_type=plant.Simplified_Type,
                                              capacity_mw=plant.Capacity, construction_year=plant.Start_date,
                                              **estimated_cost_parameters)
                gen_co.plants.append(power_plant)
        self.schedule.add(gen_co)
