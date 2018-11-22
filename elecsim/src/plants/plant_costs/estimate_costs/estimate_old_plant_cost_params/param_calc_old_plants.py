

class OldPlantCosts():
    """
    Class which takes LCOE values and type of power plants from retrospective database and predicts
    more detailed cost parameters using the same proportions as the BEIS Power Plant Cost Database.
    Specifically uses 2018 power plants from BEIS Power Plant Cost Database.
    """
    def __init__(self, lcoe, type):
        self.lcoe = lcoe
        self.type = type

    def predict_capex_spend(self):
        pass

    def predict_opex_spend(self):
        pass

