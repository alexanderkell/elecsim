import pandas as pd

from elecsim.src.plants.power_plant import PowerPlant


class CostConversion:

    def __init__(self, start_date, capacity, fuel):
        self.start_date = start_date
        self.capacity = capacity
        self.fuel = fuel

    def plant_to_costs(self):
        cost_data = pd.read_csv("../../../data/Power_Plants/Power_Plant_costs/plant_costs_data.csv")
        print(cost_data.head())


        # power_plant = PowerPlant(name = plant.Name, plant_type = plant.Fuel, capacity_mw = plant.Capacity)


CostConversion(1990, 400, "Gas").plant_to_costs()
