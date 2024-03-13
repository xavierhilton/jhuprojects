import pandas as pd
import project_functions as pf

"""
The function of this program is to create the "master data table". Ultimately, this entails listing the average of every
metric for every site across the two years of study, 1974 and 2001.
"""

# Use pandas to convert csv inputs into dataframes
calista = pd.read_csv("calista.csv")
swak = pd.read_csv("swak2001.csv")

# Filter out all sites that the two datasets have in common
sites = list(calista["QD250NAME"].unique())
sites.remove('Hagemeister Island')
# years is to differentiate the two surveys, as Calista is taken in 1974 and SWAK2001 in 2001
years = ["1974","2001"]

column_names = pf.return_metrics(calista)

master_table = pd.DataFrame()
# Multiindex is used to provide a more complex categorization to better highlight the changes between the columns.
# The upper index represents the metric, while the lower index highlights the years of the studies
multiindex = pd.MultiIndex.from_product([column_names, years], names = ['Measurement', 'Year'])

for value in column_names:
    # This for loop is to bundle up all the concentrations into a format that is processable by pandas
    calista_vals = pf.get_site_averages(calista, value, sites)
    swak_vals = pf.get_site_averages(swak, value, sites)
    paired_vals = pd.DataFrame(zip(calista_vals, swak_vals))
    master_table = pd.concat([master_table, paired_vals], axis = 1, ignore_index = True)
# Data is extracted and reprocessed by adding the column and index labels
data = master_table.get(master_table.columns.values)
master_table = pd.DataFrame(data = data[0:len(data)].values, index = sites, columns = multiindex)
# Finished table is exported as CSV
master_table.to_csv("master_data_table.csv", sep = ',')
