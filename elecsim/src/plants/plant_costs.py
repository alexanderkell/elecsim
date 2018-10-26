import pandas as pd


def plant_costing(fuel, capacity, start_date):
    """
    Function which estimates load factor, efficiency, pre-development costs and period, construction period and costs,
    operating period, infrastructure costs, fixed and variable operating costs and connection and use of system charges.
    :param fuel: Fuel which the plant uses
    :param capacity: Maximum capacity of power plant in MW
    :param start_date: Year that plant begins operation
    :return: Returns array of plant characteristics including time periods and construction costs
    """

    costs = pd.read_csv("../../../data/Power_Plants/Power_Plant_costs/plant_costs_data.csv")

    print(costs.head())

plant_costing("Gas", 1200, 2015)
