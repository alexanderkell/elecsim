import pandas as pd
pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 5000)


class UKPlants:

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
                                                             else "Recip_diesel" if "Gas oil" == x
                                                             else "EfW" if "Waste" == x
                                                             else "Hydro_Store" if "Pumped storage" == x
                                                             else "Onshore" if "Wind" == x
                                                             else x)

    def remove_ambiguous_values(self):
        print(self.plant_db.head())
        self.plant_db.loc[418, 'Start_date'] = '2002.00'
        return self.plant_db

pp_dat = UKPlants("/Users/b1017579/Documents/PhD/Projects/10. ELECSIM/elecsim/data/Power_Plants/No_Location/power_plants_2018.csv")
plant_db = pp_dat.plant_type_synchronisation()
plant_db = pp_dat.remove_ambiguous_values()
plant_db.to_csv('/Users/b1017579/Documents/PhD/Projects/10. ELECSIM/elecsim/data/Power_Plants/No_Location/power_plant_db_with_simplified_type.csv')
