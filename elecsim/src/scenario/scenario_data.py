from elecsim.src.plants.power_plant import PowerPlant
from elecsim.src.plants.nuclear import Nuclear

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

# Number of generator companies
number_of_gencos = 3

# Generator Company initial power generators owned
generators_owned = [[Nuclear(), Nuclear(), Nuclear()],[Nuclear(),Nuclear()],[Nuclear()]]

# Initial money of generating companies
starting_money_of_gencos = [100000,2000000,300000]

# Carbon price floor
cpf = [18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18 ]

# Lost load price
lost_load = 100
