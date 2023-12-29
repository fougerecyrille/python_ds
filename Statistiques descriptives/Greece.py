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

# Sorting regions of Spain based on the number of agricultural holdings in descending order
sizes = sizes.sort_values(ascending=False)

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

#Sorting the values in descending order to make it easier to read the bar chart 
df_area = df_area.sort_values(by='Used agricultural area (ha)', ascending=False)

# Drawing a bar chart according to these data
plt.bar(df_area['Geographic indication'],df_area['Used agricultural area (ha)'], color = "g")
plt.xlabel('Geographic indication')
plt.ylabel('Used agricultural area (ha)')
plt.title('Used Agricultural Area in Greece by NUTS2 Regions')
plt.xticks(rotation=45, ha='right')

# Trying the scientific notation to make it easier to read the bar chart
for i, value in enumerate(df_area['Used agricultural area (ha)']):
    if i < len(df_area) // 2:
        plt.text(i, value + 10000, '{:.2e}'.format(value), ha='center', va='top', rotation=90, color="white")
    else:
        plt.text(i, value - 10000, '{:.2e}'.format(value), ha='center', va='bottom', rotation=90)

plt.show()

"""3. Drawing a pie chart on the main farming type by NUTS2 regions in Greece"""

csv_file = '/Users/cyrillefougere/Desktop/ENSAE 2023:2024/S1/Python et Data Science/Databases/Greece_Type of farming.csv'

# Read the CSV file into a pandas DataFrame
farming_type = pd.read_csv(csv_file)

"""# Display the first few rows of the DataFrame
print(farming_type.head(50))"""

# Get the number of types of farms in the dataset
nb_types = farming_type['farmtype'].nunique()
print("There were", nb_types, "different types of farms in Greece in 2010")

# Get a list of strings containing the different values of farmtypes in this dataset
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

# Replace the 'farmtype' labels with new values using a dictionnary :
nomenclature_dic = {
    "FT15_SO" : "Specialist cereals, oilseed and protein crops",
    "FT16_SO" : "General field cropping",
    "FT21_SO" : "Specialist horticulture indoor",
    "FT22_SO" : "Specialist horticulture outdoor",
    "FT23_SO" : "Other horticulture",
    "FT35_SO" : "Specialist vineyards",
    "FT36_SO" : "Specialist fruit and citrus fruits",
    "FT37_SO" : "Specialist olives",
    "FT38_SO" : "Various permanent crops combined",
    "FT45_SO" : "Specialist dairying",
    "FT46_SO" : "Specialist cattle-rearing and fattening",
    "FT47_SO" : "Cattle-dayring, rearing and fattening combined",
    "FT48_SO" : "Sheep, goats and other grazing livestock",
    "FT51_SO" : "Specialist pigs",
    "FT52_SO" : "Specialist poultry",
    "FT53_SO" : "Various granivores combined",
    "FT61_SO" : "Mixed cropping",
    "FT73_SO" : "Mixed livestock, mainly grazing livestock",
    "FT74_SO" : "Mixed livestock, mainly granivores",
    "FT83_SO" : "Field crops-grazing livestock combined",
    "FT84_SO" : "Various crops and livestock combined",
    "FT90_SO" : "Non-classified farms"
}
farming_type_unique = farming_type[['farmtype', 'all_nb_holdings']].drop_duplicates()
farming_type_unique['farmtype'] = farming_type_unique['farmtype'].replace(nomenclature_dic)
print(farming_type_unique)

# Sort the types of farms based on the number of holdings in descending order
farming_type_unique = farming_type_unique.sort_values(by='all_nb_holdings', ascending=False)

# Draw the corresponding pie chart
plt.figure(figsize=(8, 8))
plt.pie(farming_type_unique['all_nb_holdings'], labels=farming_type_unique['farmtype'], autopct='%1.1f%%', startangle=90)
plt.title('Repartition of Farm Types in Greece')
plt.show()

"""4. Drawing a bar chart illustrating the standard economic output, 
in euros, of agriculture, of every Greek region"""

excel_file_path = "/Users/cyrillefougere/Desktop/ENSAE 2023:2024/S1/Python et Data Science/Databases/Key farm indicators_Greece_NUTS2.xlsx"
econ_output = "Sheet 5"  
df_output = pd.read_excel(excel_file_path, sheet_name=econ_output, engine='openpyxl')

# Replacing '(NUTS 2010)' with an empty string in 'Geographic indication'
df_output['Geographic indication'] = df_output['Geographic indication'].str.replace(' (NUTS 2010)', '')
print(df_output)

#Trying a descending order ranking for better understanding of the following bar chart
df_output = df_output.sort_values(by='Standard economic output (euros)', ascending=False)

# Drawing a bar chart according to these data
plt.bar(df_output['Geographic indication'],df_output['Standard economic output (euros)'], color = "g")
plt.xlabel('Geographic indication')
plt.ylabel('Standard economic output (euros)')
plt.title('Standard Agricultural economic output by NUTS2 Regions')
plt.xticks(rotation=45, ha='right')

# Trying the scientific notation to make it easier to read the bar chart
for i, value in enumerate(df_output['Standard economic output (euros)']):
    if i < len(df_output) // 2:
        plt.text(i, value + 10000, '{:.2e}'.format(value), ha='center', va='top', rotation=90, color="white")
    else:
        plt.text(i, value - 10000, '{:.2e}'.format(value), ha='center', va='bottom', rotation=90)

plt.show()