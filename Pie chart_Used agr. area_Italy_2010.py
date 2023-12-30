import pandas as pd
import matplotlib.pyplot as plt

csv_file = "/Users/cyrillefougere/Desktop/ENSAE 2023:2024/S1/Python et Data Science/Databases/Italy_Non-Organic_Types of crops_Used area (ha).csv"

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

plt.title('Distribution of Used Agricultural Area by Farm Type')
plt.show()
