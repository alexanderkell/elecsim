import pandas as pd

class UKPlants():

    def __init__(self, uk_plant_db_dir):
        self.plant_db = pd.read_csv(uk_plant_db_dir)

    def plant_type_synchronisation(self):

        self.plant_db['Simplified_Type'] = self.plant_db['Fuel'].map(lambda x:
                                                             "Biomass" if "Meat" == x
                                                             else "Offshore" if "Wind (offshore)" == x
                                                             else "Biomass" if "Biomass_poultry_litter" == x
                                                             else "Biomass" if "Straw" == x
                                                             else "Recip_diesel" if "Diesel" == x
                                                             else "Biomass" if "Biomass_wood" == x
                                                             else "Recip_gas" if "Gas" == x
                                                             else "PV" if "Solar" == x
                                                             else "Diesel" if "Gas oil" == x
                                                             else "EfW" if "Waste" == x
                                                             else "Hydro_Store" if "Pumped storage" == x
                                                             else "Onshore" if "Wind" == x
                                                             else x)

        # self.plant_db = self.plant_db[self.plant_db['Fuel']=="Gas oil"]

        return self.plant_db

plant_db = UKPlants("/Users/b1017579/Documents/PhD/Projects/10. ELECSIM/elecsim/data/Power_Plants/No_Location/power_plants_2018.csv")
plant_db = plant_db.plant_type_synchronisation()
plant_db.to_csv('/Users/b1017579/Documents/PhD/Projects/10. ELECSIM/elecsim/data/Power_Plants/No_Location/power_plant_db_with_simplified_type.csv')
