# If you don't have geopandas installed, uncomment the following line:
# !pip install geopandas

import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Data: ISO3 country codes and associated numeric values
path="C:\\Users\\Arthur\\Documents\\Linkedin data\\"
data=pd.read_excel(path+"iMaPP_database-2024-12-2.xlsx", 
    sheet_name="MaPP", usecols="AN:AP", skiprows=72, nrows=136, header=0)
df = pd.DataFrame(data)
df.columns

# Read a world dataset from a GeoJSON file
# Using Natural Earth data hosted on GitHub (110m resolution)
geojson_url = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_admin_0_countries.geojson"
world = gpd.read_file(geojson_url)

# Inspect the columns to find the ISO3 column name
# print(world.columns)
# From inspection, we see 'ADM0_A3' is commonly the ISO-3 country code column in Natural Earth data.

# Merge the DataFrame with the GeoDataFrame
merged = world.merge(df, how='left', left_on='ADM0_A3', right_on='iso3')
merged['value'] = pd.to_numeric(merged['value'], errors='coerce')

# Create a choropleth map
fig, ax = plt.subplots(1, 1, figsize=(15,10))
merged.plot(
    column='value',
    cmap='RdYlGn_r',
    legend=False,
    missing_kwds={
        "color": "white",
        "edgecolor": "black",
        "linewidth": 0.5,
        "hatch": "",
        "label": "No Data"
    },
    ax=ax
)

# Create a scalar mappable for the colorbar
sm = plt.cm.ScalarMappable(cmap='RdYlGn_r', norm=plt.Normalize(
    vmin=merged['value'].min(), 
    vmax=merged['value'].max()
))
sm._A = []  # dummy array for the scalar mappable

cbar = fig.colorbar(
    sm, 
    ax=ax, 
    orientation='horizontal',   # Set orientation to horizontal
    fraction=0.033,            # Size of the colorbar (default is 0.15)
    pad=0.04                   # Distance from the plot (default is 0.04)
)
cbar.set_label(
    "Cumulative sum of MPru measures for the last 5 years",
    fontsize=14,
    fontweight='bold',
    color='grey'
)
ax.text(
    0.07, 0.07, 
    "Data from IMF's iMaPP database.\n Chart prepared by Arthur Grigoryan, CFA",
    fontsize=12,
    #fontweight='bold',
    fontstyle='italic',
    color='grey',
    rotation=90,
    fontfamily='sans-serif',
    transform=ax.transAxes,        # use axes-relative coordinates
    ha='left',                     # horizontally align left
    va='bottom',                   # vertically align bottom
)

ax.set_title("Relative tightness of Macroprudential \n policy  across countries", fontsize=20, fontweight='bold', color='black')
ax.set_axis_off()

#plt.tight_layout()
plt.show()


