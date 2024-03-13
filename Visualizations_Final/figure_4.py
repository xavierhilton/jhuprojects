import pandas as pd
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.palettes import Bokeh3
import project_functions as pf

"""
The purpose of this script is to generate the visualization seen in Figure 4.
"""

# Use pandas to convert csv inputs into dataframes
calista = pd.read_csv("calista.csv")
swak = pd.read_csv("swak2001.csv")

# Filter out all sites that the two datasets have in common
sites = list(calista["QD250NAME"].unique())
sites.remove('Hagemeister Island')
# years is to differentiate the two surveys, as Calista is taken in 1974 and SWAK2001 in 2001
years = ["1974","2001"]

metrics = ["AS_ICP40","AS_AA", "SE_AA"]
sites_years = [(site, year) for site in sites for year in years]
wt_overall = []
for metric in metrics:
    # This for loop is to bundle up all the concentrations into a format that is processable by Bokeh
    cal_set = pf.get_site_averages(calista, metric, sites)
    swak_set = pf.get_site_averages(swak, metric, sites)
    combine = sum(zip(cal_set, swak_set), ())
    wt_overall.append(combine)
# Data is inputted into a dictionary and made into a ColumnDataSource
data = dict(site_year = sites_years, AS_ICP40 = wt_overall[0], AS_AA = wt_overall[1], SE_AA = wt_overall[2])
data_cds = ColumnDataSource(data)

plot = figure(x_range = FactorRange(*sites_years), toolbar_location = None, width = 1100,
              title = "Arsenic and Selenium ICP40/AA Comparisons Between Calista, SWAK2001 Datasets")
# I used a vbar_stack to better display all the data that I had, as it consisted of multiple metrics and would not take up as much space
plot.vbar_stack(metrics, x = 'site_year', width = 0.9, alpha = 0.5,
                fill_color = Bokeh3,
                legend_label = metrics, source = data_cds)
# Adjust settings about plot axes, grid, and legend
plot.x_range.range_padding = 0.05
plot.xaxis.major_label_orientation = 1
plot.xgrid.grid_line_color = None
plot.legend.location = "top_left"
plot.yaxis.axis_label = "PPM"
show(plot)

