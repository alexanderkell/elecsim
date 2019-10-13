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

from pebble import ProcessPool
from concurrent.futures import TimeoutError

import time
from pathlib import Path
project_dir = Path("__file__").resolve().parents[1]
import string
import random

"""
File name: optimiser_for_beis_scenario
Date created: 04/09/2019
Feature: #Enter feature description here
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"


pd.set_option('display.max_rows', 4000)

logging.basicConfig(level=logging.INFO)


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



# }config = {
#   'host':'elecsimresults.mysql.database.azure.com',
#   'user':'alexkell@elecsimresults',
#   'password':'b3rz0s4m4dr1dth3h01113s!',
#   'database':'elecsim',
#   'ssl_ca':'run/validation-optimisation/database/BaltimoreCyberTrustRoot.crt.pem'
# }
config = {
  'host':'elecsimresults2.mysql.database.azure.com',
  'user':'alexkell@elecsimresults2',
  'password':'b3rz0s4m4dr1dth3h01113s!',
  'database':'elecsimbeisresults',
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
    # return ([1]),

    # individual = np.array([0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    prices_individual = np.array(individual[:-3]).reshape(-1, 2).tolist()


    MARKET_TIME_SPLICES = 8
    YEARS_TO_RUN = 5
    number_of_steps = YEARS_TO_RUN * MARKET_TIME_SPLICES

    scenario_2018 = "{}/../run/beis_case_study/scenario/reference_scenario_2018.py".format(ROOT_DIR)

    world = World(initialization_year=2018, scenario_file=scenario_2018, market_time_splices=MARKET_TIME_SPLICES, data_folder="best_run_beis_comparison", number_of_steps=number_of_steps, long_term_fitting_params=prices_individual, highest_demand=63910, nuclear_subsidy=individual[-3], future_price_uncertainty_m=individual[-2], future_price_uncertainty_c=individual[-1])
    time_start = time.perf_counter()
    timestamp_start = time.time()
    for _ in range(YEARS_TO_RUN):
        for i in range(MARKET_TIME_SPLICES):
            try:
                results_df, over_invested = world.step()
            except:
                return [[99999999], 0, 0, 0, 0]
            if over_invested:
                return [[99999999], 0, 0, 0, 0]
        _, cumulative_diff = get_projection_difference_sum(results_df, world.year_number)
        # print("cumulative diff: {}".format(cumulative_diff))
        if cumulative_diff > 3:
            return [[99999999-(10*world.year_number)], 0, 0, 0, 0]
        else:
            pass

    time_end = time.perf_counter()
    timestamp_end = time.time()

    time_taken = time_end-time_start

    joined, total_difference = get_projection_difference_sum(results_df)

    print("max_demand : dif: {} :x {}".format(individual, total_difference))
    # print(joined.simulated)
    # print("input: {} {}, returns: {}, {}, {}".format(individual[0], individual[1], [total_difference], time_taken, joined.simulated))
    # print("input: {} {}, returns: {}, {}, {}".format(individual[0], individual[1], [total_difference], time_taken, timestamp_start, timestamp_end, joined.simulated))
    try:
        return [total_difference], time_taken, timestamp_start, timestamp_end, joined.simulated
    except AttributeError:
        return [total_difference], time_taken, timestamp_start, timestamp_end, 0
# contributed_results['run_id'] = np.repeat(list(range(int(len(contributed_results)/number_of_steps))), number_of_steps)
# def get_year(df):
#     df['year'] = np.repeat(list(range(YEARS_TO_RUN)), 8)
#     return df

def get_mix(df):
    df['actual_perc'] = df['value_actual'] / df['value_actual'].sum()
    df['simulated_perc'] = df['value_predicted'] / df['value_predicted'].sum()
    return df

def get_projection_difference_sum(results_df, year_to_compare=None):
    contributed_results = results_df.filter(regex='contributed_')  # .tail(MARKET_TIME_SPLICES)
    contributed_results *= 1 / 24

    # best_mix_year = contributed_results.apply(get_year)
    best_mix_year = contributed_results.copy()
    # best_mix_year['year'] = np.repeat(list(range(YEARS_TO_RUN)), 8)
    best_mix_year['year'] = np.repeat(list(range(int(len(best_mix_year.index)/8))), 8)
    # print("contributed_results: {}".format(contributed_results))
    best_mix_year = best_mix_year.rename(columns={'contributed_PV': "contributed_solar"})
    cluster_size = pd.Series([22.0, 30.0, 32.0, 35.0, 43.0, 53.0, 68.0, 82.0])
    # contributed_results['cluster_size'] = [22.0, 30.0, 32.0, 35.0, 43.0, 53.0, 68.0, 82.0]
    # print("best_mix_year: {}".format(best_mix_year))
    results_wa = best_mix_year.groupby('year').apply(
        lambda x: np.average(x, weights=cluster_size.values, axis=0)).to_frame()
    # print("results_wa: {}".format(results_wa))
    results_wa_split = pd.DataFrame(results_wa)
    # print(results_wa.values)
    results_wa_split[
        ['ccgt', "coal", 'onshore', 'offshore', 'solar', 'nuclear', 'recip_gas', 'biomass', 'year']] = pd.DataFrame(
        results_wa.values[0].tolist(), index=results_wa.index)
    results_wa_split
    # print("results_wa_split: {}".format(results_wa_split))
    # results_wa.index = results_wa.index.str.split("_").str[1].str.lower()
    # print("results_wa: {}".format(results_wa))
    # offshore = results_wa.loc["offshore"].iloc[0]
    # onshore = results_wa.loc["onshore"].iloc[0]
    results_wa_split['wind'] = results_wa_split['offshore'] + results_wa_split['onshore']
    results_wa_split['Natural_gas'] = results_wa_split['ccgt'] + results_wa_split['recip_gas']
    results_wa_split['Renewables'] = results_wa_split['biomass'] + results_wa_split['wind'] + results_wa_split['solar']
    results_wa_split = results_wa_split.drop(['offshore', 'onshore', 'ccgt', 'recip_gas', 'biomass', 'wind', 'solar'],
                                             axis=1)
    results_wa_split = results_wa_split.drop([0, 'year'], axis=1)
    results_wa_long = pd.melt(results_wa_split.reset_index(), id_vars="year")
    results_wa_long['year'] += 2018
    # print("results_wa_long: {}".format(results_wa_long))

    if year_to_compare is not None:
        # results_wa_long = results_wa_long[results_wa_long.year == year_to_compare+1]
        results_wa_long = results_wa_long[results_wa_long.year == year_to_compare]

    results_wa_long = results_wa_long.rename(columns={'variable': "fuel_type"})
    results_wa_long = results_wa_long.set_index(['year', 'fuel_type'])
    # results_wa = results_wa.append(pd.DataFrame({"wind", offshore+onshore}))
    # results_wa.loc['wind'] = [offshore+onshore]
    # print("results_wa: {}".format(results_wa))
    beis_forecast = pd.read_csv('{}/../run/beis_case_study/data/reference_run/2018-2035-beis.csv'.format(ROOT_DIR))
    # electricity_mix = pd.read_csv("{}/data/processed/electricity_mix/energy_mix_historical.csv".format(ROOT_DIR))
    beis_forecast['fuel_type'] = beis_forecast['fuel_type'].replace(
        {"Coal": 'coal', 'Natural gas': 'Natural_gas', "Nuclear": "nuclear"})
    beis_2035_long = pd.melt(beis_forecast, id_vars='fuel_type')
    # print("beis_2035_long: {}".format(beis_2035_long))
    beis_2035_long.variable = pd.to_numeric(beis_2035_long.variable)
    # beis_2035_long = beis_2035_long[beis_2035_long.variable <= 2020]
    beis_2035_long = beis_2035_long.rename(columns={"variable": "year"})
    # print("beis_2035_long_1 : {}".format(beis_2035_long))
    beis_2035_long = beis_2035_long.set_index(["year", 'fuel_type'])
    # print("beis_2035_long: {}".format(beis_2035_long))
    # print("results_wa_long: {}".format(results_wa_long))
    joined = beis_2035_long.join(results_wa_long, how='inner', lsuffix="_actual", rsuffix="_predicted")
    # print("joined: \n{}".format(joined))
    joined = joined.rename(columns={'value': 'actual', 0: 'simulated'})
    # joined = joined.reset_index()
    # joined = joined.loc[~joined.index.str.contains('biomass')]
    # print("joined: \n{}".format(joined))

    joined = joined.groupby("year").apply(get_mix)
    print("joined grouped: \n{}".format(joined))
    try:
        total_difference_col = abs(joined['actual_perc'] - joined['simulated_perc'])
        print(total_difference_col)
        total_difference = total_difference_col.abs().sum()
        print(total_difference)
    except:
        total_difference = 999998
    return joined, total_difference


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
toolbox.register("attr_m", random.uniform, 0.0, 0.003)
toolbox.register("attr_c", random.uniform, -30, 50)
toolbox.register("attr_nuclear_sub", random.uniform, 0, 150)

toolbox.register("attr_future_price_uncertainty_m", random.uniform, 0, 10)
toolbox.register("attr_future_price_uncertainty_c", random.uniform, 0, 10)

toolbox.register("map_distributed", futures.map)



# Structure initializers
#                         define 'individual' to be an individual
#                         consisting of 100 'attr_bool' elements ('genes')
toolbox.register("individual", tools.initCycle, creator.Individual, (toolbox.attr_m, toolbox.attr_c, toolbox.attr_m, toolbox.attr_c, toolbox.attr_m, toolbox.attr_c, toolbox.attr_m, toolbox.attr_c, toolbox.attr_m, toolbox.attr_c, toolbox.attr_m, toolbox.attr_c, toolbox.attr_m, toolbox.attr_c, toolbox.attr_m, toolbox.attr_c, toolbox.attr_m, toolbox.attr_c, toolbox.attr_m, toolbox.attr_c, toolbox.attr_m, toolbox.attr_c, toolbox.attr_m, toolbox.attr_c, toolbox.attr_m, toolbox.attr_c, toolbox.attr_m, toolbox.attr_c, toolbox.attr_m, toolbox.attr_c, toolbox.attr_m, toolbox.attr_c, toolbox.attr_m, toolbox.attr_c, toolbox.attr_nuclear_sub, toolbox.attr_future_price_uncertainty_c, toolbox.attr_future_price_uncertainty_m), 1)

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
toolbox.register("select", tools.selTournament, tournsize=10)

#----------

# eval_world([0.002547, -13.374101,0.002547, -13.374101,0.002547, -13.374101,0.002547, -13.374101,0.002547,0.002547, -13.374101,0.002547,0.002547, -13.374101,0.002547,0.002547, -13.374101,0.002547,0.002547, -13.374101,0.002547])
# eval_world([0.000137615718875977, -20.661061777482672, 0.001855046716492092, -20.20537031004143, 0.0010007529142925344, 31.253694948054033, 0.0027059244084475537, 30.01188585297122, 0.0016018356671484695, 37.59359989736696, 0.0008953508572214155, -12.892645057337102, 0.001513974732012828, 6.506433416826368, 0.002023948965422118, 1.8106558207626051, 0.0008781476149830236, -25.595797095196183, 0.0005881160162589889, 14.435076960058062, 0.0013461065471132225, -10.576048737244264, 0.0001378752516406303, 34.120748147348806, 0.001127774446127339, -17.286036063853363, 0.00012280742501245134, 7.395480867947832, 0.00032273106750109514, -18.93807731245588, 0.0014681438742877098, -21.658343265042717, 0.002670174360030499, 7.383998066104375, 37.94741640791914, 6.616435857663106, 4.446264311226145])

def main():

    # create an initial population of 300 individuals (where
    # each individual is a list of integers)
    pop = toolbox.population(n=127)

    # CXPB  is the probability with which two individuals
    #       are crossed
    #
    # MUTPB is the probability for mutating an individual
    CXPB, MUTPB = 0.5, 0.2

    print("Start of evolution")

    # Evaluate the entire population
    # fitnesses = list(map(toolbox.evaluate, pop))

    # fitnesses_and_time = []


    # with ProcessPool() as pool:
    fitnesses_and_time = list(toolbox.map_distributed(toolbox.evaluate, pop))
    #     future = pool.map(toolbox.evaluate, pop)
    #     iterator = future.result()
    #
    #     while True:
    #         try:
    #             fitnesses_and_time.append(next(iterator))
    #         except StopIteration:
    #             print("StopIteration Error")
    #             break
    #         except TimeoutError as error:
    #             print("function took longer than %d seconds" % error.args[1])
    #             fitnesses_and_time.append([[9999999999], 0, 0, 0, 0])

    # fitnesses = [fitness_time[0] for fitness_time in fitnesses_and_time]
    # print(fitnesses_and_time)

    timing_holder = []

    for ind, fit in zip(pop, fitnesses_and_time):
        ind.fitness.values = fit[0]
        # timing_holder.append(fit[1])

    print("  Evaluated %i individuals" % len(pop))

    # Extracting all the fitnesses of
    fits = [ind.fitness.values[0] for ind in pop]

    # Variable keeping track of the number of generations
    g = 0

    # Begin the evolution
    while g < 1000:

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
                # del child1.fitness.values
                # del child2.fitness.values

        # Recalculate all individual due to stochastic nature of simulation
        for ind in offspring:
            del ind.fitness.values

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

        # fitnesses = list(toolbox.map_distributed(toolbox.evaluate, invalid_ind))

        # fitnesses = []
        # with ProcessPool() as pool:
        # fitnesses_and_time = list(toolbox.map_distributed(toolbox.evaluate, pop))
        fitnesses = list(toolbox.map_distributed(toolbox.evaluate, pop))
            # future = pool.map(toolbox.evaluate, pop)
            # iterator = future.result()
            #
            # while True:
            #     try:
            #         fitnesses.append(next(iterator))
            #     except StopIteration:
            #         break
            #     except TimeoutError as error:
            #         print("function took longer than %d seconds" % error.args[1])
            #         fitnesses.append([[9999999999], 0, 0, 0, 0])
            # print(fitnesses)

        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit[0]
            try:
                timing_holder.append(fit[1])
                time_start_holder.append(fit[2])
                time_end_holder.append(fit[3])
                generators_invested.append(fit[4])
            except:
                timing_holder.append(0)
                time_start_holder.append(0)
                time_end_holder.append(0)
                generators_invested.append(0)

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

        first_part = 'INSERT INTO validoptimresults1 (run_number,time_taken,timestamp_start,timestamp_end,reward,individual_m_1,individual_c_1,individual_m_2,individual_c_2,individual_m_3,individual_c_3,individual_m_4,individual_c_4,individual_m_5,individual_c_5,individual_m_6,individual_c_6,individual_m_7,individual_c_7,individual_m_8,individual_c_8,individual_m_9,individual_c_9,individual_m_10,individual_c_10,individual_m_11,individual_c_11,individual_m_12,individual_c_12,individual_m_13,individual_c_13,individual_m_14,individual_c_14,individual_m_15,individual_c_15,individual_m_16,individual_c_16,individual_m_17,individual_c_17,attr_nuclear_sub,attr_future_price_uncertainty_c,attr_future_price_uncertainty_m,coal,nuclear,ccgt,wind,solar) VALUES '
        try:
            insert_vars = "".join(["({},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}),\n".format(g, time, time_start, time_end, ind.flat[0], ind.flat[1], ind.flat[2], ind.flat[3], ind.flat[4], ind.flat[5], ind.flat[6], ind.flat[7], ind.flat[8], ind.flat[9], ind.flat[10], ind.flat[11], ind.flat[12], ind.flat[13], ind.flat[14], ind.flat[15], ind.flat[16], ind.flat[17], ind.flat[18], ind.flat[19], ind.flat[20], ind.flat[21], ind.flat[22], ind.flat[23], ind.flat[24], ind.flat[25], ind.flat[26], ind.flat[27], ind.flat[28], ind.flat[29], ind.flat[30], ind.flat[31], ind.flat[32], ind.flat[33], ind.flat[34], ind.flat[35], ind.flat[36], ind.flat[37], gen_invested.loc['coal'], gen_invested.loc['nuclear'], gen_invested.loc['ccgt'], gen_invested.loc['wind'], gen_invested.loc['solar']) for ind, time, time_start, time_end, gen_invested in zip(progression, timing_holder, time_start_holder, time_end_holder, generators_invested)])
            insert_cmd = first_part+insert_vars
            insert_cmd = insert_cmd[:-2]
            # print("command: {}".format(insert_cmd))

            cursor.execute(insert_cmd)
            conn.commit()
            cursor.close()
            conn.close()
        except:
            insert_vars = "".join(["({},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}),\n".format(g, time, time_start, time_end, ind.flat[0], ind.flat[1], ind.flat[2], ind.flat[3], ind.flat[4], ind.flat[5], ind.flat[6], ind.flat[7], ind.flat[8], ind.flat[9], ind.flat[10], ind.flat[11], ind.flat[12], ind.flat[13], ind.flat[14], ind.flat[15], ind.flat[16], ind.flat[17], ind.flat[18], ind.flat[19], ind.flat[20], ind.flat[21], ind.flat[22], ind.flat[23], ind.flat[24], ind.flat[25], ind.flat[26], ind.flat[27], ind.flat[28], ind.flat[29], ind.flat[30], ind.flat[31], ind.flat[32], ind.flat[33], ind.flat[34], ind.flat[35], ind.flat[36], ind.flat[37], -1000, -1000, -1000, -1000, -1000) for ind, time, time_start, time_end, gen_invested in zip(progression, timing_holder, time_start_holder, time_end_holder, generators_invested)])
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
    # pass

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
