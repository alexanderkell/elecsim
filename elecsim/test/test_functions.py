# from elecsim.src.plants.power_plant import PowerPlant

import elecsim.src.plants.plant_type.fuel_plant as fuel_plant
import elecsim.src.scenario.scenario_data as scenario
import elecsim.src.plants.plant_type.fuel as fuel


plant = fuel_plant.FuelPlant(name="Keadby", plant_type="CCGT H Class", capacity_mw=1200, load_factor=0.93, efficiency=0.54, pre_dev_period=2, construction_period=3, operating_period=25, pre_dev_spend_years=[0.44, 0.44, 0.12], construction_spend_years=[0.4, 0.4, 0.2], pre_dev_cost_per_kw=10, construction_cost_per_kw=500, infrastructure=15100, fixed_o_and_m_per_mw=12200, variable_o_and_m_per_mwh=3, insurance_cost_per_kw=2100, connection_cost_per_kw=3300, min_running=5000, fuel_type="Gas")

print(plant.calculate_lcoe())
