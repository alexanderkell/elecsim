import pandas as pd


def power_plant_import(data):
    """

    :param data: Power Plant data - Dataframe should be of the form: Company (String), Name of power station (String), Fuel type (String), Capacity (float), Build date (int))
    :return: Null
    """
    print(data['Company'].unique())


def company_names(data):
    """
    Function that takes a dataframe of power plants and returns company name. Used for
    :param data: Power Plant data - Dataframe should be of the form: Company (String), Name of power station (String), Fuel type (String), Capacity (float), Build date (int))
    :return: unique names
    """
    names = data['Company'].unique()
    return names

pp = pd.read_csv("/Users/b1017579/Documents/PhD/Projects/6. Agent Based Models/1. elecsim/elecsim/data/Power Plants/No Location/power_plants_2018.csv")

print(pp.groupby('Fuel').count())
print("---------")
print(pp.groupby('Fuel').sum().sort_values(['Capacity'], ascending=0))


