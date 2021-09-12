import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import wbgapi as wb

pd.options.display.max_columns = None
pd.options.display.max_rows = None

#Plot #1
df_water = wb.data.DataFrame('SH.H2O.BASW.ZS', time = 2017, labels = True)
df_water = df_water.dropna()
df_water = df_water.loc[:'AFG']
df_water = df_water.round(2)
df_water = df_water.rename(columns = {'SH.H2O.BASW.ZS': '% of Pop. Having Water'})
print(df_water)
print('')

sns.set_style('darkgrid')
f, plot_water = plt.subplots(figsize = (12, 7))
plot_water = sns.histplot(data = df_water, x = '% of Pop. Having Water', bins = 8, color = 'red')
plot_water.set_title('Percentage of Population Having Access to Basic Drinking Facilities per Country in 2017', fontsize = 15, fontweight ='bold')
plot_water.set_xlabel('Percentage of Population Having Access to Basic Drinking Facilities', fontsize = 12)
plot_water.set_ylabel('Number of Countries', fontsize = 12)
plot_water.yaxis.set_ticks(np.arange(0, 145, 5))
plot_water.set(xlim = (30, 100))

#Plot #2
df_food = wb.data.DataFrame('SN.ITK.DEFC.ZS', time = 2017, labels = True)
df_food = df_food.dropna()
df_food = df_food.loc[:'AFG']
df_food['SN.ITK.DEFC.ZS'] = 100 - df_food['SN.ITK.DEFC.ZS']
df_food = df_food.rename(columns = {'SN.ITK.DEFC.ZS': '% of Pop. Having Food'})
print(df_food)

sns.set_style('whitegrid')
f, plot_food = plt.subplots(figsize = (12, 6))
plot_food = sns.histplot(data = df_food, x = '% of Pop. Having Food', bins  = 7, color = 'green', kde = True)
plot_food.set_title('Percentage of Population Having Access to Proper Nutrition per Country in 2017', fontsize = 15, fontweight ='bold')
plot_food.set_xlabel('Percentage of Population Having Access to Proper Nutrition', fontsize = 12)
plot_food.set_ylabel('Number of Countries', fontsize = 12)
plot_food.yaxis.set_ticks(np.arange(0, 115, 10))
plot_food.set(xlim = (30, 100))

#Show both plots
plt.show()