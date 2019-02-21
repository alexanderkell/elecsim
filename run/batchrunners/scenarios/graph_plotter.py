import glob
import logging
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from constants import ROOT_DIR

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
    os.chdir("{}/run/batchrunners/scenarios/data/{}".format(ROOT_DIR, folder))
    for file_name in glob.glob('*.csv'):
        print(file_name)
        scenario_results = pd.read_csv(file_name,encoding="ISO-8859-1")
        print(scenario_results)
        scenario_results['total'] = scenario_results.iloc[:,1:8].sum(axis=1)
        scenario_results.iloc[:,1:8] = scenario_results.iloc[:,1:8].div(scenario_results.total, axis=0)
        scenario_results = scenario_results.replace(r'\[|\]','',regex=True).astype(float)

        logger.info("Plotting: {}".format(file_name))
        scenario_results_long = pd.melt(scenario_results, id_vars='Unnamed: 0', value_vars=['CCGT', 'Coal', 'Onshore', 'Offshore', 'PV', 'Nuclear',
       'Recip_gas', 'Carbon_tax'])


        plot = sns.lineplot(x="Unnamed: 0", y="value", hue='variable', data=scenario_results_long).set_title(file_name)
        figure = plot.get_figure()

        # ax2 = plt.twinx()
        # sns.lineplot(x="Unnamed: 0", y="Carbon_tax", data=group, color="black", ax=ax2, linewidth=3, label="Carbon Price")
        # ax2.set_ylim(-10,200)
        # ax2.set_ylabel("Carbon Tax (£/tonne)")


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
        scenario_results = scenario_results.rename(index=str, columns = {"Recip_gas":"Recip. Gas"})
        scenario = file_name.split("_")[0]+file_name.split("_")[1]+file_name.split("_")[2]
        scenario_results['Unnamed: 0'] += 2013
        scenario_results['Carbon_tax'] = scenario_results['Carbon_tax'].shift(6)
        scenario_results[['CCGT','Coal','Onshore','Offshore','PV','Nuclear','Recip. Gas']] = scenario_results[['CCGT','Coal','Onshore','Offshore','PV','Nuclear','Recip. Gas']].iloc[6:]
        scenario_results['scenario'] = [scenario]*len(scenario_results)
        scenario_results['total'] = scenario_results.iloc[:,1:8].sum(axis=1)
        scenario_results.iloc[:,1:8] = scenario_results.iloc[:,1:8].div(scenario_results.total/100, axis=0)

        all_data.append(scenario_results)
    frame = pd.concat(all_data, axis=0, ignore_index=True)
    frame_long = pd.melt(frame, id_vars=['Unnamed: 0','scenario','Carbon_tax'],value_vars=['CCGT', 'Coal', 'Onshore', 'Offshore', 'PV', 'Nuclear','Recip. Gas'])
    frame_long = frame_long.rename(index=str, columns={'variable':"Variables"})
    scenario_group = frame_long.groupby('scenario')

    directory = '{}/run/batchrunners/scenarios/figures/{}'.format(ROOT_DIR, folder_to_save)
    if_no_directory_create(directory)

    publishable = '{}/run/batchrunners/scenarios/figures/to_publish/{}'.format(ROOT_DIR, folder_to_save)
    if_no_directory_create(directory)

    # for name, group in scenario_group:
    #     plot = sns.lineplot(x="Unnamed: 0", y="value", hue='variable', data=group).set_title(name)
    #     ax2 = plt.twinx()
    #     sns.lineplot(x="Unnamed: 0", y="Carbon_tax", data=group, color="black", ax=ax2)
    #     ax2.set_ylim(-10,200)
    #     figure = plot.get_figure()
    #
    #
    #     print("Saving figure: {}".format(name))
    #     figure.savefig('{}/{}.png'.format(directory,name))
    #     plt.close('all')

    for name, group in scenario_group:

        plot = sns.lineplot(x="Unnamed: 0", y="value", hue='Variables', data=group)
        plt.xlabel('Year')
        plt.ylabel('Share of Energy Mix (%)')
        ax2 = plt.twinx()
        sns.lineplot(x="Unnamed: 0", y="Carbon_tax", data=group, color="black", ax=ax2, linewidth=3, label="Carbon Price")
        ax2.set_ylim(-10,200)
        ax2.set_ylabel("Carbon Tax (£/tonne)")



        h1, l1 = plot.get_legend_handles_labels()
        h2, l2 = ax2.get_legend_handles_labels()
        box = ax2.get_position()
        ax2.set_position([box.x0, box.y0,box.width, box.height * 0.9])
        if (name == "demand099-carbon10-datetime") or (name =='demand099-carbon70-datetime'):

            # ax2.set_position([box.x0, box.y0,box.width, box.height * 0.9])

            ax2.legend(h1+h2, l1+l2, loc='upper center', bbox_to_anchor=(0.5, 1.2),fancybox=True, shadow=True, ncol=5, fontsize=17.5)


        else:
            ax2.get_legend().remove()
        plot.get_legend().remove()
        # plt.show()
        print("Saving figure: {}".format(name))
        plt.rcParams['figure.figsize'] = 12, 10

        plt.rcParams.update({'font.size': 25})
        figure = plot.get_figure()
        # plt.show()
        figure.savefig('{}/{}.png'.format(publishable,name))
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


def if_no_directory_create(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


if __name__ == '__main__':
    # single_plots("fourth_run_8_iterations_lower_taxes_no_max_investment_2018", "fourth_run_8_iterations_lower_taxes_no_max_investment_2018")
    # variance_plots('fourth_run_8_iterations_lower_taxes_no_max_investment_2018','first_variance_results')
    single_plots("None", "first_rl_results")

