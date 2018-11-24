from elecsim.src.plants.plant_type.fuel_plant import FuelPlant
from elecsim.src.plants.plant_type.no_fuel_plant import NoFuelPlant


def plant_registry(requires_fuel):
    """
    Power Plant Registry which takes a boolean variable on whether a plant requires plant_type and returns object of type
    either FuelPlant or RenewablePlant

    :param requires_fuel: Boolean on whether the power plant requires plant_type or not
    :return: Object of type of power plant
    """

    if not isinstance(requires_fuel, bool):
        # print("is not bool")
        raise ValueError("Must enter a boolean for plant_registry function.")

    if not requires_fuel:
        return NoFuelPlant
    elif requires_fuel:
        return FuelPlant


def plant_type_to_if_fuel(plant_type):
    """
    Takes a plant_type type and returns a boolean specifying whether the power plant uses fuel or not.
    :param plant_type: Type of plant
    :return: Boolean specifying whether plant requires plant_type or not
    """
    plant_type = plant_type.lower()
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

