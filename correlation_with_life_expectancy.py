import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import wbgapi as wb

pd.options.display.max_columns = None
pd.options.display.max_rows = None

df_life_expectancy = wb.data.DataFrame('SP.DYN.LE00.MA.IN', time = 2019, labels = True)
df_life_expectancy = df_life_expectancy.dropna()
df_life_expectancy = df_life_expectancy.loc[:'AFG']
df_life_expectancy = df_life_expectancy.round(2)
df_life_expectancy = df_life_expectancy.rename(columns = {'SP.DYN.LE00.MA.IN': 'Life Expectancy'})
print('')

# Plot #1(heatmap): Life Expectancy and Basic Needs for some of the Most Populated Countries in the World
df_population_matrix = wb.data.DataFrame('SP.POP.TOTL', time = 2020, labels = True)
df_population_matrix = df_population_matrix.loc[:'AFG']
df_population_matrix = df_population_matrix.dropna()
df_population_matrix['SP.POP.TOTL'] = df_population_matrix['SP.POP.TOTL'].astype('int64')
df_population_matrix = df_population_matrix.nlargest(25, 'SP.POP.TOTL')
df_population_matrix = df_population_matrix.rename(columns = {'SP.POP.TOTL': 'Population (in millions)'})
df_population_matrix['Population (in millions)'] = df_population_matrix['Population (in millions)'] / 1000000
df_population_matrix['Population (in millions)'] = df_population_matrix['Population (in millions)'].round(2)
print('')

df_sanitation_matrix = wb.data.DataFrame('SH.STA.HYGN.ZS', time = 2017, labels = True)
df_sanitation_matrix = df_sanitation_matrix.fillna(99.5)
df_sanitation_matrix = df_sanitation_matrix.round(2)
df_sanitation_matrix.columns = ['Country', '% of Pop. Having Soap']

df_water_matrix = wb.data.DataFrame('SH.H2O.BASW.ZS', time = 2017, labels = True)
df_water_matrix = df_water_matrix.dropna()
df_water_matrix = df_water_matrix.loc[:'AFG']
df_water_matrix = df_water_matrix.round(2)
df_water_matrix = df_water_matrix.rename(columns = {'SH.H2O.BASW.ZS': '% of Pop. Having Water'})

df_food_matrix = wb.data.DataFrame('SN.ITK.DEFC.ZS', time = 2017, labels = True)
df_food_matrix = df_food_matrix.dropna()
df_food_matrix = df_food_matrix.loc[:'AFG']
df_food_matrix['SN.ITK.DEFC.ZS'] = 100 - df_food_matrix['SN.ITK.DEFC.ZS']
df_food_matrix = df_food_matrix.rename(columns = {'SN.ITK.DEFC.ZS': '% of Pop. Having Food'})

df_le_correlation_all = pd.merge(pd.merge(pd.merge(pd.merge(df_life_expectancy, df_population_matrix, how ='inner', on ='Country'),
                                                   df_sanitation_matrix, how ='inner', on ='Country'),
                                          df_water_matrix, how ='inner', on ='Country'),
                                 df_food_matrix, how ='inner', on ='Country')
df_le_correlation_all = df_le_correlation_all.set_index('Country', drop = True)
df_le_correlation_all = df_le_correlation_all.drop(axis = 1, columns ='Population (in millions)')
df_le_correlation_all = df_le_correlation_all.drop(axis = 0, index = ['Turkey', 'Russian Federation', 'Iran, Islamic Rep.', 'China', 'Brazil'])
print(df_le_correlation_all)
print('')

f, plot_corr_matrix = plt.subplots(figsize = (13, 7))
plot_corr_matrix = sns.heatmap(data = df_le_correlation_all, cmap ='icefire')
plot_corr_matrix.set_title('Life Expectancy and Basic Needs for some of the Most Populated Countries in the World', fontsize = 15, fontweight ='bold')
plot_corr_matrix.set_xlabel('Life Expectancy and Basic Needs', fontsize = 12)
plot_corr_matrix.set_ylabel('Countries', fontsize = 12)


# Plot #2(scatterplot): Access to Potable Water vs Life Expectancy
# Plot #3(regplot): Access to Food vs Life Expectancy
# Both plots are shown together
df_population = wb.data.DataFrame('SP.POP.TOTL', time = 2020, labels = True)
df_population = df_population.loc[:'AFG']
df_population = df_population.dropna()
df_population['SP.POP.TOTL'] = df_population['SP.POP.TOTL'].astype('int64')
df_population = df_population.rename(columns = {'SP.POP.TOTL': 'Population (in millions)'})
df_population['Population (in millions)'] = df_population['Population (in millions)'] / 1000000
df_population['Population (in millions)'] = df_population['Population (in millions)'].round(2)

df_le_corr_water = pd.merge(pd.merge(df_life_expectancy, df_water_matrix, how ='inner', on ='Country'),
                            df_population, how ='inner', on ='Country')
df_le_corr_water = df_le_corr_water[~df_le_corr_water['Country'].isin(['China', 'India'])]

df_le_corr_food = pd.merge(df_life_expectancy, df_food_matrix, how ='inner', on ='Country')

print(df_le_corr_water)
print('')
print(df_le_corr_food)
print('')

sns.set_style('darkgrid')
f, (plot_corr_water, plot_corr_food) = plt.subplots(1, 2, figsize = (12, 7))
plot_corr_le_water = sns.scatterplot(data = df_le_corr_water, x = '% of Pop. Having Water', y = 'Life Expectancy', ax = plot_corr_water,
                                     color = 'purple', size = 'Population (in millions)', sizes = (20, 200))
plot_corr_le_water.set_title('Access to Potable Water vs Life Expectancy', fontsize = 14, fontweight ='bold')
plot_corr_le_water.set_xlabel('Percentage of Population Having Access to Basic Drinking Facilities', fontsize = 12)
plot_corr_le_water.set_ylabel('Life Expectancy', fontsize = 12)

plot_corr_le_food = sns.regplot(data = df_le_corr_food, x = '% of Pop. Having Food', y = 'Life Expectancy', ax = plot_corr_food,
                                scatter_kws={'alpha': 0.5})
plot_corr_le_food.set_title('Access to Food vs Life Expectancy', fontsize = 14, fontweight ='bold')
plot_corr_le_food.set_xlabel('Percentage of Population Having Access to Proper Nutrition', fontsize = 12)
plot_corr_le_food.set_ylabel('Life Expectancy', fontsize = 12)
plot_corr_le_food.set(xlim = (50, 100))

# Plot #4(boxplot): Sanitation Level vs Life Expectancy
df_sanitation = wb.data.DataFrame('SH.STA.HYGN.ZS', time = 2017, labels = True)
df_sanitation = df_sanitation.dropna()
df_sanitation = df_sanitation.round(2)
df_sanitation.columns = ['Country', '% of Pop. Having Soap']

df_le_corr_sanitation = pd.merge(df_life_expectancy, df_sanitation, how = 'inner', on = 'Country')

# sanitation_level(sanitation) provides the sanitation level of sanitation
def sanitation_level(sanitation):
    if sanitation <= 50.0 :
        return 'Basic'
    if 50.0 < sanitation <= 80.0:
        return 'Average'
    if 80.0 < sanitation:
        return 'Good'

df_le_corr_sanitation['Country Type(by Sanitation Level)'] = df_le_corr_sanitation['% of Pop. Having Soap'].apply(sanitation_level)
print(df_le_corr_sanitation)

sns.set_style('darkgrid')
f, plot_corr_le_sanitation = plt.subplots(figsize = (11, 5))
plot_corr_le_sanitation = sns.boxplot(data = df_le_corr_sanitation, x = 'Country Type(by Sanitation Level)', y = 'Life Expectancy',
                                      order = ['Basic', 'Average', 'Good'], palette = 'Dark2')
plot_corr_le_sanitation.set_title('Sanitation Level vs Life Expectancy', fontsize = 15, fontweight ='bold')
plot_corr_le_sanitation.set_xlabel('Sanitation Level', fontsize = 12)
plot_corr_le_sanitation.set_ylabel('Life Expectancy', fontsize = 12)

# Show all plots
plt.show()