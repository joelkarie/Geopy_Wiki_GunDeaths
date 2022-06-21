from numpy import dtype
import pandas as pd
import geopandas
import folium

# Url for Wikipedia sight
url = 'https://en.wikipedia.org/wiki/List_of_countries_by_firearm-related_death_rate'

# Create pandas dataframes from Wikikpedia content
tables = pd.read_html(url)

# Data is in the third[2] table
table = tables[2]

# Adjust display options for VS Code
pd.set_option('display.max_columns', 20)
pd.set_option('display.max_rows', 200)
pd.set_option('display.width', 200)

# Import world map from geopandas
world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))

# Merge data into a single table
table = world.merge(table, how='left', left_on=['name'], right_on=['Country'])

# Clean the data
table = table.dropna(subset=['Total']) # drop empty rows
table = table[pd.to_numeric(table['Total'], errors='coerce').notnull()]
table['Total'] = table['Total'].astype(float)
print(table[["Country","Total"]])

# Get empty map from folium
my_map = folium.Map()

# Add data to map for choropleth map
folium.Choropleth(
    geo_data=table,
    name="choropleth",
    data=table,
    columns=["Country", "Total"],
    key_on="feature.properties.name",
    fill_color="BuPu",
    fill_opacity=0.7,
    line_opacity=0.5,
    legend_name="Gun Deaths",
).add_to(my_map)

# Save map as html
my_map.save('total_gun_deaths.html')