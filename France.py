""" 0. Import des modules utilisés (pandas pour le traitement stat, matplotlib pour les graphiques)"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#j'ai installé openpyxl par la commande pip install openpyxl (pcq vscode)

""" 1. Accès aux données et lecture """
chemin_acces = "/home/onyxia/work/ef_kvaareg__custom_9130147_spreadsheet.xlsx"
ttl_hold_nb = "Sheet 1"  # Nombre total d'exploitations par région française
df_hold = pd.read_excel(chemin_acces, sheet_name=ttl_hold_nb, engine='openpyxl')

""" 2. Tracer un pie chart """

"""2.1 apparemment j'ai des problèmes de NaN donc réglons-les"""
# Afficher les lignes avec des valeurs NaN dans la colonne 'Number of holdings'
nan_rows = df_hold[df_hold['Number of holdings'].isna()]
print(df_hold['Number of holdings'].dtype)
print(nan_rows)

#conversion de la colonne number of holdings en numériques
df_hold['Number of holdings'] = pd.to_numeric(df_hold['Number of holdings'], errors='coerce')
print(df_hold.head(3))
#j'ai compris!!! c'est parce que j'ai des lignes vides au début!
df_hold = df_hold.dropna(subset=['Number of holdings'])

print(df_hold.head(3))

"""2.2 code de construction du graphique"""
labels = df_hold['Geographic indication']
sizes = df_hold['Number of holdings']
plt.pie(sizes, labels=labels, autopct='%1.1f%%')
plt.title('Geographic Repartition of the Agricultural Holdings in France')
plt.show()



"""3. Drawing a bar chart illustrating the total used agricultural area in France, by ha. 
and European NUTS2 regions"""

excel_file_path = "/home/onyxia/work/ef_kvaareg__custom_9130147_spreadsheet.xlsx"
ttl_area_ha = "Sheet 4"  
df_area = pd.read_excel(excel_file_path, sheet_name=ttl_area_ha, engine='openpyxl')

# Drawing a bar chart according to these data
plt.bar(df_area['Geographic indication'],df_area['Used agricultural area (ha)'])
plt.xlabel('Geographic indication')
plt.ylabel('Used agricultural area (ha)')
plt.title('Used Agricultural Area in France by NUTS2 Regions')

#Trying the scientific notation to make it easier to read the bar chart
for i, value in enumerate(df_area['Used agricultural area (ha)']):
    plt.text(i, value + 10000, '{:.2e}'.format(value), ha='center', va='bottom', rotation=90)
plt.xticks(rotation=45, ha='right')
plt.show()

"""4. Drawing a bar chart illustrating the standard economic output, 
in euros, of agriculture, of every french region"""

excel_file_path = "/home/onyxia/work/ef_kvaareg__custom_9130147_spreadsheet.xlsx"
econ_output = "Sheet 7"  
df_output = pd.read_excel(excel_file_path, sheet_name=econ_output, engine='openpyxl')

#Trying a descending order ranking for better understanding of the following bar chart
df_output = df_output.sort_values(by='Standard output (euros)', ascending=False)

#Drawing a bar chart according to these data
plt.bar(df_output['Geographic indication'],df_output['Standard output (euros)'])
plt.xlabel('Geographic indication')
plt.ylabel('Standard output (euros)')
plt.title('Standard Agricultural economic output by NUTS2 Regions')
plt.xticks(rotation=45, ha='right')

#Trying the scientific notation to make it easier to read the bar chart
for i, value in enumerate(df_output['Standard output (euros)']):
    plt.text(i, value + 10000, '{:.2e}'.format(value), ha='center', va='bottom', rotation=90)
plt.show()

"""5. Drawing a pie chart on the main farming type by NUTS2 regions in France"""

csv_file = '/home/onyxia/work/ef_kvftreg__custom_9131585_linear.csv'

# Read the CSV file into a pandas DataFrame
farming_type = pd.read_csv(csv_file)

# Display the first few rows of the DataFrame
print(farming_type.head(50))

# Get the number of types of farms in the dataset
nb_types = farming_type['farmtype'].nunique()
print("There were", nb_types, "different types of farms in Spain in 2010")

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

# Draw the corresponding pie chart
plt.figure(figsize=(8, 8))
plt.pie(farming_type_unique['all_nb_holdings'], labels=farming_type_unique['farmtype'], autopct='%1.1f%%', startangle=90)
plt.title('Repartition of Farm Types in France')
plt.show()