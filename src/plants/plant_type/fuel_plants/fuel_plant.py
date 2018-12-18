from src.plants.plant_type.power_plant import PowerPlant
from src.plants.fuel.fuel_registry.fuel_registry import fuel_registry, plant_type_to_fuel


""" fuel_plant.py: Child class of power plant which contains functions for a power plant which consumes fuel.
                    Most notably, the functinos contain the ability to calculate the cost of fuel.
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"


class FuelPlant(PowerPlant):

    def __init__(self, name, plant_type, capacity_mw, construction_year, average_load_factor, efficiency, pre_dev_period, construction_period, operating_period, pre_dev_spend_years, construction_spend_years, pre_dev_cost_per_mw, construction_cost_per_mw, infrastructure, fixed_o_and_m_per_mw, variable_o_and_m_per_mwh, insurance_cost_per_mw, connection_cost_per_mw):
        """
        Initialisation of plant_type power plant object.
        :param efficiency: Efficiency of power plant at converting plant_type energy into electrical energy.
        """
        super().__init__(name=name, plant_type=plant_type, capacity_mw=capacity_mw, construction_year=construction_year, average_load_factor=average_load_factor, pre_dev_period=pre_dev_period, construction_period=construction_period, operating_period=operating_period, pre_dev_spend_years=pre_dev_spend_years, construction_spend_years=construction_spend_years, pre_dev_cost_per_mw=pre_dev_cost_per_mw, construction_cost_per_mw=construction_cost_per_mw, infrastructure=infrastructure, fixed_o_and_m_per_mw=fixed_o_and_m_per_mw, variable_o_and_m_per_mwh=variable_o_and_m_per_mwh, insurance_cost_per_mw=insurance_cost_per_mw, connection_cost_per_mw=connection_cost_per_mw)
        self.efficiency = efficiency
        # Finds fuel type of power plant eg. CCGT power plant type returns gas.
        fuel_string = plant_type_to_fuel(plant_type, self.construction_year)
        # Fuel object, containing information on fuel.
        self.fuel = fuel_registry(fuel_string)

        if plant_type in ['Coal', 'Nuclear']:
            self.min_running = 5000
        else:
            self.min_running = 0

        self.capacity_fulfilled = 0



    def __repr__(self):
        return 'PowerPlant({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})'.format(self.name, self.type, self.capacity_mw, self.construction_year, self.average_load_factor, self.pre_dev_period, self.construction_period, self.operating_period, self.pre_dev_spend_years, self.construction_spend_years, self.pre_dev_cost_per_mw, self.construction_cost_per_mw, self._infrastructure, self.fixed_o_and_m_per_mw, self.variable_o_and_m_per_mwh, self.insurance_cost_per_mw, self.connection_cost_per_mw)


