import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import wbgapi as wb

pd.options.display.max_columns = None
pd.options.display.max_rows = None

df = wb.data.DataFrame('NY.GDP.PCAP.CD', time = range(2019, 2021), labels = True)
df = df.dropna()
df['Average 2019-2020'] = (df['YR2020'] + df['YR2019']) / 2
df = df.sort_values('Average 2019-2020')
df = df.drop(axis = 1, columns = ['YR2019', 'YR2020'])
df = df.round(2)
print(df)
print('')

df = df.iloc[:11]
studied_countries = df['Country']
print(studied_countries)
print('')

# Plot #1(lineplot): Percentage of Population with Handwashing Facilities by Country from 2013 to 2017
df_sanitation_total = wb.data.DataFrame('SH.STA.HYGN.ZS', time = range(2013, 2018), labels = True)
df_sanitation_total = df_sanitation_total[df_sanitation_total['Country'].isin(studied_countries)]
df_sanitation_total = df_sanitation_total.dropna()
df_sanitation_total = df_sanitation_total.drop(index = 'AFG')
df_sanitation_total = df_sanitation_total.round(2)
df_sanitation_total.columns = ['Country', '2013', '2014', '2015', '2016', '2017']
df_sanitation_total = df_sanitation_total.melt(id_vars ='Country', var_name ='Year', value_name ='% with Handwashing Facilities')
print(df_sanitation_total)
df_sanitation_total = df_sanitation_total.pivot(index = 'Year', columns = 'Country', values = '% with Handwashing Facilities')
print(df_sanitation_total)
print('')

sns.set_style('whitegrid')
f, plot_sanitation_total = plt.subplots(figsize = (12, 7))
plot_sanitation_total = sns.lineplot(data = df_sanitation_total, linewidth = 4)
plot_sanitation_total.set_title('Percentage of Population with Handwashing Facilities by Country from 2013 to 2017', fontsize = 15, fontweight ='bold')
plot_sanitation_total.set_xlabel('Country', fontsize = 12)
plot_sanitation_total.set_ylabel('% with Handwashing Facilities', fontsize = 12)
plot_sanitation_total.yaxis.set_ticks(np.arange(0, 30, 5))
sns.move_legend(plot_sanitation_total, "lower left", ncol = 2)

# Plot #2(barplot): Percentage of Population with Handwashing Facilities by Settlement Type by Country in 2017
df_sanitation_urban = wb.data.DataFrame('SH.STA.HYGN.UR.ZS', time = 2017, labels = True)
df_sanitation_urban = df_sanitation_urban[df_sanitation_urban['Country'].isin(studied_countries)]
df_sanitation_urban = df_sanitation_urban.dropna()
df_sanitation_urban = df_sanitation_urban.round(2)

df_sanitation_rural = wb.data.DataFrame('SH.STA.HYGN.RU.ZS', time = 2017, labels = True)
df_sanitation_rural = df_sanitation_rural[df_sanitation_rural['Country'].isin(studied_countries)]
df_sanitation_rural = df_sanitation_rural.dropna()
df_sanitation_rural = df_sanitation_rural.drop(index ='AFG')
df_sanitation_rural = df_sanitation_rural.round(2)

df_sanitation_ur_and_ru = pd.merge(df_sanitation_urban, df_sanitation_rural, how ='inner', on ='Country')
df_sanitation_ur_and_ru.columns = ['Country', 'Urban', 'Rural']
df_sanitation_ur_and_ru = df_sanitation_ur_and_ru.melt(id_vars ='Country', var_name ='Settlement Type', value_name ='% with Handwashing Facilities')
print(df_sanitation_ur_and_ru)

sns.set_style('darkgrid')
f, plot_sanitation_ur_and_ru = plt.subplots(figsize = (12, 6))
plot_sanitation_ur_and_ru = sns.barplot(x ='Country', y ='% with Handwashing Facilities', hue ='Settlement Type', data = df_sanitation_ur_and_ru, palette = 'husl')
plot_sanitation_ur_and_ru.set_title('Percentage of Population with Handwashing Facilities by Settlement Type by Country in 2017', fontsize = 15, fontweight ='bold')
plot_sanitation_ur_and_ru.set_xlabel('Country', fontsize = 12)
plot_sanitation_ur_and_ru.set_ylabel('% with Handwashing Facilities', fontsize = 12)
plot_sanitation_ur_and_ru.yaxis.set_ticks(np.arange(0, 40, 5))

# Show both plots
plt.show()

