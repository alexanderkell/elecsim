import pandas as pd
from itertools import count, islice, cycle
from functools import reduce

pd.set_option('display.max_columns', 70)
pd.set_option('display.max_rows', 200)

# df = pd.read_csv("/Users/b1017579/Documents/PhD/Projects/10. ELECSIM/elecsim/data/Power Plants/Power_Plant_costs/page_1.csv")
df = pd.read_csv("/Users/b1017579/Documents/PhD/Projects/10. ELECSIM/elecsim/data/Power Plants/Power_Plant_costs/plant_costs_files/page_1.csv")


def plant_data(dat):
    characteristics = dat.loc[0:2].dropna(axis='columns').drop(['Unnamed: 1'], axis=1).transpose()
    operating_period = dat.loc[9].dropna().drop(['Unnamed: 1']).transpose().to_frame()

    dat = characteristics.merge(operating_period, left_index=True, right_index=True)

    dat = dat.rename(index=str, columns = {0:"Plant_Size",1:"Average_Load_Factor",2:"Efficiency",9:"Operating_Period"})
    # dat.rename(columns={"Unnamed: 0 ": "Plants"})

    return dat
    # return dat


def development_period(dat):
    dat = df.iloc[3:9].copy()
    dat.iloc[:, 0] = dat.iloc[:, 0].fillna(method='ffill')

    dat.iloc[:, 0] = dat.iloc[:, 0].replace({
                                                    "Pre-development period ":"Pre", "Construction period ":"Constr"})

    dat.iloc[:, 1] = dat.iloc[:, 1].replace({
                                                    "Duration and % spend per years 1 & 2 ": "Dur,1,2",
                                                    "% spend per years 3, 4, & 5 ": "3,4,5",
                                                    "% spend per years 6, 7, & 8 ": "6,7,8"})

    dat['A'], dat['B'], dat['C'] = dat.iloc[:, 1].str.split(',', 2).str
    dat = dat.drop(['Unnamed: 1'], axis=1)
    dat['A'], dat['B'], dat['C'] = dat['Unnamed: 0'] + "_" + dat['A'], dat['Unnamed: 0'] + "_" + dat['B'], dat['Unnamed: 0'] + "_" + dat['C']

    tot_cols = []
    for it in islice(count(),1,13,3):
        # print(it)
        cycle_period = cycle(['A', 'B', 'C'])
        for val in range(0,3):
            period = next(cycle_period)
            cols = pd.DataFrame({'plant': dat.columns.values[it],'period': dat[period],'value': dat.iloc[:, it+val]})
            tot_cols.append(cols)
        # print(tot_cols)
    db = pd.concat(tot_cols).reset_index().drop(['index'],axis=1)
    db = db.pivot(index='plant', columns='period', values='value')

    return db


def costs(dat):
    dat=dat[10:].copy()
    dat.iloc[:, 0] = dat.iloc[:, 0].fillna(method='ffill')

    dat.iloc[:, 0] = dat.iloc[:, 0].replace({
                                                    "Pre-development £/kW ":"Pre-dev_cost", "Construction £/kW ":"Constr_cost",
                                                    "Infrastructure £'000s ":"Infra_cost", "Fixed O&M £/MW/year ":"Fixed_cost",
                                                    "Variable O&M £/MWh ":"Var_cost","Insurance £/MWh/year ":"Insurance_cost",
                                                    "Connection and Use of System charges £/MW/year ":"Connect_system_cost"
                                                    })
    dat.iloc[:, 0] = dat.iloc[:, 0] + ":" + dat.iloc[:,1]
    dat = dat.drop(['Unnamed: 1'], axis=1)

    col_names = []
    col_values = []
    plant_names = [x for z in range(13) for x in dat.columns if not "Unnamed:" in x for y in range(3)]

    for x in dat[2:].itertuples(index=False):
        for j in range(1,len(x)):
            col_names.append(x[0]+"_"+dat.iloc[1, j])
            col_values.append(x[j])

    cols_df = pd.DataFrame({'columns':col_names,'plant':plant_names,'col_values':col_values})
    cols_df = cols_df.pivot(index="plant",values='col_values',columns='columns')
    return cols_df


def convert_cost_csv(df):
    plant = plant_data(df)
    # print("------PLANT-------")
    # print(plant)
    dev = development_period(df)
    # print("------DEV------")
    # print(dev)
    cost = costs(df)
    # print("------COSTS----")
    # print(costs)

    dfs = [plant, dev, cost]

    df_final = reduce(lambda left, right: pd.merge(left,right, left_index=True, right_index=True), dfs)
    return df_final


print(convert_cost_csv(df))
