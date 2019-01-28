from constants import ROOT_DIR
import matplotlib.pyplot as plt
import seaborn as sns
import glob, os
import numpy as np
import pandas as pd
import logging

logger = logging.getLogger(__name__)
"""
File name: graph_plotter
Date created: 20/01/2019
Feature: #Enter feature description here
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)

logging.basicConfig(level=logging.INFO)



def single_plots(folder, folder_to_save):
    os.chdir("{}/run/batchrunners/scenarios/data//".format(folder, ROOT_DIR))
    for file_name in glob.glob('*.csv'):
        scenario_results = pd.read_csv(file_name,dtype=np.float64)
        scenario_results['total'] = scenario_results.iloc[:,1:8].sum(axis=1)
        scenario_results.iloc[:,1:8] = scenario_results.iloc[:,1:8].div(scenario_results.total, axis=0)
        logger.info("Plotting: {}".format(file_name))
        scenario_results_long = pd.melt(scenario_results, id_vars='Unnamed: 0', value_vars=['CCGT', 'Coal', 'Onshore', 'Offshore', 'PV', 'Nuclear',
       'Recip_gas'])
        plot = sns.lineplot(x="Unnamed: 0", y="value", hue='variable', data=scenario_results_long).set_title(file_name)
        figure = plot.get_figure()

        directory = '{}/run/batchrunners/scenarios/figures/{}'.format(ROOT_DIR, folder_to_save)
        if not os.path.exists(directory):
            os.makedirs(directory)

        figure.savefig('{}/run/batchrunners/scenarios/figures/{}/{}{}.png'.format(ROOT_DIR, folder_to_save, file_name.split(".")[0],file_name.split(".")[1]))
        plt.close('all')


def variance_plots(folder, folder_to_save):
    os.chdir("{}/run/batchrunners/scenarios/data/{}".format(ROOT_DIR, folder))
    all_data = []
    for file_name in glob.glob('*.csv'):

        scenario_results = pd.read_csv(file_name,dtype=np.float64, index_col=None, header=0)
        scenario = file_name.split("_")[0]+file_name.split("_")[1]+file_name.split("_")[2]
        scenario_results['scenario'] = [scenario]*len(scenario_results)
        scenario_results['total'] = scenario_results.iloc[:,1:8].sum(axis=1)
        scenario_results.iloc[:,1:8] = scenario_results.iloc[:,1:8].div(scenario_results.total, axis=0)

        # print(scenario_results)
        all_data.append(scenario_results)
    frame = pd.concat(all_data, axis=0, ignore_index=True)
    frame_long = pd.melt(frame, id_vars=['Unnamed: 0','scenario','Carbon_tax'], value_vars=['CCGT', 'Coal', 'Onshore', 'Offshore', 'PV', 'Nuclear','Recip_gas'])

    scenario_group = frame_long.groupby('scenario')

    directory = '{}/run/batchrunners/scenarios/figures/{}'.format(ROOT_DIR, folder_to_save)
    if not os.path.exists(directory):
        os.makedirs(directory)

    for name, group in scenario_group:
        plot = sns.lineplot(x="Unnamed: 0", y="value", hue='variable', data=group).set_title(name)
        # ax2 = plt.twinx()
        # sns.lineplot(x="Unnamed: 0", y="Carbon_tax", data=group, color="black", ax=ax2,size=40)
        # ax2.set_ylim(-10,200)
        figure = plot.get_figure()


        print("Saving figure: {}".format(name))
        figure.savefig('{}/{}.png'.format(directory,name))
        plt.close('all')


    # print(frame_long.head())
    # g = sns.FacetGrid(data=frame_long, row='scenario', hue="variable")
    # g.map(plt.scatter, x='Unnamed: 0', y='value')
    # plt.show()
       #  scenario_results['total'] = scenario_results.iloc[:,1:8].sum(axis=1)
       #  scenario_results.iloc[:,1:8] = scenario_results.iloc[:,1:8].div(scenario_results.total, axis=0)
       #  logger.info("Plotting: {}".format(file_name))
       #  scenario_results_long = pd.melt(scenario_results, id_vars='Unnamed: 0', value_vars=['CCGT', 'Coal', 'Onshore', 'Offshore', 'PV', 'Nuclear',
       # 'Recip_gas'])
       #  print(scenario_results_long.columns)
       #



if __name__ == '__main__':
    # single_plots("fourth_run_8_iterations_lower_taxes_no_max_investment_2018", "fourth_run_8_iterations_lower_taxes_no_max_investment_2018")
    # variance_plots('fourth_run_8_iterations_lower_taxes_no_max_investment_2018','first_variance_results')
    variance_plots('5th_run_testing_2013_start','2013_start_variance_results')

