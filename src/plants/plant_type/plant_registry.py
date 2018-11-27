from src.plants.plant_type.fuel_plant import FuelPlant
from src.plants.plant_type.non_fuel_plant import NoFuelPlant

class PlantRegistry:

    def __init__(self, plant_type):
        self.plant_type = plant_type

    def plant_type_to_fuel(self):
        requires_fuel = self._fuel_or_no_fuel()
        return self._plant_object_registry(requires_fuel)

    def _plant_object_registry(self, requires_fuel):
        """
        Power Plant Registry which takes a boolean variable on whether a plant requires plant_type and returns object of type
        either FuelPlant or RenewablePlant

        :param requires_fuel: Boolean on whether the power plant requires plant_type or not
        :return: Object of type of power plant
        """

        requires_fuel = self._fuel_or_no_fuel()

        if not isinstance(requires_fuel, bool):
            # print("is not bool")
            raise ValueError("Must enter a boolean for plant_registry function.")

        if not requires_fuel:
            return NoFuelPlant
        elif requires_fuel:
            return FuelPlant


    def _fuel_or_no_fuel(self):
        """
        Takes a plant_type type and returns a boolean specifying whether the power plant uses fuel or not.
        :param plant_type: Type of plant
        :return: Boolean specifying whether plant requires plant_type or not
        """
        plant_type = self.plant_type.lower()
        if plant_type == "gas":
            return True
        elif plant_type == "ccgt":
            return True
        elif plant_type == "ccgt":
            return True
        elif plant_type == "coal":
            return True
        elif plant_type == "pv":
            return False
        elif plant_type == "ad":
            return True
        elif plant_type == "act":
            return True
        elif plant_type == "offshore":
            return False
        elif plant_type == "biomass":
            return True
        elif plant_type == "onshore":
            return False
        elif plant_type == "landfill":
            return True
        elif plant_type == "sewage":
            return True
        elif plant_type == "geothermal":
            return False
        elif plant_type == "hydro_store":
            return False
        elif plant_type == "hydro":
            return False
        elif plant_type == "wave":
            return False
        elif plant_type == "tidal":
            return False
        elif plant_type == "ocgt":
            return True
        elif plant_type == "nuclear":
            return False
        elif plant_type == "recip_gas":
            return False
        elif plant_type == "pumped_storage":
            return False
        elif plant_type == "recip_diesel":
            return False
        else:
            raise ValueError("Plant Type not Found: "+plant_type)

