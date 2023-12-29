import geopandas as gpd
import pandas as pd
import contextily as ctx
import matplotlib.pyplot as plt
import cartiflette.s3 as s3
import pyogrio
import fiona
import os
import geodatasets

os.chdir() 
# Le dossier dans lequel vous travaillez ici.

#Il suffit d'avoir dans le path ci-dessus les 4 dossiers (décompressés) correspondant aux années 2022,2021,2020,2019.
#C'est à dire les dossiers: rpg-bio-2019-national.shp, rpg-bio-2020-national.shp, rpg-bio-2021-national.geojson, rpg-bio-2022-national.gpkg.
#Il faut cependant renommer le dossier 2022 et mettre un underscore comme ci-dessous.(rpg-bio-2022-national.gpkg -> rpg-bio-2022-national_.gpkg)

national2022 = gpd.read_file("rpg-bio-2022-national_.gpkg/rpg-bio-2022-national.gpkg")
#J'ai rajouté un underscore dans le nom du dossier car je ne pourrai pas out un fichier portant le même nom que lui sinon.
national2022 = national2022.to_crs(3857)
#Ici je choisi un système de coordonnées arbitraires (crs = 3857) afin d'avoir le même pour toutes les bdds (car elle ne possédait pas toutes le même initialement). Il est très facile d'en changer et celui choisit est donc peu important.
national2022 = national2022.rename(columns={"code_culture":"code_cultu","lbl_culture":"lbl_cultu","grp_culture":"grp_cultu"})
national2022.to_file("rpg-bio-2022-national.gpkg","GPKG")

# for val in national2022.head():
#     print val
#Permet d'afficher l'intégralité des entêtes de colonnes afin d'avoir les mêmes pour toutes les bdds.


national2021 = gpd.read_file("rpg-bio-2021-national.geojson/rpg-bio-2021-national.geojson")
national2021 = national2021.to_crs(3857)
national2021.to_file("rpg-bio-2021-national.gpkg","GPKG")
#Ici simple conversion d'un format geojson à un format gpkg et changement du système de coordonnées pour qu'il soit le même pour toutes les bases


# for val in national2021.head():
#     print(val)


national2020 = gpd.read_file("rpg-bio-2020-national.shp/rpg-bio-2020-national.shp")
national2020 = national2020.to_crs(3857)
national2020 = national2020.rename(columns={"MILLESIME":"millesime","CODE_CULTU":"code_cultu","LBL_CULTU":"lbl_cultu","BIO":"bio","GRP_CULTU":"grp_cultu","SURFACE_HA":"surface_ha"})
national2020.to_file("rpg-bio-2020-national.gpkg","GPKG")
#Conversion d'un format shp vers gpkg et changement des noms des colonnes qui auparavant étaient en majuscules.

# for val in national2020.head():
#     print(val)

national2019 = gpd.read_file("rpg-bio-2019-national.shp/rpg-bio-2019-national.shp")
national2019 = national2019.to_crs(3857)
national2019 = national2019.rename(columns={"MILLESIME":"millesime","CODE_CULTU":"code_cultu","LBL_CULTU":"lbl_cultu","BIO":"bio","GRP_CULTU":"grp_cultu","SURFACE_HA":"surface_ha"})
national2019.to_file("rpg-bio-2019-national.gpkg","GPKG")
#Conversion d'un format shp vers gpkg et changement des noms des colonnes qui auparavant étaient en majuscules.

# for val in national2019.head():
#     print(val)


#Cette partie est purement optionnelle. Il n'est pas forcément judicieux de travailler sur une base de donnée trop importante qui serait trop longue à parcourir.
#Il convient sans doute mieux de travailler avec 4 petites bases de données standardisées.


# merged_data = pd.concat([national2022,national2021,national2020,national2019])

# for val in merged_data.head():
#     print(val)
#Ici un problème qui peut se poser est que seul 2022 possède les données code_epci, code_departement, code_region, zone_geo. Une grosse partie des données est donc rempli de valeurs NaN qu'il va falloir prendre en compte.

# merged_data.to_file("rpg-bio-national-fusion.gpkg","GPKG")
#On enregistre les bdds une fois qu'elles sont toutes fusionnées.
# print(merged_data.head())

# nationalWhole = gpd.read_file("rpg-bio-national-fusion")