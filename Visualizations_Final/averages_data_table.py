import pandas as pd
import project_functions as pf

"""
This program is designed to create Appendix A, which highlights the relative change in concentrations from 1974 to 2001
"""

# Use pandas to convert csv inputs into dataframes
calista = pd.read_csv("calista.csv")
swak = pd.read_csv("swak2001.csv")

# Filter out all sites that the two datasets have in common
sites = list(calista["QD250NAME"].unique())
sites.remove('Hagemeister Island')
# years is to differentiate the two surveys, as Calista is taken in 1974 and SWAK2001 in 2001
years = ["1974","2001"]

# Gather all metrics
column_names = pf.return_metrics(calista)

averages_table = pd.DataFrame()

for value in column_names:
    averages = []
    calista_vals = pf.get_site_averages(calista, value, sites)
    swak_vals = pf.get_site_averages(swak, value, sites)
    for calista_val, swak_val in zip(calista_vals, swak_vals):
        if calista_val == 0:
            if swak_val == 0:
                # If both values in SWAK2001 and Calista are 0 - this is to prevent division by 0
                averages.append(0)
            else:
                # This highlights a noticeable change from 0 in Calista to some positive value in SWAK2001
                # Since the relative % change would be infinity, I made it a noticeably large number, which is highlighted in the footnote for the table
                averages.append(999999)
        else:
            averages.append((swak_val - calista_val)/calista_val*100)
    averages = ['%.2f' % average for average in averages]
    averages_table = pd.concat([averages_table, pd.DataFrame(averages)], axis = 1, ignore_index = True)
# Label the columns and indices, transpose for better viewing, and export as csv
averages_table.columns = column_names
averages_table.index = sites
averages_table = averages_table.transpose()
averages_table.to_csv("percent_change_elements_table.csv", sep = ',')