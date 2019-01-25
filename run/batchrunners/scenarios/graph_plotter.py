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


if __name__ == '__main__':
    os.chdir("{}/run/batchrunners/scenarios/data/third_run_4_iterations_smaller_taxes/".format(ROOT_DIR))

    for file_name in glob.glob('*.csv'):
        scenario_results = pd.read_csv(file_name,dtype=np.float64)
        scenario_results['total'] = scenario_results.iloc[:,1:8].sum(axis=1)
        scenario_results.iloc[:,1:8] = scenario_results.iloc[:,1:8].div(scenario_results.total, axis=0)
        logger.info("Plotting: {}".format(file_name))
        scenario_results_long = pd.melt(scenario_results, id_vars='Unnamed: 0', value_vars=['CCGT', 'Coal', 'Onshore', 'Offshore', 'PV', 'Nuclear',
       'Recip_gas'])
        plot = sns.lineplot(x="Unnamed: 0", y="value", hue='variable', data=scenario_results_long).set_title(file_name)
        figure = plot.get_figure()



        figure.savefig('{}/run/batchrunners/scenarios/figures/third_run_4_iterations_smaller_taxes/{}{}.png'.format(ROOT_DIR, file_name.split(".")[0],file_name.split(".")[1]))
        plt.close('all')


