from src.agents.demand.demand import Demand
from src.agents.generation_company.gen_co import GenCo
from src.data_manipulation.uk_gencos_and_plants import company_names
from src.plants.plant_costs.estimate_costs.predict_modern_plant_costs import PredictPlantStatistics
from src.power_exchange.power_exchange import PowerEx
from mesa import Model

from src.mesa_addons.scheduler_addon import OrderedActivation

"""Model.py: Model for the electricity landscape world"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"


class Model(Model):
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
            for plant in genco_plant_db.itertuples():
                # print(plant.Simplified_Type)
                estimated_statistics = PredictPlantStatistics(plant.Simplified_Type, plant.Capacity, plant.Start_date)()
                # print(estimated_statistics)
                # power_plant = PowerPlant(name = plant.Name, plant_type = plant.Fuel, capacity_mw = plant.Capacity)

                # gen_co.plants.append(power_plant)

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
