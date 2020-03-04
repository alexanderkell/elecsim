import numpy as np
import numpy.random as ra
"""
File name: inverse_transform_sampling
Date created: 10/01/2019
Feature: # Generate random numbers from a custom distribution
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"


def sample_from_custom_distribution(count, division, n_samples):
    prob = [c/sum(count) for c in count]
    prob_sum = np.cumsum(prob)
    N=n_samples
    R=ra.uniform(0, 1, N)

    prob_sum = np.array(prob_sum)
    division = np.array(division)

    generate_points = [division[np.argwhere(prob_sum == min(prob_sum[(prob_sum - r) > 0]))][0][0] for r in R]
    if n_samples > 1:
        return generate_points
    elif n_samples == 1:
        return generate_points[0]
