import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
from constants import ROOT_DIR, KW_TO_MW

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

# Historical fuel prices of coal, oil and gas  Source: Average prices of fuels purchased by the major UK power producers, BEIS UK Government, table_321.xlsx
historical_fuel_prices_long = pd.read_csv('{}/data/processed/fuel/fuel_costs/historical_fuel_costs/historical_fuel_costs_converted_long.csv'.format(ROOT_DIR))
historical_fuel_prices_mw = pd.read_csv('{}/data/processed/fuel/fuel_costs/historical_fuel_costs/fuel_costs_per_mwh.csv'.format(ROOT_DIR))

# User input of future fuel prices
gas_price = [KW_TO_MW * 0.018977] * 60  # Source: Average prices of fuels purchased by the major UK power producers: table_321.xls
coal_price = [KW_TO_MW * 0.00906] * 60  # Source: Average prices of fuels purchased by the major UK power producers: table_321.xls
uranium_price = [KW_TO_MW * 0.0039] * 60  # Source: The Economics of Nuclear Power: EconomicsNP.pdf
oil_price = [KW_TO_MW * 0.02748] * 60  # Source: Average prices of fuels purchased by the major UK power producers: table_321.xls
diesel_price = [KW_TO_MW * 0.1] * 60  # Source: https://www.racfoundation.org/data/wholesale-fuel-prices-v-pump-prices-data
woodchip_price = [KW_TO_MW * 0.0252] * 60  # Source: Biomass for Power Generation: IRENA BiomassCost.pdf
poultry_litter_price = [KW_TO_MW * 0.01139] * 60  # Source: How much is poultry litter worth?: sp06ca08.pdf
straw_price = [KW_TO_MW * 0.016488] * 60  # Source: https://dairy.ahdb.org.uk/market-information/farm-expenses/hay-straw-prices/#.W6JnFJNKiYU
meat_price = [KW_TO_MW * 0.01] * 42  # Assumption: Low price due to plant_type being a waste product
waste_price_post_2000 = [KW_TO_MW * -0.0252] * 60  # Source: Gate fees report 2017 Comparing the costs of waste treatment options: Gate Fees report 2017_FINAL_clean.pdf
waste_price_pre_2000 = [KW_TO_MW * -0.01551] * 60  # Source: Gate fees report 2017 Comparing the costs of waste treatment options: Gate Fees report 2017_FINAL_clean.pdf

# Joining historical and future fuel prices for simulation purposes.
fuel_prices = pd.DataFrame(data=[coal_price, oil_price, gas_price, uranium_price, diesel_price, woodchip_price,
                                 poultry_litter_price, straw_price, meat_price, waste_price_post_2000,
                                 waste_price_pre_2000],
                           columns=[str(i) for i in range(2019, (2019+len(gas_price)))])
fuel_prices = pd.concat([historical_fuel_prices_mw, fuel_prices], axis=1)
# Convert from wide to long
fuel_prices = fuel_prices.melt(id_vars=['Fuel'], var_name='Year', value_vars=list(fuel_prices.loc[:,'1990':'2018'].columns))
fuel_prices.Year = pd.to_numeric(fuel_prices.Year)

# Learning rate for renewables
learning_rate = 0.5

# Generator Companies imported from Government data files
power_plants = pd.read_csv('{}/data/processed/power_plants/uk_power_plants/uk_power_plants.csv'.format(ROOT_DIR), dtype={'Start_date': int})
modern_plant_costs = pd.read_csv('{}/data/processed/power_plants/power_plant_costs/modern_power_plant_costs/power_plant_costs_with_simplified_type.csv'.format(ROOT_DIR))

power_plant_historical_costs_long = pd.read_csv('{}/data/processed/power_plants/power_plant_costs/historical_power_plant_costs/historical_power_plant_costs_long.csv'.format(ROOT_DIR))




# Company financials
company_financials = pd.read_csv('{}/data/processed/companies/company_financials.csv'.format(ROOT_DIR))



# Carbon price - Forecast used from BEIS Electricity Generation Report - Page 10 - Includes forecast for carbon tax and EU ETS
carbon_price_scenario = [18.00, 19.42, 20.83, 22.25, 23.67, 25.08, 26.50, 27.92, 29.33, 30.75, 32.17, 33.58, 35.00, 43.25, 51.50, 59.75, 68.00, 76.25, 84.50, 92.75, 101.00, 109.25, 117.50, 125.75, 134.00, 142.25, 150.50, 158.75, 167.00, 175.25, 183.50, 191.75, 200.00]
# Join historical and future carbon prices into dataframe for simulation purposes
carbon_data = {'year': [str(i) for i in range(2019, (2019 + len(carbon_price_scenario)))], 'price': carbon_price_scenario}
carbon_price_scenario_df = pd.DataFrame(carbon_data)
historical_carbon_price = pd.read_csv(ROOT_DIR + '/data/processed/carbon_price/uk_carbon_tax_historical.csv')
carbon_cost = historical_carbon_price.append(carbon_price_scenario_df, sort=True)
carbon_cost.year = pd.to_numeric(carbon_cost.year)

# Lost load price - Set at £6000 MW/h as per the recommendations of the UK Government https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/267613/Annex_C_-_reliability_standard_methodology.pdf
lost_load = 6000

