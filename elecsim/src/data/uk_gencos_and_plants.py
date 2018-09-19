import pandas as pd


def power_plant_import(data):
    """

    :param data: Power Plant data - Dataframe should be of the form: Company (String), Name of power station (String), Fuel type (String), Capacity (float), Build date (int))
    :return: Null
    """
    print(data['Company'].unique())


def company_names(data):
    """
    Function that takes a dataframe of power plants and returns company names.
    :param data: Power Plant data - Dataframe should be of the form: Company (String), Name of power station (String), Fuel type (String), Capacity (float), Build date (int))
    :return: unique names
    """
    names = data['Company'].unique()
    return names

def plants_owned(gen_co):
    query = pp.loc[pp['Company'] == gen_co]
    return query


pp = pd.read_csv("/Users/b1017579/Documents/PhD/Projects/6. Agent Based Models/1. elecsim/elecsim/data/Power Plants/No Location/power_plants_2018.csv")

print(pp.groupby('Fuel').count())
print("---------")
print(pp.groupby('Fuel').sum().sort_values(['Capacity'], ascending=0))

print(pp.loc[pp['Fuel']=="Coal"])

# print("Company names")
# print(company_names(pp))

# gencos = company_names(pp)
#
# for i in gencos:
#     print(plants_owned(i))

