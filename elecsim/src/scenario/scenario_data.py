import pandas as pd

"""scenario_data.py: Scenario file containing data for a single simulation run."""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"


# Demand per segment of load duration function
segment = [17568, 4396, 1163, 1200, 1193, 1240, 1128, 1047, 930, 856, 846, 748, 873, 994, 1323, 1975, 2105, 2621, 3003, 6943]

# Time of load duration function
segment_time = [8752.5, 8291.833333333332, 7831.166666666666, 7370.5, 6909.916666666666, 6449.25, 5988.5833333333, 5527.916666666666, 5067.25, 4606.583333333333, 4146, 3685.33333333333, 3224.6666666666665, 2764, 2303.333333333333, 1842.6666666666665, 1382.0833333333333, 921.4166666666666, 460.75, 0.08333333333333333]

# Change in load duration function by year
yearly_demand_change = [1.00, 1.01, 1.02, 1.01, 1.02, 1.02, 1.03, 1.02, 1.01, 1.02, 0.99, 1, 1, 1, 1.01, 1.02, 1.01, 1.01, 1, 1]

# Gas prices (£/kWh)
gas_prices = [0.018977] * 42


# Number of generator companies
# number_of_gencos = 3

# Generator Company initial power generators owned
# generators_owned = [[Nuclear(), Nuclear(), Nuclear()],[Nuclear(),Nuclear()],[Nuclear()]]

# Generator Companies imported from Government database

power_plants = pd.read_csv("/Users/b1017579/Documents/PhD/Projects/6. Agent Based Models/1. elecsim/elecsim/data/Power Plants/power_plants_2018.csv")


# Initial money of generating companies
starting_money_of_gencos = [100000,2000000,300000]

# Carbon price - Forecast used from BEIS Electricity Generation Report - Page 10 - Includes forecast for carbon tax and EU ETS
carbon_price = [18.00, 19.42, 20.83, 22.25, 23.67, 25.08, 26.50, 27.92, 29.33, 30.75, 32.17, 33.58, 35.00, 43.25, 51.50, 59.75, 68.00, 76.25, 84.50, 92.75, 101.00, 109.25, 117.50, 125.75, 134.00, 142.25, 150.50, 158.75, 167.00, 175.25, 183.50, 191.75, 200.00]

# Lost load price
lost_load = 100

