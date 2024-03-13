import pandas as pd
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.palettes import Category10_8
import project_functions as pf

"""
The purpose of this script is to generate the visualization seen in Figure 2.
"""

# Use pandas to convert csv inputs into dataframes
calista = pd.read_csv("calista.csv")
swak = pd.read_csv("swak2001.csv")

# Filter out all sites that the two datasets have in common
sites = list(calista["QD250NAME"].unique())
sites.remove('Hagemeister Island')
# years is to differentiate the two surveys, as Calista is taken in 1974 and SWAK2001 in 2001
years = ["1974","2001"]
metrics = ["AL_ICP40", "FE_ICP40","MG_ICP40", "TI_ICP40", "AU_ICP40", "AG_ICP40", "HG_AA", "PB_ICP40"]
sites_years = [(site, year) for site in sites for year in years]

wt_overall = []
for metric in metrics:
    # This for loop is to bundle up all the concentrations into a format that is processable by Bokeh
    cal_set = pf.get_site_averages(calista, metric, sites)
    swak_set = pf.get_site_averages(swak, metric, sites)
    combine = sum(zip(cal_set, swak_set), ())
    wt_overall.append(combine)
# Data is inputted into a dictionary and made into a ColumnDataSource
data = dict(site_year = sites_years, AL_ICP40 = wt_overall[0], FE_ICP40 = wt_overall[1], MG_ICP40 = wt_overall[2],
            TI_ICP40 = wt_overall[3], AU_ICP40 = wt_overall[4], AG_ICP40 = wt_overall[5], HG_AA = wt_overall[6], PB_ICP40 = wt_overall[7])
data_cds = ColumnDataSource(data)
plot = figure(x_range = FactorRange(*sites_years), toolbar_location = None, width = 1100,
              title = "ICP40/AA Metric Comparisons Between Calista, SWAK2001 Datasets")
# I used a vbar_stack to better display all the data that I had, as it consisted of multiple metrics and would not take up as much space
plot.vbar_stack(metrics, x = 'site_year', width = 0.9, alpha = 0.5,
                color = Category10_8,
                legend_label = metrics, source = data_cds)
# Adjust settings about plot axes, grid, and legend
plot.x_range.range_padding = 0.05
plot.xaxis.major_label_orientation = 1
plot.xgrid.grid_line_color = None
plot.legend.location = "top_left"
plot.legend.orientation = "horizontal"
plot.yaxis.axis_label = "Weight Percent (%)/PPM"
show(plot)
