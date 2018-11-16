from elecsim.src.plants.plant_type.fuel_plant import FuelPlant
from elecsim.src.plants.plant_type.zero_fuel_plant import ZeroFuelPlant


def plant_registry(requires_fuel):
    """
    Power Plant Registry which takes a boolean variable on whether a plant requires fuel and returns object of type
    either FuelPlant or RenewablePlant
    :param requires_fuel: Boolean on whether the power plant requires fuel or not
    :return: Object of type of power plant
    """

    if not requires_fuel:
        return ZeroFuelPlant
    elif requires_fuel:
        return FuelPlant


def plant_type_to_fuel_required(plant_type):
    """
    Takes a fuel type and returns a boolean specifying whether the power plant requires fuel or not
    :param plant_type: Type of plant
    :return: Boolean specifying whether plant requires fuel or not
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
















print(plant_registry(plant_type_to_fuel_required("Gas")))
