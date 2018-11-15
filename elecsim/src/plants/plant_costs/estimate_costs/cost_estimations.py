import pandas as pd
from scipy.interpolate import interp1d

class ExtrapolateInterpolate:

    def __init__(self, x, y):
        """
        Interpolate and extrapolate a 1-D function.

        `x` and `y` are arrays of values used to approximate a function. This class returns a function whose call
        method uses interpolation and extrapolation to find the new points. The extrapolation is completed by
        choosing the last known data point (either maximum point in list, or minimum)
        :param x: array like X axis
        :param y: array like Y axis. The length of y must be the same as the length of x
        """
        self.x = x
        self.y = y

        if len(self.x) != len(self.y):
            ValueError("The x axis and y axis must be of the same size.")

    def __call__(self, point):
        """
        Function which extrapolates and interpolates from known data. Use of linear interpolation between known
        points, and last known data point for extrapolation.
        :param point (int): Cost variable to be extrapolated/interpolated.
        :return (int): Returns extrapolated/interpolated cost of cost variable
        """

        if point <= min(self.x):
            return self.y.iloc[0]
            # return var_req[cost_var_wanted].iloc[0]
        elif point >= max(self.x):
            return self.y.iloc[-1]
        else:
            interp = interp1d(self.x, self.y)
            return interp(point)


df = pd.DataFrame({'Year':[1981, 1984, 1989, 1992],
                   'lcoe':[177.19296, 102.93248, 80.01536, 89.86624]})

print(ExtrapolateInterpolate(df.Year, df.lcoe)(1987))

