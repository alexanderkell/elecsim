

import mysql.connector
from mysql.connector import errorcode

import os.path
import sys


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
import time
from pathlib import Path
project_dir = Path("__file__").resolve().parents[1]
import string
import random

"""
File name: run_GA_price_fitter
Date created: 26/07/2019
Feature: #Enter feature description here
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"

pd.set_option('display.max_rows', 4000)

logging.basicConfig(level=logging.WARNING)


# creator.create("FitnessMin", base.Fitness, weights=(-1.0, -1.0, -1.0))
# creator.create("Individual", array.array, typecode='d',
#                fitness=creator.FitnessMin)
#
# toolbox = base.Toolbox()
#
# # Problem definition
# # Functions zdt1, zdt2, zdt3, zdt6 have bounds [0, 1]
# BOUND_LOW, BOUND_UP = 0.0, 100
#
# # Functions zdt4 has bounds x1 = [0, 1], xn = [-5, 5], with n = 2, ..., 10
# # BOUND_LOW, BOUND_UP = [0.0] + [-5.0]*9, [1.0] + [5.0]*9
#
# # Functions zdt1, zdt2, zdt3 have 30 dimensions, zdt4 and zdt6 have 10
# NDIM = 3 * 12 * 12 + 2
# # NDIM = 3 * 51 + 1
#
#
# def uniform(low, up, size=None):
#     try:
#         return [random.randint(a, b) for a, b in zip(low, up)]
#     except TypeError:
#         return [random.randint(a, b) for a, b in zip([low] * size, [up] * size)]



config = {
  'host':'elecsimresults.mysql.database.azure.com',
  'user':'alexkell@elecsimresults',
  'password':'b3rz0s4m4dr1dth3h01113s!',
  'database':'elecsim',
  'ssl_ca':'run/validation-optimisation/database/BaltimoreCyberTrustRoot.crt.pem'
}




def eval_world(individual):

    # time_start = time.time()
    # for i in range(1000):
    #     pass
    # t1 = time.time()
    #
    # time_taken = t1-time_start
    # return [1], time_taken


    MARKET_TIME_SPLICES = 8
    YEARS_TO_RUN = 6
    number_of_steps = YEARS_TO_RUN * MARKET_TIME_SPLICES

    scenario_2013 = "{}/../run/validation-optimisation/scenario_file/scenario_2013.py".format(ROOT_DIR)

    world = World(initialization_year=2013, scenario_file=scenario_2013, market_time_splices=MARKET_TIME_SPLICES, data_folder="runs_2013", number_of_steps=number_of_steps, fitting_params=[individual[0], individual[1]], highest_demand=63910)
    time_start = time.perf_counter()
    timestamp_start = time.time()
    for i in range(number_of_steps):
        results_df = world.step()
    time_end = time.perf_counter()
    timestamp_end = time.time()

    time_taken = time_end-time_start

    contributed_results = results_df.filter(regex='contributed_').tail(MARKET_TIME_SPLICES)
    contributed_results *= 1/24

    # print("contributed_results: {}".format(contributed_results))
    contributed_results = contributed_results.rename(columns={'contributed_PV': "contributed_solar"})
    cluster_size = pd.Series([22.0, 30.0, 32.0, 35.0, 43.0, 53.0, 68.0, 82.0])

    # contributed_results['cluster_size'] = [22.0, 30.0, 32.0, 35.0, 43.0, 53.0, 68.0, 82.0]

    results_wa = contributed_results.apply(lambda x: np.average(x, weights=cluster_size.values)).to_frame()

    results_wa.index = results_wa.index.str.split("_").str[1].str.lower()
    # print("results_wa: {}".format(results_wa))
    offshore = results_wa.loc["offshore"].iloc[0]
    onshore = results_wa.loc["onshore"].iloc[0]
    # print("offshore: {}".format(offshore))
    # results_wa = results_wa.append(pd.DataFrame({"wind", offshore+onshore}))
    results_wa.loc['wind'] = [offshore+onshore]
    # print("results_wa: {}".format(results_wa))

    electricity_mix = pd.read_csv("{}/data/processed/electricity_mix/energy_mix_historical.csv".format(ROOT_DIR))
    actual_mix_2018 = electricity_mix[electricity_mix.year == 2018]


    actual_mix_2018 = actual_mix_2018.set_index("variable")
    # print(actual_mix_2018)

    joined = actual_mix_2018[['value']].join(results_wa, how='inner')
    # print("joined: \n{}".format(joined))

    joined = joined.rename(columns={'value':'actual', 0:'simulated'})

    joined = joined.loc[~joined.index.str.contains('biomass')]

    # print("joined: \n{}".format(joined))

    joined['actual_perc'] = joined['actual']/joined['actual'].sum()
    joined['simulated_perc'] = joined['simulated']/joined['simulated'].sum()

    # print("joined: \n{}".format(joined))

    total_difference_col = joined['actual_perc'] - joined['simulated_perc']
    # print(total_difference_col)
    total_difference = total_difference_col.abs().sum()
    # print("max_demand : dif: {} :x {}".format(individual, total_difference))
    # print(joined.simulated)
    # print("input: {} {}, returns: {}, {}, {}".format(individual[0], individual[1], [total_difference], time_taken, joined.simulated))
    print("input: {} {}, returns: {}, {}, {}".format(individual[0], individual[1], [total_difference], time_taken, timestamp_start, timestamp_end, joined.simulated))
    return [total_difference], time_taken, timestamp_start, timestamp_end, joined.simulated


# for i in np.linspace(62244, 66326, num=50):
#     eval_world(i)

# eval_world([0.002547, -13.374101])



creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()

# Attribute generator
#                      define 'attr_bool' to be an attribute ('gene')
#                      which corresponds to integers sampled uniformly
#                      from the range [0,1] (i.e. 0 or 1 with equal
#                      probability)
toolbox.register("attr_m", random.uniform, 0.0, 0.004)
toolbox.register("attr_c", random.uniform, -30, 100)

toolbox.register("map_distributed", futures.map)
# Structure initializers
#                         define 'individual' to be an individual
#                         consisting of 100 'attr_bool' elements ('genes')
toolbox.register("individual", tools.initCycle, creator.Individual, (toolbox.attr_m, toolbox.attr_c), 1)

# define the population to be a list of individuals
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


#----------
# Operator registration
#----------
# register the goal / fitness function
toolbox.register("evaluate", eval_world)

# register the crossover operator
toolbox.register("mate", tools.cxTwoPoint)

# register a mutation operator with a probability to
# flip each attribute/gene of 0.05
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)

# operator for selecting individuals for breeding the next
# generation: each individual of the current generation
# is replaced by the 'fittest' (best) of three individuals
# drawn randomly from the current generation.
toolbox.register("select", tools.selTournament, tournsize=3)

#----------

def main():

    # create an initial population of 300 individuals (where
    # each individual is a list of integers)
    pop = toolbox.population(n=150)

    # CXPB  is the probability with which two individuals
    #       are crossed
    #
    # MUTPB is the probability for mutating an individual
    CXPB, MUTPB = 0.5, 0.2

    print("Start of evolution")

    # Evaluate the entire population
    # fitnesses = list(map(toolbox.evaluate, pop))
    fitnesses_and_time = list(toolbox.map_distributed(toolbox.evaluate, pop))
    # fitnesses = [fitness_time[0] for fitness_time in fitnesses_and_time]
    # print(fitnesses_and_time)

    timing_holder = []

    for ind, fit in zip(pop, fitnesses_and_time):
        ind.fitness.values = fit[0]
        timing_holder.append(fit[1])

    print("  Evaluated %i individuals" % len(pop))

    # Extracting all the fitnesses of
    fits = [ind.fitness.values[0] for ind in pop]

    # Variable keeping track of the number of generations
    g = 0

    # Begin the evolution
    while g<1000:

        time_results = {}

        # A new generation
        g = g + 1
        print("-- Generation %i --" % g)

        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(toolbox.map_distributed(toolbox.clone, offspring))

        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):

            # cross two individuals with probability CXPB
            if random.random() < CXPB:
                toolbox.mate(child1, child2)

                # fitness values of the children
                # must be recalculated later
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:

            # mutate an individual with probability MUTPB
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # # fitnesses = list(map(toolbox.evaluate, pop))
        # fitnesses_and_time = list(toolbox.map_distributed(toolbox.evaluate, pop))
        # # fitnesses = [fitness_time[0] for fitness_time in fitnesses_and_time]
        # print(fitnesses_and_time)
        #
        # timing_holder = {}
        #
        # for ind, fit in zip(pop, fitnesses_and_time):
        #     ind.fitness.values = fit[0]
        #     timing_holder[ind[0]] = fit[1]

        timing_holder = []
        time_start_holder = []
        time_end_holder = []
        generators_invested = []

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        # fitnesses = map(toolbox.evaluate, invalid_ind)
        fitnesses = list(toolbox.map_distributed(toolbox.evaluate, invalid_ind))
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit[0]
            timing_holder.append(fit[1])
            time_start_holder.append(fit[2])
            time_end_holder.append(fit[3])
            generators_invested.append(fit[4])

        print("  Evaluated %i individuals" % len(invalid_ind))

        # The population is entirely replaced by the offspring
        pop[:] = offspring

        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in pop]

        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x*x for x in fits)
        std = abs(sum2 / length - mean**2)**0.5

        print("  Min %s" % min(fits))
        print("  Max %s" % max(fits))
        print("  Avg %s" % mean)
        print("  Std %s" % std)

        best_ind = tools.selBest(pop, 1)[0]
        print("Best individual is %s, %s" % (best_ind, best_ind.fitness.values))

        progression = np.array([ind.fitness.values + tuple(ind) for ind in pop])



        # for ind in progression:
        #     print("ind: {}".format(ind))
                # Insert some data into table

                # Connect to MySQL
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

        first_part = 'INSERT INTO validoptimresults (run_number, time_taken, timestamp_start, timestamp_end, reward, individual_m, individual_c, coal, nuclear, ccgt, wind, solar) VALUES '

        insert_vars = "".join(["({},{},{},{},{},{},{},{},{},{},{},{}),\n".format(g, time, time_start, time_end, ind.flat[0], ind.flat[1], ind.flat[2], gen_invested.loc['coal'], gen_invested.loc['nuclear'], gen_invested.loc['ccgt'], gen_invested.loc['wind'], gen_invested.loc['solar']) for ind, time, time_start, time_end, gen_invested in zip(progression, timing_holder, time_start_holder, time_end_holder, generators_invested)])
        insert_cmd = first_part+insert_vars
        insert_cmd = insert_cmd[:-2]

        # print("command: {}".format(insert_cmd))

        cursor.execute(insert_cmd)
        conn.commit()
        cursor.close()
        conn.close()

        # np.savetxt('{}/run/validation-optimisation/data/generations/generation_{}.csv'.format(project_dir, g), progression, delimiter=",")

    print("-- End of (successful) evolution --")

    best_ind = tools.selBest(pop, 1)[0]
    print("Best individual is %s, %s" % (best_ind, best_ind.fitness.values))

if __name__ == "__main__":
    main()


#NSGA-2


# creator.create("FitnessMin", base.Fitness, weights=(-1.0, -1.0))
# creator.create("Individual", array.array, typecode='d', fitness=creator.FitnessMin)
#
# toolbox = base.Toolbox()
#
# # Problem definition
# # Functions zdt1, zdt2, zdt3, zdt6 have bounds [0, 1]
# BOUND_LOW, BOUND_UP = -0.01, 0.01
#
# # Functions zdt4 has bounds x1 = [0, 1], xn = [-5, 5], with n = 2, ..., 10
# # BOUND_LOW, BOUND_UP = [0.0] + [-5.0]*9, [1.0] + [5.0]*9
#
# # Functions zdt1, zdt2, zdt3 have 30 dimensions, zdt4 and zdt6 have 10
# NDIM = 2
#
# def uniform(low, up, size=None):
#     try:
#         return [random.uniform(a, b) for a, b in zip(low, up)]
#     except TypeError:
#         return [random.uniform(a, b) for a, b in zip([low] * size, [up] * size)]
#
# toolbox.register("attr_float", uniform, BOUND_LOW, BOUND_UP, NDIM)
# toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.attr_float)
# toolbox.register("population", tools.initRepeat, list, toolbox.individual)
#
# toolbox.register("evaluate", eval_world)
# toolbox.register("mate", tools.cxSimulatedBinaryBounded, low=BOUND_LOW, up=BOUND_UP, eta=20.0)
# toolbox.register("mutate", tools.mutPolynomialBounded, low=BOUND_LOW, up=BOUND_UP, eta=20.0, indpb=1.0/NDIM)
# toolbox.register("select", tools.selNSGA2)
#
# def main(seed=None):
#     random.seed(seed)
#
#     NGEN = 250
#     MU = 100
#     CXPB = 0.9
#
#     stats = tools.Statistics(lambda ind: ind.fitness.values)
#     # stats.register("avg", numpy.mean, axis=0)
#     # stats.register("std", numpy.std, axis=0)
#     stats.register("min", numpy.min, axis=0)
#     stats.register("max", numpy.max, axis=0)
#
#     logbook = tools.Logbook()
#     logbook.header = "gen", "evals", "std", "min", "avg", "max"
#
#     pop = toolbox.population(n=MU)
#
#     # Evaluate the individuals with an invalid fitness
#     invalid_ind = [ind for ind in pop if not ind.fitness.valid]
#     fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
#     for ind, fit in zip(invalid_ind, fitnesses):
#         ind.fitness.values = fit
#
#     # This is just to assign the crowding distance to the individuals
#     # no actual selection is done
#     pop = toolbox.select(pop, len(pop))
#
#     record = stats.compile(pop)
#     logbook.record(gen=0, evals=len(invalid_ind), **record)
#     print(logbook.stream)
#
#     # Begin the generational process
#     for gen in range(1, NGEN):
#         # Vary the population
#         offspring = tools.selTournamentDCD(pop, len(pop))
#         offspring = [toolbox.clone(ind) for ind in offspring]
#
#         for ind1, ind2 in zip(offspring[::2], offspring[1::2]):
#             if random.random() <= CXPB:
#                 toolbox.mate(ind1, ind2)
#
#             toolbox.mutate(ind1)
#             toolbox.mutate(ind2)
#             del ind1.fitness.values, ind2.fitness.values
#
#         # Evaluate the individuals with an invalid fitness
#         invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
#         fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
#         for ind, fit in zip(invalid_ind, fitnesses):
#             ind.fitness.values = fit
#
#         # Select the next generation population
#         pop = toolbox.select(pop + offspring, MU)
#         record = stats.compile(pop)
#         logbook.record(gen=gen, evals=len(invalid_ind), **record)
#         print(logbook.stream)
#
#     print("Final population hypervolume is %f" % hypervolume(pop, [11.0, 11.0]))
#
#     return pop, logbook
#
# if __name__ == "__main__":
#     # with open("pareto_front/zdt1_front.json") as optimal_front_data:
#     #     optimal_front = json.load(optimal_front_data)
#     # Use 500 of the 1000 points in the json file
#     # optimal_front = sorted(optimal_front[i] for i in range(0, len(optimal_front), 2))
#
#     pop, stats = main()
#     # pop.sort(key=lambda x: x.fitness.values)
#
#     # print(stats)
#     # print("Convergence: ", convergence(pop, optimal_front))
#     # print("Diversity: ", diversity(pop, optimal_front[0], optimal_front[-1]))
#
#     # import matplotlib.pyplot as plt
#     # import numpy
#
#     # front = numpy.array([ind.fitness.values for ind in pop])
#     # optimal_front = numpy.array(optimal_front)
#     # plt.scatter(optimal_front[:,0], optimal_front[:,1], c="r")
#     # plt.scatter(front[:,0], front[:,1], c="b")
#     # plt.axis("tight")
#     # plt.show()
