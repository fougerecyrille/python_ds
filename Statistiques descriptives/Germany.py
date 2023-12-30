import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pynsee.download

"""1. Drawing a pie chart illustrating the geographic repartition of the agricultural holdings in Italy,
by number of holdings and European NUTS2 regions"""

excel_file_path = "/Users/cyrillefougere/Desktop/ENSAE 2023:2024/S1/Python et Data Science/Databases/Key farm indicators_Germany_NUTS2.xlsx"
ttl_hold_nb = "Sheet 1"  
df_hold = pd.read_excel(excel_file_path, sheet_name=ttl_hold_nb, engine='openpyxl')

# Eliminating the row for the 'Berlin, Bremen, Hamburg' geographic indication
indentifying_value = 'Berlin, Bremen, Hamburg'
df_hold=df_hold[df_hold["Geographic indication"] !=indentifying_value]

# Drawing a pie chart according to these data
labels = df_hold['Geographic indication']
sizes = df_hold['Number of holdings']

#Sorting regions of Germany based on the number of agricultural holdings in descending order
sizes = sizes.sort_values(ascending=False)

plt.pie(sizes, labels=labels, autopct='%1.1f%%')
plt.title('Geographic Repartition of the Agricultural Holdings in Germany, by number of holdings and NUTS2 Region')
plt.show()

"""2. Drawing a bar chart illustrating the total used agricultural area in Italy, by ha. and European NUTS2 regions"""

excel_file_path = "/Users/cyrillefougere/Desktop/ENSAE 2023:2024/S1/Python et Data Science/Databases/Key farm indicators_Germany_NUTS2.xlsx"
ttl_area_ha = "Sheet 2"  
df_area = pd.read_excel(excel_file_path, sheet_name=ttl_area_ha, engine='openpyxl')

# Eliminating the row for the 'Berlin, Bremen, Hamburg' geographic indication
indentifying_value = 'Berlin, Bremen, Hamburg'
df_area=df_area[df_area["Geographic indication"] !=indentifying_value]

# Sorting the x-axis labels by descending order on the y-axis values
df_area=df_area.sort_values(by="Used agricultural area (ha)", ascending=False)

# Drawing a bar chart according to these data
plt.bar(df_area['Geographic indication'],df_area['Used agricultural area (ha)'], color = "g")
plt.xlabel('Geographic indication')
plt.ylabel('Used agricultural area (ha)')
plt.title('Used Agricultural Area in Germany by NUTS2 Regions')
plt.xticks(rotation=45, ha='right')

# Trying the scientific notation to make it easier to read the bar chart
for i, value in enumerate(df_area['Used agricultural area (ha)']):
    if i < len(df_area) // 2:
        plt.text(i, value + 10000, '{:.2e}'.format(value), ha='center', va='top', rotation=90, color="white")
    else:
        plt.text(i, value - 10000, '{:.2e}'.format(value), ha='center', va='bottom', rotation=90)

plt.show()

"""3. Drawing a bar chart illustrating the standard economic output, 
in euros, of agriculture, of every Italian region"""

excel_file_path = "/Users/cyrillefougere/Desktop/ENSAE 2023:2024/S1/Python et Data Science/Databases/Key farm indicators_Germany_NUTS2.xlsx"
econ_output = "Sheet 5"  
df_output = pd.read_excel(excel_file_path, sheet_name=econ_output, engine='openpyxl')

# Eliminating the row for the 'Berlin, Bremen, Hamburg' geographic indication
indentifying_value = 'Berlin, Bremen, Hamburg'
df_output=df_output[df_output["Geographic indication"] !=indentifying_value]

#Trying a descending order ranking for better understanding of the following bar chart
df_output = df_output.sort_values(by='Standard output (euros)', ascending=False)

#Drawing a bar chart according to these data
plt.bar(df_output['Geographic indication'],df_output['Standard output (euros)'], color = "g")
plt.xlabel('Geographic indication')
plt.ylabel('Standard output (euros)')
plt.title('Standard Agricultural economic output by NUTS2 Regions in Italy, in euros')
plt.xticks(rotation=45, ha='right')

# Trying the scientific notation to make it easier to read the bar chart
for i, value in enumerate(df_output['Standard output (euros)']):
    if i < len(df_output) // 2:
        plt.text(i, value + 10000, '{:.2e}'.format(value), ha='center', va='top', rotation=90, color="white")
    else:
        plt.text(i, value - 10000, '{:.2e}'.format(value), ha='center', va='bottom', rotation=90)

plt.show()

"""4. Drawing a pie chart on the main farming type by NUTS2 regions in Germany

csv_file = '/Users/cyrillefougere/Desktop/ENSAE 2023:2024/S1/Python et Data Science/Databases/Germany_Type of farming.csv'

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

# Sort the types of farms based on the number of holdings in descending order
farming_type_unique = farming_type_unique.sort_values(by='all_nb_holdings', ascending=False)

# Draw the corresponding pie chart
plt.figure(figsize=(8, 8))
plt.pie(farming_type_unique['all_nb_holdings'], labels=farming_type_unique['farmtype'], autopct='%1.1f%%', startangle=90)
plt.title('Repartition of Farm Types in Germany')
plt.show()
"""

"""4. Drawing a pie chart on the main farming type by NUTS2 regions in Germany"""

csv_file = '/Users/cyrillefougere/Desktop/ENSAE 2023:2024/S1/Python et Data Science/Databases/Germany_Type of farming.csv'

# Read the CSV file into a pandas DataFrame
farming_type = pd.read_csv(csv_file)

# Create a dictionnary which will be later used to replace the abstract nomenclature with more descriptibe labels
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

# Replace farmtype codes with descriptive names
farming_type['farmtype'] = farming_type['farmtype'].replace(nomenclature_dic)

# Sum the number of holdings for each farm type
farming_type_summary = farming_type.groupby('farmtype')['OBS_VALUE'].sum().reset_index(name='Total Holdings')

# Calculate the percentage of holdings for each farm type
farming_type_summary['Percentage'] = farming_type_summary['Total Holdings'] / farming_type_summary['Total Holdings'].sum() * 100

# Identify farm types with less than 1% of the total holdings
small_farm_types = farming_type_summary[farming_type_summary['Percentage'] < 1.5]

# Create a new DataFrame combining major types and "Other crops"
major_types = farming_type_summary[farming_type_summary['Percentage'] >= 1.5]
other_crops_row = pd.DataFrame({'farmtype': ['Other crops'], 'Total Holdings': [small_farm_types['Total Holdings'].sum()]})
other_crops_row['Percentage'] = other_crops_row['Total Holdings'] / farming_type_summary['Total Holdings'].sum() * 100
farming_type_combined = pd.concat([major_types, other_crops_row], ignore_index=True)

# Draw the corresponding pie chart
plt.figure(figsize=(8, 8))

# Set a custom color cycle with distinct colors for adjacent slices
custom_colors = plt.cm.tab20c.colors  # You can use a different colormap if needed
plt.gca().set_prop_cycle('color', custom_colors)

# Draw the pie chart without labels for legend
wedges, _, autotexts = plt.pie(
    farming_type_combined['Total Holdings'],
    labels=None,
    autopct='%1.1f%%',  # Specify autopct to include percentages
    startangle=90,
    pctdistance=0.85,
)

# Extract percentages from autopct
percentages = [float(autotext.get_text()[:-1]) for autotext in autotexts]

# Draw the legend outside the plot area with labels and percentages
legend_labels = [f'{label} ({percentage:.1f}%)' for label, percentage in zip(farming_type_combined['farmtype'], percentages)]
legend = plt.legend(wedges, legend_labels, title='Farm Types', loc='center left', bbox_to_anchor=(1, 0, 0.5, 1))

# Set the legend to display labels and percentages in a single column
for label, percentage in zip(legend_labels, percentages):
    legend.texts[legend_labels.index(label)].set_text(f'{label}\n{percentage:.1f}%')

plt.title('Repartition of Farm Types in Germany, based on the number of holdings')

plt.show()

"""5. Drawing a pie chart plotting the distribution of the used agricultural 
area in Germany by farm types."""

csv_file = "/Users/cyrillefougere/Desktop/ENSAE 2023:2024/S1/Python et Data Science/Databases/Germany_Non-Organic_Used area (ha).csv"

# Load the CSV file into a DataFrame
df = pd.read_csv(csv_file)

# Replace farmtype codes with descriptive names
crop_type_dic = {
    "FT15_SO": "Cereals, Oilseeds, and Protein Crops",
    "FT16_SO": "General Field Cropping",
    "FT21_SO": "Specialist horticulture indoor",
    "FT22_SO": "Specialist horticulture outdoor",
    "FT23_SO": "Other horticulture",
    "FT35_SO": "Specialist vineyards",
    "FT36_SO": "Specialist fruit and citrus fruits",
    "FT37_SO": "Specialist olives",
    "FT38_SO": "Various permanent crops combined",
    "FT45_SO": "Specialist dairying",
    "FT46_SO": "Specialist cattle-rearing and fattening",
    "FT47_SO": "Cattle-dayring, rearing and fattening combined",
    "FT48_SO": "Sheep, goats and other grazing livestock",
    "FT51_SO": "Specialist pigs",
    "FT52_SO": "Specialist poultry",
    "FT53_SO": "Various granivores combined",
    "FT61_SO": "Mixed cropping",
    "FT73_SO": "Mixed livestock, mainly grazing livestock",
    "FT74_SO": "Mixed livestock, mainly granivores",
    "FT83_SO": "Field crops-grazing livestock combined",
    "FT84_SO": "Various crops and livestock combined",
    "FT90_SO": "Non-classified farms"
}

df['farmtype'] = df['farmtype'].replace(crop_type_dic)

# Sum the used agricultural area for each farm type
area_summary = df.groupby('farmtype')['OBS_VALUE'].sum().reset_index(name='Total Area (ha)')

# Calculate the percentage of total area for each farm type
area_summary['Percentage'] = area_summary['Total Area (ha)'] / area_summary['Total Area (ha)'].sum() * 100

# Identify farm types with less than 1.5% of the total area
small_farm_types = area_summary[area_summary['Percentage'] < 1.5]

# Replace farm types with less than 1.5% of the total area with "Other crops"
df.loc[df['farmtype'].isin(small_farm_types['farmtype']), 'farmtype'] = 'Other crops'

# Sum the used agricultural area for each farm type after aggregation
area_summary_filtered = df.groupby('farmtype')['OBS_VALUE'].sum().reset_index(name='Total Area (ha)')

# Calculate the percentage of total area for each farm type after aggregation
area_summary_filtered['Percentage'] = area_summary_filtered['Total Area (ha)'] / area_summary_filtered['Total Area (ha)'].sum() * 100

# Draw the pie chart without labels around it
plt.figure(figsize=(12, 8))
custom_colors = plt.cm.tab20c.colors
plt.gca().set_prop_cycle('color', custom_colors)
wedges, _, autotexts = plt.pie(
    area_summary_filtered['Total Area (ha)'],
    labels=None,  # No labels around the pie chart
    autopct='%1.1f%%',  # Display percentages in the pie chart
    startangle=90,
    pctdistance=0.85,
)

# Add legend to the right of the pie chart with color and percentage
legend_labels = [f'{label} ({percentage:.1f}%)' for label, percentage in
                 zip(area_summary_filtered['farmtype'], area_summary_filtered['Percentage'])]
plt.legend(area_summary_filtered['farmtype'], title='Crop Types', bbox_to_anchor=(1, 0.5), loc='center left',
           labels=legend_labels)

plt.title('Distribution of Used Agricultural Area by Farm Type, in Germany')
plt.show()