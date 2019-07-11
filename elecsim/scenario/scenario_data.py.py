import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
from elecsim.constants import ROOT_DIR, KW_TO_MW

"""scenario_data.py: Scenario file containing data for a single simulation run."""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"


# Demand per segment of load duration function
segment_demand_diff = [17568, 21964, 23127, 24327, 25520, 26760, 27888, 28935, 29865, 30721, 31567, 32315, 33188, 34182, 35505, 37480, 39585, 42206, 45209, 52152]
segment_demand = [52152, 45209, 42206, 39585, 37480, 35505, 34182, 33188, 32315, 31567, 30721, 29865, 28935, 27888, 26760, 25520, 24327, 23127, 21964, 17568]
# Time of load duration function
segment_time = [8752.5, 8291.83, 7831.17, 7370.5, 6909.92, 6449.25, 5988.58, 5527.92, 5067.25, 4606.58, 4146, 3685.33, 3224.67, 2764, 2303.33, 1842.67, 1382.08, 921.42, 460.75, 0.08]

# Change in load duration function by year
# yearly_demand_change = [1.00, 1.01, 1.02, 1.01, 1.02, 1.02, 1.03, 1.02, 1.01, 1.02, 0.99, 1, 1, 1, 1.01, 1.02, 1.01, 1.01, 1, 1, 1.01, 1, 1.01, 1.01, 1, 1.01, 1.01, 1, 1.01, 1.01, 1, 1.01, 1.01, 1, 1.01, 1.01, 1, 1.01, 1.01, 1, 1.01, 1.01, 1, 1.01, 1.01, 1, 1.01, 1.01, 1, 1.01, 1.01, 1, 1.01, 1.01, 1, 1.01, 1.01, 1, 1.01, 1.01, 1, 1.01]
<<<<<<< HEAD
yearly_demand_change = [1.00]*100
=======
yearly_demand_change = [1.02]*100
>>>>>>> 5f3c373861c398621fed06ebb3fe989ceb1733a9

multi_year_data = pd.read_csv('{}/data/processed/multi_day_data/8_medoids.csv'.format(ROOT_DIR))
multi_year_data_scaled = pd.read_csv('{}/data/processed/multi_day_data/8_medoids_scaled.csv'.format(ROOT_DIR))
# Fuel prices (£/MWh)

# Historical fuel prices of coal, oil and gas  Source: Average prices of fuels purchased by the major UK power producers, BEIS UK Government, table_321.xlsx
historical_fuel_prices_long = pd.read_csv('{}/data/processed/fuel/fuel_costs/historical_fuel_costs/historical_fuel_costs_converted_long.csv'.format(ROOT_DIR))
historical_fuel_prices_mw = pd.read_csv('{}/data/processed/fuel/fuel_costs/historical_fuel_costs/fuel_costs_per_mwh.csv'.format(ROOT_DIR))

# Future fuel prices
gas_price = [KW_TO_MW * 0.01909] * 60  # Source: Average prices of fuels purchased by the major UK power producers: table_321.xls
coal_price = [KW_TO_MW * 0.01106] * 60  # Source: Average prices of fuels purchased by the major UK power producers: table_321.xls
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
fuel_prices = fuel_prices.melt(id_vars=['Fuel'], var_name='Year', value_vars=list(fuel_prices.loc[:,'1990':'2078'].columns))
fuel_prices.Year = pd.to_numeric(fuel_prices.Year)
# Fill NA's with average of group
fuel_prices['value'] = fuel_prices.groupby("Fuel")['value'].transform(lambda x: x.fillna(x.mean()))


# Weighted Cost of Capital
nuclear_wacc = 0.1  # https://www.imperial.ac.uk/media/imperial-college/research-centres-and-groups/icept/Cost-estimates-for-nuclear-power-in-the-UK.pdf (page 20). # Post tax
non_nuclear_wacc = 0.059  # https://assets.kpmg/content/dam/kpmg/ch/pdf/cost-of-capital-study-2017-en.pdf # post tax

# Availability
non_fuel_plant_availability = 0.97
pv_availability = 0.995 # https://ieeexplore.ieee.org/document/7355976
offshore_availability = 0.95 # https://pureportal.strath.ac.uk/files-asset/43185998/Carroll_etal_EWEA2015_availability_improvements_from_condition_monitoring_systems.pdf
onshore_availability = 0.97 # https://pureportal.strath.ac.uk/files-asset/43185998/Carroll_etal_EWEA2015_availability_improvements_from_condition_monitoring_systems.pdf
fuel_plant_availability = 0.97 # Electricity Generation Costs and Hurdle Rates - Leigh_Fisher_Non-renewable_Generation_Cost.pdf


# Capacity factor data (from https://www.renewables.ninja/)
# Wind
wind_capacity_factor = pd.read_csv('{}/data/processed/capacity_factor/Wind/ninja_wind_country_GB_current-merra-2_corrected.csv'.format(ROOT_DIR))
# wind_capacity_factor.time = pd.to_datetime(wind_capacity_factor.time)
# Solar
solar_capacity_factor = pd.read_csv('{}/data/processed/capacity_factor/Solar/ninja_pv_country_GB_merra-2_corrected.csv'.format(ROOT_DIR))
# Hydro
hydro_capacity_factor = 0.456 # http://www.osemosys.org/uploads/1/8/5/0/18504136/hydropower.pdf

# Availability factors (from Source: AESO 2017 Annual Market Statistics)
historical_availability_factor = pd.read_csv('{}/data/processed/availability_factor/historical_availability_factor.csv'.format(ROOT_DIR))

# UK Hourly Demand
historical_hourly_demand = pd.read_csv('{}/data/processed/electricity_demand/uk_all_year_demand.csv'.format(ROOT_DIR))
# historical_hourly_demand = historical_hourly_demand.tail(2628)

# Load duration curve:
load_duration_curve = pd.read_csv('{}/data/processed/load_duration_curve/load_duration_curve.csv'.format(ROOT_DIR))
load_duration_curve_diff = pd.read_csv('{}/data/processed/load_duration_curve/load_duration_curve_difference.csv'.format(ROOT_DIR))

# Learning rate for renewables
learning_rate = 0.5

# Generator Companies imported from Government data files
power_plants = pd.read_csv('{}/data/processed/power_plants/uk_power_plants/uk_power_plants.csv'.format(ROOT_DIR), dtype={'Start_date': int})
# power_plants = power_plants[:100]
modern_plant_costs = pd.read_csv('{}/data/processed/power_plants/power_plant_costs/modern_power_plant_costs/power_plant_costs_with_simplified_type.csv'.format(ROOT_DIR))

power_plant_historical_costs_long = pd.read_csv('{}/data/processed/power_plants/power_plant_costs/historical_power_plant_costs/historical_power_plant_costs_long.csv'.format(ROOT_DIR))

# Variable operation and maintenance costs random numbers for stochasticity (uniform distribution)
o_and_m_multiplier = (0.3, 2)

# Historical power plant efficiency
historical_fuel_plant_efficiency = pd.read_csv('{}/data/processed/power_plants/power_plant_costs/historical_power_plant_costs/efficiency/historical_fuel_plant_efficiency.csv'.format(ROOT_DIR))  # https://www.eia.gov/electricity/annual/html/epa_08_01.html, U.S. Energy Information Administration, Form EIA-923, "Power Plant Operations Report," and predecessor form(s) including U.S. Energy Information Administration, Form EIA-906, "Power Plant Report;" and Form EIA-920, "Combined Heat and Power Plant Report;" Form EIA-860, "Annual Electric Generator Report."


# Company financials
company_financials = pd.read_csv('{}/data/processed/companies/company_financials.csv'.format(ROOT_DIR))

# Bid mark-up price
bid_mark_up = 1.0


# Carbon price - Forecast used from BEIS Electricity Generation Report - Page 10 - Includes forecast for carbon tax and EU ETS
# carbon_price_scenario = [18.00, 19.42, 20.83, 22.25, 23.67, 25.08, 26.50, 27.92, 29.33, 30.75, 32.17, 33.58, 35.00, 43.25, 51.50, 59.75, 68.00, 76.25, 84.50, 92.75, 101.00, 109.25, 117.50, 125.75, 134.00, 142.25, 150.50, 158.75, 167.00, 175.25, 183.50, 191.75, 200.00]
carbon_price_scenario = [10]*1000
# carbon_price_scenario = [0]*100
EU_ETS_COST = 13.62
carbon_price_scenario = [uk_tax + EU_ETS_COST for uk_tax in carbon_price_scenario]


def concatenate_carbon_price():
      carbon_data = {'year': [str(i) for i in range(2019, (2019 + len(carbon_price_scenario)))],
                    'price': carbon_price_scenario}
      carbon_price_scenario_df = pd.DataFrame(carbon_data)
      historical_carbon_price = pd.read_csv(ROOT_DIR + '/data/processed/carbon_price/uk_carbon_tax_historical.csv')
      carbon_cost = historical_carbon_price.append(carbon_price_scenario_df, sort=True)
      carbon_cost.year = pd.to_numeric(carbon_cost.year)
      return carbon_cost


carbon_price_all_years = concatenate_carbon_price()




# Join historical and future carbon prices into dataframe for simulation purposes
# carbon_data = {'year': [str(i) for i in range(2019, (2019 + len(carbon_price_scenario)))], 'price': carbon_price_scenario}
# carbon_price_scenario_df = pd.DataFrame(carbon_data)
# historical_carbon_price = pd.read_csv(ROOT_DIR + '/data/processed/carbon_price/uk_carbon_tax_historical.csv')
# carbon_cost = historical_carbon_price.append(carbon_price_scenario_df, sort=True)
# carbon_cost.year = pd.to_numeric(carbon_cost.year)

# Lost load price - Set at £6000 MW/h as per the recommendations of the UK Government https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/267613/Annex_C_-_reliability_standard_methodology.pdf
<<<<<<< HEAD
# lost_load = 6000
lost_load = 300
=======
lost_load = 6000
# lost_load = 200
>>>>>>> 5f3c373861c398621fed06ebb3fe989ceb1733a9

upfront_investment_costs = 0.25

years_for_agents_to_predict_forward = 10


max_onshore_capacity = 34000  # 42 million acres (170,000 km^2) of agricultural land in UK, 10% dedicated to wind with average energy density of 2W/m^2 David McKay, http://www.withouthotair.com/cft.pdf),
max_offshore_capacity = 1  #
max_pv_capacity = 85000  # 10W/m^2 (David McKay), cover 5% of the UK

# Predict lost load through exponential and linear regression
lost_load_price_predictor = True
