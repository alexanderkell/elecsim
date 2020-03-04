import mysql.connector
from mysql.connector import errorcode

import os.path
import sys
import ray


sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from elecsim.model.world import World
import tracemalloc

import pandas as pd
import linecache

from elecsim.constants import ROOT_DIR
import string
from deap import algorithms
from deap import base
from deap import benchmarks
from deap.benchmarks.tools import diversity, convergence, hypervolume
from deap import creator
from deap import tools

import array
import random
import logging
logger = logging.getLogger(__name__)
import numpy as np
import numpy

from scoop import futures

from pebble import ProcessPool
from concurrent.futures import TimeoutError

import time
from pathlib import Path
project_dir = Path("__file__").resolve().parents[1]
import string
import random


import array
import random
import json

import numpy

from math import sqrt

from deap import algorithms
from deap import base
from deap import benchmarks
from deap.benchmarks.tools import diversity, convergence, hypervolume
from deap import creator
from deap import tools

creator.create("FitnessMin", base.Fitness, weights=(-1.0, -1.0))
creator.create("Individual", array.array, typecode='d', fitness=creator.FitnessMin)

@ray.remote(num_return_vals=2)
def world_eval(individual, carbon_policy):
    beis_params = [0.00121256259168, 46.850377392563864, 0.0029982421515, 28.9229765616468, 0.00106156336814, 18.370337670063762, 0.00228312539654, 0.0, 0.0024046471141100003, 34.43480109190594, 0.0, -20.88014916953091, 0.0, 8.15032953348701, 0.00200271495761, -12.546185375581802, 0.00155518243668, 39.791132970522796, 0.00027449937576, 8.42878689508516, 0.00111989525697, 19.81640207212787, 0.00224091998324, 5.26288570922149, 0.00209189353332, -5.9117317131295195, 0.00240696026847, -5.0144941135222, 0.00021183142492999999, -1.29658413335784, 0.00039441444392000004, -11.41659250225168, 0.00039441444392000004, -11.41659250225168, 120.21276910611674, 0.0, 0.00059945111227]
    # beis_params = [0.00121256259168, 46.850377392563864, 0.0029982421515, 28.9229765616468, 0.00106156336814, 18.370337670063762, 0.00228312539654, 0.0, 0.0024046471141100003, 34.43480109190594, 0.0, -20.88014916953091, 0.0, 8.15032953348701, 0.00200271495761, -12.546185375581802, 0.00155518243668, 39.791132970522796, 0.00027449937576, 8.42878689508516, 0.00111989525697, 19.81640207212787, 0.00224091998324, 5.26288570922149, 0.00209189353332, -5.9117317131295195, 0.00240696026847, -5.0144941135222, 0.00021183142492999999, -1.29658413335784, 0.00039441444392000004, -11.41659250225168, 0.0021988838824299997, 12.633572943294599, 120.21276910611674, 0.0, 0.00059945111227]

    prices_individual = np.array(beis_params[:-3]).reshape(-1, 2).tolist()

    MARKET_TIME_SPLICES = 8
    YEARS_TO_RUN = 17
    number_of_steps = YEARS_TO_RUN * MARKET_TIME_SPLICES

    scenario_2018 = "{}/../run/beis_case_study/scenario/reference_scenario_2018.py".format(ROOT_DIR)

    # if individual[0] == 1:
    #     individual = [individual[1]*i + individual[2] for i in range(1, 20)]
    # else:
    #     individual = [individual[3]*i ** individual[4] + individual[2] for i in range(1, 20)]
    individual = [individual[0]*i + individual[1] for i in range(1, 20)]
    print(individual)

    world = World(carbon_price_scenario=individual[:-1], initialization_year=2018, scenario_file=scenario_2018, market_time_splices=MARKET_TIME_SPLICES, data_folder="{}_data".format(carbon_policy), number_of_steps=number_of_steps, long_term_fitting_params=prices_individual, highest_demand=63910, nuclear_subsidy=beis_params[-3], future_price_uncertainty_m=beis_params[-2], future_price_uncertainty_c=beis_params[-1])
    for _ in range(YEARS_TO_RUN):
        for i in range(MARKET_TIME_SPLICES):
            # try:
            if i/8 == 0:
                print('end of year')

            average_electricity_price, carbon_emitted = world.step()
            # except Exception as e:
            #     print("try catch error: \n{}".format(e))
            #     return 889999999999999999, 889999999999999999
            # if carbon_emitted is bool:
            if isinstance(carbon_emitted, bool):
                print("carbon emitted error")
                return 999999999999999999, 999999999999999999

            if not isinstance(average_electricity_price, float):
                print("average_electricity_price {}, type {}".format(average_electricity_price, type(average_electricity_price)))
                average_electricity_price = 779999999999999999
            if not isinstance(carbon_emitted, float):
                print("carbon_emitted {}, type {}".format(carbon_emitted, type(carbon_emitted)))
                carbon_emitted = 779999999999999999

    print("average_electricity_price: {}, carbon_emitted: {}".format(average_electricity_price, carbon_emitted))
    return average_electricity_price, carbon_emitted
toolbox = base.Toolbox()

# Problem definition
# Functions zdt1, zdt2, zdt3, zdt6 have bounds [0, 1]
BOUND_LOW, BOUND_UP = 0, 250

# Functions zdt4 has bounds x1 = [0, 1], xn = [-5, 5], with n = 2, ..., 10
# BOUND_LOW, BOUND_UP = [0.0] + [-5.0]*9, [1.0] + [5.0]*9

# Functions zdt1, zdt2, zdt3 have 30 dimensions, zdt4 and zdt6 have 10
NDIM = 19

def uniform(low, up, size=None):
    try:
        return [random.uniform(a, b) for a, b in zip(low, up)]
    except TypeError:
        return [random.uniform(a, b) for a, b in zip([low] * size, [up] * size)]
#



# toolbox.register("attr_float", uniform, BOUND_LOW, BOUND_UP, NDIM)

# toolbox.register("attr_function", random.randint, 0, 1)
toolbox.register("attr_m", random.uniform, -14, 14)
toolbox.register("attr_c", random.uniform, 0, 250)

# toolbox.register("attr_L", random.uniform, -10, 10)
# toolbox.register("attr_k", random.uniform, 1, 14)
# toolbox.register("attr_n", random.uniform, 0, 250)
# toolbox.register("individual", tools.initCycle, creator.Individual, (toolbox.attr_function, toolbox.attr_m, toolbox.attr_c, toolbox.attr_a, toolbox.attr_d), n=1)
toolbox.register("individual", tools.initCycle, creator.Individual, (toolbox.attr_m, toolbox.attr_c), n=1)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", world_eval)
# toolbox.register("mate", tools.cxSimulatedBinaryBounded, low=BOUND_LOW, up=BOUND_UP, eta=20.0)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selNSGA2)
toolbox.register("map_distributed", futures.map)


config = {
  'host':'elecsimresults2.mysql.database.azure.com',
  'user':'alexkell@elecsimresults2',
  'password':'b3rz0s4m4dr1dth3h01113s!',
  'database':'carbonoptimiser',
  'ssl_ca':'run/validation-optimisation/database/BaltimoreCyberTrustRoot.crt.pem'
  # 'ssl_ca':'/Users/b1017579/Documents/PhD/Projects/10-ELECSIM/run/validation-optimisation/database/BaltimoreCyberTrustRoot.crt.pem'

}


def main(seed=None):
    random.seed(seed)

    NGEN = 999
    # MU = 120
    MU = 80
    # MU = 4
    CXPB = 0.9

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    # stats.register("avg", numpy.mean, axis=0)
    # stats.register("std", numpy.std, axis=0)
    stats.register("min", numpy.min, axis=0)
    stats.register("max", numpy.max, axis=0)

    logbook = tools.Logbook()
    logbook.header = "gen", "evals", "std", "min", "avg", "max"

    pop = toolbox.population(n=MU)

    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in pop if not ind.fitness.valid]
    fitnesses = toolbox.map_distributed(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    # This is just to assign the crowding distance to the individuals
    # no actual selection is done
    pop = toolbox.select(pop, len(pop))

    record = stats.compile(pop)
    logbook.record(gen=0, evals=len(invalid_ind), **record)
    print(logbook.stream)

    # Begin the generational process
    for gen in range(1, NGEN):
        # Vary the population
        offspring = tools.selTournamentDCD(pop, len(pop))
        offspring = [toolbox.clone(ind) for ind in offspring]

        for ind1, ind2 in zip(offspring[::2], offspring[1::2]):
            if random.random() <= CXPB:
                toolbox.mate(ind1, ind2)

            toolbox.mutate(ind1)
            toolbox.mutate(ind2)
            del ind1.fitness.values, ind2.fitness.values

        # Recalculate all individual due to stochastic nature of simulation
        for ind in offspring:
            del ind.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map_distributed(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # Select the next generation population
        pop = toolbox.select(pop + offspring, MU)
        record = stats.compile(pop)
        logbook.record(gen=gen, evals=len(invalid_ind), **record)
        print(logbook.stream)

        front = numpy.array(
            [ind.fitness.values + tuple(ind) for ind in pop])

        print("front: {}".format(front))

        try:
            conn = mysql.connector.connect(**config)
            print("Connection established")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with the user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            cursor = conn.cursor()

        # first_part = 'INSERT INTO carbon_results (reward,carbon_1,carbon_2,carbon_3,carbon_4,carbon_5,carbon_6,carbon_7,carbon_8,carbon_9,carbon_10,carbon_11,carbon_12,carbon_13,carbon_14,carbon_15,carbon_16,carbon_17,carbon_18) VALUES '
        #
        # insert_vars = "".join(["({},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}),\n".format(ind.flat[0], ind.flat[1], ind.flat[2], ind.flat[3], ind.flat[4], ind.flat[5], ind.flat[6], ind.flat[7], ind.flat[8], ind.flat[9], ind.flat[10], ind.flat[11], ind.flat[12], ind.flat[13], ind.flat[14], ind.flat[15], ind.flat[16], ind.flat[17], ind.flat[18]) for ind in front])

        # first_part = 'INSERT INTO carbon_results_function (average_electricity_price,carbon_emitted,attr_function,attr_m,attr_c,attr_a,attr_d) VALUES '
        #
        # insert_vars = "".join(["({},{},{},{},{},{},{}),\n".format(ind.flat[0], ind.flat[1], ind.flat[2], ind.flat[3], ind.flat[4], ind.flat[5], ind.flat[6]) for ind in front])
        first_part = 'INSERT INTO carbon_results_function (average_electricity_price,carbon_emitted,attr_m,attr_c) VALUES '

        insert_vars = "".join(["({},{},{},{}),\n".format(ind.flat[0], ind.flat[1], ind.flat[2], ind.flat[3]) for ind in front])



        insert_cmd = first_part+insert_vars
        insert_cmd = insert_cmd[:-2]
        # print("command: {}".format(insert_cmd))

        cursor.execute(insert_cmd)
        conn.commit()
        cursor.close()
        conn.close()


    print("Final population hypervolume is %f" % hypervolume(pop, [11.0, 11.0]))

    return pop, logbook

if __name__ == "__main__":
    # with open("pareto_front/zdt1_front.json") as optimal_front_data:
    #     optimal_front = json.load(optimal_front_data)
    # Use 500 of the 1000 points in the json file
    # optimal_front = sorted(optimal_front[i] for i in range(0, len(optimal_front), 2))

    # pop, stats = main()

    # #lowest
    # world_eval([11.384098, 81.34436])
    #
    # #highest
    # world_eval([11.384098, 202.53813])
    #
    # #flat
    # world_eval([-0.2289701, 192.5701])

    def world_eval_parallel(params, strategy):
        output1, output2 = [], []

        # Launch the tasks.
        for j in range(100):
            id1, id2 = world_eval.remote(params, strategy)
            output1.append(id1)
            output2.append(id2)

        # Block until the results have finished and get the results.
        output1 = ray.get(output1)
        output2 = ray.get(output2)

    ray.init(num_cpus=os.cpu_count()-1)
    # world_eval_parallel([11.384098, 81.34436], "lowest")
    # world_eval_parallel([11.384098, 202.53813], "highest")
    world_eval_parallel([-0.2289701, 192.5701], "flat")

