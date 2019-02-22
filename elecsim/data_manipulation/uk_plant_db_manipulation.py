import pandas as pd
pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 5000)


class UKPlants:

    def __init__(self, uk_plant_db_dir):
        self.plant_db = pd.read_csv(uk_plant_db_dir)

    def modify_plant_db(self):
        """
        Overall method which runs synchronises UK cost and power plant database, removes ambiguous values and removes
        black start motors
        :return: Returns modified UK power plant database
        """

        self._remove_black_start_motors()
        self._plant_type_synchronisation()
        self._remove_ambiguous_values()

        return self.plant_db

    def _plant_type_synchronisation(self):
        """
        Function to match the power plant type plant_type of the UK power plant database with the UK power plant cost database
        :return: Returns modified power plant database
        """
        self.plant_db['Simplified_Type'] = self.plant_db['Fuel'].map(lambda x:
                                                             "Biomass" if "Meat" == x
                                                             else "Offshore" if "Wind (offshore)" == x
                                                             else "Biomass" if "Biomass_poultry_litter" == x
                                                             else "Biomass" if "Straw" == x
                                                             else "Recip_diesel" if "Diesel" == x
                                                             else "Biomass" if "Biomass_wood" == x
                                                             else "Recip_gas" if "Gas" == x
                                                             else "PV" if "Solar" == x
                                                             else "OCGT" if "Gas oil" == x
                                                             else "EfW" if "Waste" == x
                                                             else "Hydro_Store" if "Pumped storage" == x
                                                             else "Onshore" if "Wind" == x
                                                             else x)

    def _remove_ambiguous_values(self):
        """
        Function which removes ambiguous values from the database.
        :return: Returns modified power plant database
        """
        # Dolgarrog start date labelled as 1926/2002, replaced this with 2002
        self.plant_db.loc[418, 'Start_date'] = '2002.00'

        # Killingholme power station was demolished and closed in 2016.
        self.plant_db = self.plant_db[self.plant_db.Name != 'Killingholme']


    def _remove_black_start_motors(self):
        """
        Removal of power plants due to the fact that they do not contribute to national grid electricity supply,
        and are used as starter motors in the event of an electric grid blackout.
        :return: Returns modified power plant database
        """
        # self.plant_db = self.plant_db[self.plant_db.Name != 'Baglan Bay OCGT']
        self.plant_db = self.plant_db[~self.plant_db['Name'].isin(['Baglan Bay OCGT','Drax GT','West Burton GT',
                                                                   'Coolkeeragh OCGT','Aberthaw GT','Didcot GT',
                                                                   'Little Barford GT', 'Fiddler’s Ferry GT',
                                                                   'Keadby GT', "Grain GT", 'Ratcliffe GT'])]


pp_dat = UKPlants("/Users/b1017579/Documents/PhD/Projects/10. ELECSIM/10. ELECSIM/data/Power_Plants/No_Location/power_plants_removed_location.csv")
# plant_db = pp_dat.remove_black_start_motors()

plant_db = pp_dat.modify_plant_db()
plant_db.to_csv('/Users/b1017579/Documents/PhD/Projects/10. ELECSIM/10. ELECSIM/data/Power_Plants/No_Location/power_plant_db_with_simplified_type.csv')
