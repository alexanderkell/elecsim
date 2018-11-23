import pandas as pd

from elecsim.constants import ROOT_DIR

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

# Fuel prices (£/MWh)

KW_TO_MW_CONV = 1000
historical_fuel_prices = pd.read_csv('{}/data/fuel_data/Fuel costs/historical_fuel_costs/historical_fuel_costs_converted.csv'.format(ROOT_DIR))
gas_prices = [KW_TO_MW_CONV*0.018977] * 42 # Source: Average prices of fuels purchased by the major UK power producers: table_321.xls
coal_price = [KW_TO_MW_CONV*0.00906] * 42 # Source: Average prices of fuels purchased by the major UK power producers: table_321.xls
uranium_price = [KW_TO_MW_CONV*0.0039] * 42 # Source: The Economics of Nuclear Power: EconomicsNP.pdf
oil_price = [KW_TO_MW_CONV*0.02748] * 42 # Source: Average prices of fuels purchased by the major UK power producers: table_321.xls
diesel_price = [KW_TO_MW_CONV*0.1] * 42 # Source: https://www.racfoundation.org/data/wholesale-fuel-prices-v-pump-prices-data
woodchip_price = [KW_TO_MW_CONV*0.0252] * 42 # Source: Biomass for Power Generation: IRENA BiomassCost.pdf
poultry_litter_price = [KW_TO_MW_CONV*0.01139] * 42 # Source: How much is poultry litter worth?: sp06ca08.pdf
straw_price = [KW_TO_MW_CONV*0.016488] * 42 # Source: https://dairy.ahdb.org.uk/market-information/farm-expenses/hay-straw-prices/#.W6JnFJNKiYU
meat_price = [KW_TO_MW_CONV*0.01] * 42 # Assumption: Low price due to plant_type being a waste product
waste_price_post_2000 = [KW_TO_MW_CONV*-0.0252] * 42 # Source: Gate fees report 2017 Comparing the costs of waste treatment options: Gate Fees report 2017_FINAL_clean.pdf
waste_price_pre_2000 = [KW_TO_MW_CONV*-0.01551] * 42 # Source: Gate fees report 2017 Comparing the costs of waste treatment options: Gate Fees report 2017_FINAL_clean.pdf



# Generator Companies imported from Government database
power_plants = pd.read_csv(ROOT_DIR+'/data/Power_Plants/No_Location/power_plant_db_with_simplified_type.csv')

power_plant_costs = pd.read_csv(ROOT_DIR+'/data/Power_Plants/Power_Plant_Costs/Power_Plant_Costs_CSV/power_plant_costs_with_simplified_type.csv')

power_plant_historical_costs = pd.read_csv(ROOT_DIR+'/data/Power_Plants/Power_Plant_Costs/historical_costs/historical_power_plant_costs_long.csv')

# Initial money of generating companies
starting_money_of_gencos = [100000,2000000,300000]

# Carbon price - Forecast used from BEIS Electricity Generation Report - Page 10 - Includes forecast for carbon tax and EU ETS
carbon_price = [18.00, 19.42, 20.83, 22.25, 23.67, 25.08, 26.50, 27.92, 29.33, 30.75, 32.17, 33.58, 35.00, 43.25, 51.50, 59.75, 68.00, 76.25, 84.50, 92.75, 101.00, 109.25, 117.50, 125.75, 134.00, 142.25, 150.50, 158.75, 167.00, 175.25, 183.50, 191.75, 200.00]

# Lost load price - Set at £6000 MW/h as per the recommendations of the UK Government https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/267613/Annex_C_-_reliability_standard_methodology.pdf
lost_load = 6000

