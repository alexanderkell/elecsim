from src.agents.demand.demand import Demand
from src.agents.generation_company.gen_co import GenCo
from src.data_manipulation.uk_gencos_and_plants import company_names
from src.plants.plant_costs.estimate_costs.estimate_costs import estimate_costs
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

        # # Create and add generation companies
        # for i in range(scenario.number_of_gencos):
        #     gen_co = GenCo(i, self, scenario.generators_owned[i], scenario.starting_money_of_gencos[i], )
        #     self.schedule.add(gen_co)

        plant_data = scenario.power_plants
        names = company_names(plant_data)

        # Initialize generation companies
        for gen_id, name in enumerate(names,0):
            gen_co = GenCo(gen_id, self, name=name)
            print(gen_id)
            # Add power plants to generation company portfolio
            genco_plant_db = plant_data[plant_data['Company'] == name]
            genco_plant_db.Start_date = pd.to_numeric(genco_plant_db.Start_date)
            for plant in genco_plant_db.itertuples():
                estimated_statistics = estimate_costs(start_year=plant.Start_date, plant_type=plant.Simplified_Type, capacity=plant.Capacity)
                power_plant_obj = PlantRegistry(plant.Simplified_Type).plant_type_to_plant_object()
                power_plant = power_plant_obj(name = plant.Name, plant_type = plant.Fuel, capacity_mw = plant.Capacity, **estimated_statistics)

                gen_co.plants.append(power_plant)

        self.schedule.add(gen_co)

        # for i in range(len(names)):
        #     gen_co = GenCo(i, self, name=names[i])
        #     rows = plant_data.loc[plant_data['Company'] == names[i]]
        #     plants = []
        #     for j in range(len(rows)):
        #         # plants.append()
        #         print(rows.iloc[j])
        #         print(rows.iloc[j].Name)
        #         print(rows.iloc[j].Fuel)
        #         print(rows.iloc[j].Capacity)
        #         print(rows.iloc[j].Start_date)
        #     self.schedule.add(gen_co)
        #     print('-------------- NEW COMPANY --------------')
        # Set running to true
        self.running = True

    def step(self):
        '''Advance model by one step'''
        self.schedule.step()

        # self.PowerExchange.tender_bids(self.schedule.agents, self.demand.segment_hours, self.demand.segment_consumption)

        self.year_number += 1
