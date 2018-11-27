'''
File name: optimisation_test
Date created: 26/11/2018
Feature: #Enter feature description here
'''

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"

from scipy.optimize import minimize
import numpy as np

a = 1
b = 2
c = 3

def calc(x):
    res = 65*x[0]+74*x[1]+12*x[2]
    return res

cons = [{'type': 'eq', 'fun': lambda x: x[0]/x[1]-a/b},
        {'type': 'eq', 'fun': lambda x: x[1]/x[2]-b/c},
        {'type': 'eq', 'fun': lambda x: calc(x)-600}]

start_pos = np.ones(3)*(1/6.)

print(minimize(calc, x0=start_pos, constraints=cons))


