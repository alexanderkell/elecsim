from scipy.interpolate import interp1d

class predict_point():
    def __init__(self, plant_size, cost_var):
        self.plant_size = plant_size
        self.cost_var = cost_var

    def __call__(self, x_new):
        if type(x_new) == list:
            output = [self.predict(x) for x in x_new]
            return output
        else:
            return self.predict(x_new)

    def predict(self, x_new):
        if(x_new<=min(self.plant_size)):
            return self.cost_var.iloc[0]
        elif(x_new>=max(self.plant_size)):
            return self.cost_var.iloc[-1]
        else:
            interp = interp1d(self.plant_size, self.cost_var)
            return interp(x_new)
