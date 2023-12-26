import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pynsee.download

"""1. Drawing a pie chart illustrating the geographic repartition of the agricultural holdings in Greece,
by number of holdings and European NUTS2 regions"""

excel_file_path = "/Users/cyrillefougere/Desktop/ENSAE 2023:2024/S1/Python et Data Science/Databases/Key farm indicators_Greece_NUTS2.xlsx"
ttl_hold_nb = "Sheet 1"  
df_hold = pd.read_excel(excel_file_path, sheet_name=ttl_hold_nb, engine='openpyxl')

# Replacing '(NUTS 2010)' with an empty string in 'Geographic indication'
df_hold['Geographic indication'] = df_hold['Geographic indication'].str.replace(' (NUTS 2010)', '')
print(df_hold)

# Drawing a pie chart according to these data
df_hold_modified = df_hold.iloc[1:]
print(df_hold_modified)
labels = df_hold_modified['Geographic indication']
sizes = df_hold_modified['Number of holdings']
plt.pie(sizes, labels=labels, autopct='%1.1f%%')
plt.title('Répartition géographique des exploitations')
plt.show()

"""2. Drawing a bar chart illustrating the total used agricultural area in Greece, by ha. and European NUTS2 regions"""

excel_file_path = "/Users/cyrillefougere/Desktop/ENSAE 2023:2024/S1/Python et Data Science/Databases/Key farm indicators_Greece_NUTS2.xlsx"
ttl_area_ha = "Sheet 2"  
df_area = pd.read_excel(excel_file_path, sheet_name=ttl_area_ha, engine='openpyxl')

# Replacing '(NUTS 2010)' with an empty string in 'Geographic indication'
df_area['Geographic indication'] = df_area['Geographic indication'].str.replace(' (NUTS 2010)', '')
print(df_area)

# Drawing a bar chart according to these data
plt.bar(df_area['Geographic indication'],df_area['Used agricultural area (ha)'])
plt.xlabel('Geographic indication')
plt.ylabel('Used agricultural area (ha)')
plt.title('Used Agricultural Area in Greece by NUTS2 Regions')
for i, value in enumerate(df_area['Used agricultural area (ha)']):
    plt.text(i, value + 0.1, str(value), ha='center', va='bottom', rotation=45)
plt.xticks(rotation=45, ha='right')
plt.show()

"""3. Trying to get statistics on the main farming type by NUTS2 regions in Greece"""

csv_file = '/Users/cyrillefougere/Desktop/ENSAE 2023:2024/S1/Python et Data Science/Databases/Greece_Type of farming.csv'

# Read the CSV file into a pandas DataFrame
farming_type = pd.read_csv(csv_file)

"""# Display the first few rows of the DataFrame
print(farming_type.head(50))"""

# Getting the number of types of farms in the dataset
nb_types = farming_type['farmtype'].nunique()
print("There were", nb_types, "different types of farms in Greece in 2010")

# Getting a list of strings containing the different values of farmtypes in this dataset
diff_types = farming_type['farmtype'].unique().tolist()
print("The different values of farm types according to the European nomenclature are:", diff_types)

# Create a new column for each farm type and calculate the sum of OBS_VALUE for each TIME_PERIOD
for farm_type in diff_types:
    farming_type[f'nb_holdings_by_type_{farm_type}'] = farming_type.loc[farming_type['farmtype'] == farm_type].groupby('TIME_PERIOD')['OBS_VALUE'].transform('sum')

# Concatenate all the new columns into a single column
farming_type['all_nb_holdings'] = farming_type.apply(lambda row: row.filter(like='nb_holdings_by_type_').sum(), axis=1)

# Drop the individual farm type columns
farming_type.drop(columns=[f'nb_holdings_by_type_{farm_type}' for farm_type in diff_types], inplace=True)

#print(farming_type.head(50))

#Replacing the 'farmtype' labels with new values using a dictionnary :
nomenclature_dic = {
    "FT15_SO" : "Specialist cereals, oilseed and protein crops"
    "FT16_SO" : "General field cropping"
    "FT21_SO" : "Specialist horticulture indoor"
    "FT22_SO" :
    "FT23_SO" :
    "FT35_SO" :
    "FT36_SO" :
    "FT37_SO" :
    "FT38_SO" :
    "FT45_SO" :
    "FT46_SO" :
    "FT47_SO" :
    "FT48_SO" :
    "FT51_SO" :
    "FT52_SO" :
    "FT53_SO" :
    "FT61_SO" :
    "FT73_SO" :
    "FT74_SO" :
    "FT83_SO" :
    "FT84_SO" :
    "FT90_SO" :
}

#Drawing the corresponding pie chart
farming_type_unique = farming_type[['farmtype', 'all_nb_holdings']].drop_duplicates()
plt.figure(figsize=(8, 8))
plt.pie(farming_type_unique['all_nb_holdings'], labels=farming_type_unique['farmtype'], autopct='%1.1f%%', startangle=90)
plt.title('Repartition of Farm Types in Greece')
plt.show()

