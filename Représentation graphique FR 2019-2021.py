import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import os
from matplotlib.colors import ListedColormap

os.chdir() #Dossier dans lequel on travaille.

year = "2019"

file1_path = "rpg-bio-"+year+"-national.gpkg"
national = gpd.read_file(file1_path)

# Utilisation d'un site (https://france-geojson.gregoiredavid.fr) permettant d'obtenir un GeoDataFrame des régions de la France.
file2_path = "regions.geojson"
regions_france = gpd.read_file(file2_path)
regions_france = regions_france.to_crs(3857)

fig, ax = plt.subplots()

national.plot(column="bio", cmap=ListedColormap(['green']), legend=False, ax=ax)
ax.set_xlim(-1*(10**6), 1.5*(10**6))
ax.set_ylim(5*(10**6), 6.75*(10**6))

regions_france.boundary.plot(ax=ax, color='black')

plt.title("Parcelles en AB déclarées à la PAC en "+year)
plt.show()