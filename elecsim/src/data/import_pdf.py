import pandas as pd

pd.set_option('display.max_columns', 15)

df = pd.read_csv("/Users/b1017579/Documents/PhD/Projects/10. ELECSIM/elecsim/data/Power Plants/Power_Plant_costs/page_1.csv")
print(df[:])


cols1 = df.iloc[:, 0]
print("----------------------")
cols1 = cols1.fillna(method='ffill')
print(cols1)

cols2 = df.iloc[:, 1]
print("---------2nd-------------")
print(cols2)
cols2 = cols2.replace({"Duration and % spend per years 1 & 2 ": "Duration,year_1,year_2",
                       "% spend per years 3, 4, & 5 ": "year_3,year_4,year_5",
                       "% spend per years 6, 7, & 8 ": "year_6,year_7,year_8"})
print(cols2)

print("--------3rd----------")
cols2 = cols2.str.split(",").apply(pd.Series).stack()
print(cols2)

# col2 = cols2.str.split()
# print(cols2)


print("-----------COLS------------")
# cols = cols1.astype(str) + cols2
# print(cols)
