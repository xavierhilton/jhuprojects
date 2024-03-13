import pandas as pd
import numpy as np
from bokeh.plotting import figure, ColumnDataSource, show
from bokeh.models import WMTSTileSource, CategoricalColorMapper
from bokeh.palettes import Category20_10
from bokeh.layouts import row

"""
The purpose of this script is to generate the visualization seen in Figure 1.
"""

def get_mercator(df, lon = "Long", lat = 'Lat'):
    """
    The get_mercator function serves to convert longitude and lattitude coordinates into mercator form
    :param df: input database
    :param lon: longitude coordinate
    :param lat: latitude coordinate
    :return: df with 2 additional columns with converted mercator coordinates
    """
    k = 6378137
    df['x'] = df[lon] * (k*np.pi/180.0)
    df['y'] = np.log(np.tan((90 + df[lat])*np.pi/360.0))*k
    return df

# Use pandas to convert csv inputs into dataframes
calista = pd.read_csv("calista.csv")
swak = pd.read_csv("swak2001.csv")

# Filter out all sites that the two datasets have in common
sites = list(calista["QD250NAME"].unique())
sites.remove('Hagemeister Island')

calista_coords = pd.DataFrame()
for index, iter in enumerate(sites):
    # This for loop extracts the site name, sample name, and coordinates of the sample for the Calista dataset
    # Although sample name is not used
    calista_subset = calista[calista["QD250NAME"] == iter]
    site = calista_subset["QD250NAME"]
    sample = calista_subset["REC_NO"]
    lat = calista_subset["LAT"]
    long = calista_subset["LONG"]
    coords = pd.DataFrame(zip(site, sample, lat, long), columns=["Site","Sample", "Lat", "Long"])
    calista_coords = pd.concat([calista_coords, coords])

swak_coords = pd.DataFrame()
for index, iter in enumerate(sites):
    # This for loop extracts the site name, sample name, and coordinates of the sample for the SWAK2001 dataset
    # Although sample name is not used
    swak_subset = swak[swak["QD250NAME"] == iter]
    site = swak_subset["QD250NAME"]
    sample = swak_subset["REC_NO"]
    lat = swak_subset["LAT"]
    long = swak_subset["LONG"]
    coords = pd.DataFrame(zip(site, sample, lat, long), columns=["Site","Sample", "Lat", "Long"])
    swak_coords = pd.concat([swak_coords, coords])

# Convert coordinates into mercator coordinates
processed_cords = get_mercator(calista_coords)
processed_cords_swak = get_mercator(swak_coords)
# Convert dataframe into graphable ColumnDataSource
calista_source = ColumnDataSource(processed_cords)
swak_source = ColumnDataSource(processed_cords_swak)
# Set x and y ranges for the map
x_range = (pd.DataFrame.min(calista_coords['x']), pd.DataFrame.max(calista_coords['x']))
y_range = (pd.DataFrame.min(calista_coords['y']), pd.DataFrame.max(calista_coords['y']))
# Create the Calista map plot
calista_plot = figure(x_range = x_range, y_range = y_range, x_axis_type = 'mercator', y_axis_type = 'mercator',
                      title = "Locations of Samples Collected in Calista Dataset - 1974", height = 600, width = 600, toolbar_location = None)
# URL and WMTSTileSource are used to generate the map behind the coordinates
url = "http://a.basemaps.cartocdn.com/rastertiles/voyager/{Z}/{X}/{Y}.png"
calista_plot.add_tile(WMTSTileSource(url = url))
# Create the SWAK2001 map plot
swak_plot = figure(x_range = x_range, y_range = y_range, x_axis_type = 'mercator', y_axis_type = 'mercator',
                   title = "Locations of Samples Collected in SWAK2001 Dataset - 2001", height = 600, width = 600, toolbar_location = None)
# URL and WMTSTileSource are used to generate the map behind the coordinates
swak_plot.add_tile(WMTSTileSource(url = url))
# I added a Mapper to help make different sites different colors
mapper = CategoricalColorMapper(factors = list(processed_cords['Site'].unique()), palette = Category20_10)
# Map coordinates for both sites
calista_plot.circle(source = calista_source, x= 'x', y = 'y', size = 5, color ={'field': 'Site', 'transform': mapper}, legend_group = 'Site')
swak_plot.triangle(source = swak_source, x = 'x', y = 'y', size = 5, color ={'field': 'Site', 'transform': mapper}, legend_group = 'Site')
# Adjust legend components
calista_plot.legend.location = 'top_right'
calista_plot.legend.title = 'Calista Sites'
swak_plot.legend.location = 'top_right'
swak_plot.legend.title = 'SWAK2001 Sites'

show(row(calista_plot, swak_plot))


