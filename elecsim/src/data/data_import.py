import pandas as pd

def read_smart_meter_data(dir):
    data = pd.read_csv(dir,index_col=[0,1])
    groupby = data.groupby(['house_id']).aggregate(lambda x: tuple(x))

    return groupby

# data = read_smart_meter_data('/Users/b1017579/Documents/PhD/Projects/6. Agent Based Models/elecsim/elecsim/Data/one_hour_30.csv')
# groupby = data.groupby(['house_id'])['value'].apply(list)

# groupby = data.groupby(['house_id']).aggregate(lambda x: tuple(x))


# print(groupby)
# print(groupby.size)

# g = list(groupby.iloc[1].tolist()[0][0])
# print(g)
