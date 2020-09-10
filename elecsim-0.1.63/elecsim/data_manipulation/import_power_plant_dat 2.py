import os
from functools import reduce
from itertools import count, islice, cycle

import numpy as np
import pandas as pd
from pandas.api.types import is_string_dtype

pd.set_option('display.max_columns', 70)
pd.set_option('display.max_rows', 200)


def plant_data(dat):
    """
    Takes the first part of the dataframe from the CSV file from the tables included in BEIS_Electricity_Generation_Cost_Report, and returns a dataframe with powerplants as columns and each data as columns
    :param dat: Input dataframe from BEIS_Electricity_Generation_Cost_Report
    :return: Returns first part of table, which includes plant size, average load factor, efficiency and operating period with power plants as rows and columns as data about said power plants
    """

    characteristics = dat.loc[0:2].dropna(axis='columns').drop(['Unnamed: 1'], axis=1).transpose()  # Fills empty column names, deletes units, and transposes dataframe so that plants are as rows
    operating_period = dat.loc[9].dropna().drop(['Unnamed: 1']).transpose().to_frame()  # Transposes operating period and drops units

    dat = characteristics.merge(operating_period, left_index=True, right_index=True)  # Merges the two series together to form a single dataframe

    dat = dat.rename(index=str, columns = {0:"Plant_Size",1:"Average_Load_Factor",2:"Efficiency",9:"Operating_Period"})  # Rename columns
    return dat


def development_period(dat):
    """
    Takes the entire dataframe from a table included in BEIS_Electricity_Generation_Cost_Report and returns data about the pre-development and construction cost expenditure information per year
    :param dat: Dataframe of the table included in BEIS_Electricity_Generation_Cost_Report
    :return: Returns a dataframe of power plant data which contains pre-development and construction expenditure information per year
    """
    dat = dat.iloc[3:9].copy()
    dat.iloc[:, 0] = dat.iloc[:, 0].fillna(method='ffill')

    dat.iloc[:, 0] = dat.iloc[:, 0].replace({  # Shorten column names
                                                    "Pre-development period ":"Pre", "Construction period ":"Constr"})

    dat.iloc[:, 1] = dat.iloc[:, 1].replace({  # Shorten column names
                                                    "Duration and % spend per years 1 & 2 ": "Dur,1,2",
                                                    "% spend per years 3, 4, & 5 ": "3,4,5",
                                                    "% spend per years 6, 7, & 8 ": "6,7,8"})

    dat['A'], dat['B'], dat['C'] = dat.iloc[:, 1].str.split(',', 2).str  # Split duration and spend per year to respective column
    dat = dat.drop(['Unnamed: 1'], axis=1)
    dat['A'], dat['B'], dat['C'] = dat['Unnamed: 0'] + "_" + dat['A'], dat['Unnamed: 0'] + "_" + dat['B'], dat['Unnamed: 0'] + "_" + dat['C']  # Merge column name with year information

    tot_cols = []
    for it in islice(count(), 1, len(dat.columns), 3):  # Skip through to columns containing power plant information
        cycle_period = cycle(['A', 'B', 'C'])  # Cycle through rows to create column names
        for val in range(0, 3):  # Three values per power plant
            period = next(cycle_period)
            cols = pd.DataFrame({'plant': dat.columns.values[it],'period': dat[period],'value': dat.iloc[:, it+val]})  # Create dataframe in wide format
            tot_cols.append(cols)
    db = pd.concat(tot_cols).reset_index().drop(['index'],axis=1)  # Concatenate all dataframes
    db = db.pivot(index='plant', columns='period', values='value')  # Transform dataframe to wide format

    return db


def costs(dat):
    """
    Takes dataframe from CSV file of BEIS_Electricity_Generation_Cost_Report and returns cost section of data into a wide format with power plant data per row
    :param dat: Dataframe starting from Table 19 found in BEIS_Electricity_Generation_Cost_Report
    :return: Returns dataframe of cost information in wide format
    """
    dat=dat[10:].copy()
    dat.iloc[:, 0] = dat.iloc[:, 0].fillna(method='ffill')  # Fill in blanks of power plant information

    dat.iloc[:, 0] = dat.iloc[:, 0].replace({  # Shorten column names
                                                    "Pre-development £/kW ":"Pre_dev_cost", "Construction £/kW ":"Constr_cost",
                                                    "Infrastructure £'000s ":"Infra_cost", "Fixed O&M £/MW/year ":"Fixed_cost",
                                                    "Variable O&M £/MWh ":"Var_cost","Insurance £/MWh/year ":"Insurance_cost",
                                                    "Connection and Use of System charges £/MW/year ":"Connect_system_cost"
                                                    })
    dat.iloc[:, 0] = dat.iloc[:, 0] + "-" + dat.iloc[:, 1]  # Merge cost information with projection (high, medium or low)
    dat = dat.drop(['Unnamed: 1'], axis=1)

    col_names = []
    col_values = []
    plant_names = [x for z in range(13) for x in dat.columns if not "Unnamed:" in x for y in range(3)]  # Create list containing plant names in correct order

    for x in dat[2:].itertuples(index=False):  # Loop through each row of dataframe
        for j in range(1,len(x)):
            col_names.append(x[0]+"_"+dat.iloc[1, j])  # Create column names by merging year of cost with cost type and projection
            col_values.append(x[j])  # Take column value

    cols_df = pd.DataFrame({'columns':col_names,'plant':plant_names,'col_values':col_values})  # Create dataframe
    cols_df = cols_df.pivot(index="plant",values='col_values',columns='columns')  # Make into wide format
    return cols_df


def merge_plant_cost_tables(df):
    """
    Function to bring together all sections of dataframe
    :param df: Dataframe starting from Table 19 found in BEIS_Electricity_Generation_Cost_Report
    :return: Returns final dataframe found in BEIS_Electricity_Generation_Cost_Report Table 19 in wide format
    """

    plant = plant_data(df)  # Call functions
    dev = development_period(df)
    cost = costs(df)

    dfs = [plant, dev, cost]  # Create a list of dataframes

    df_final = reduce(lambda left, right: pd.merge(left,right, left_index=True, right_index=True), dfs)  # Merge each dataframe together
    return df_final


def beis_human_to_machine_format(dir):

    final_df = []
    for file in os.listdir(dir):
        file_p = "/Users/b1017579/Documents/PhD/Projects/10. ELECSIM/10. ELECSIM/data/Power_Plants/Power_Plant_costs/plant_costs_files/"+file
        df = pd.read_csv(file_p).replace("- ",np.nan)
        final_df.append(merge_plant_cost_tables(df))
    final_df = pd.concat(final_df)

    # Remove comma seperator for increments of 1000 and unit of year
    final_df = final_df.apply(lambda x: x.str.replace(',', ''), axis=1).apply(lambda x: x.str.replace(' years',''), axis=1)
    # Remove the % sign and divide by 100
    final_df = final_df.apply(lambda x: x.str.replace("%", "").astype('float')/100 if is_string_dtype(x) and x.str.contains('%').all() else x)
    print(final_df)
    return final_df


p_dat = beis_human_to_machine_format("/Users/b1017579/Documents/PhD/Projects/10. ELECSIM/10. ELECSIM/data/Power_Plants/Power_Plant_costs/plant_costs_files")


p_dat.to_csv("/Users/b1017579/Documents/PhD/Projects/10. ELECSIM/10. ELECSIM/data/Power_Plants/Power_Plant_costs/plant_cost_data_nan.csv")
