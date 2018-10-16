import pandas as pd

from elecsim.src.plants.power_plant import PowerPlant


class CostConversion:

    def __init__(self, start_date, capacity, fuel):
        self.start_date = start_date
        self.capacity = capacity
        self.fuel = fuel

    def plant_to_costs(self):
        cost_data = pd.read_csv("../../../data/Power_Plants/Power_Plant_costs/Power_Plant_Costs_CSV/power_plant_costs_with_simplified_type.csv")




        # power_plant = PowerPlant(name = plant.Name, plant_type = plant.Fuel, capacity_mw = plant.Capacity)


CostConversion(1990, 400, "Gas").plant_to_costs()
