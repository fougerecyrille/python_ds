"""4. Drawing a pie chart on the main farming type by NUTS2 regions in Italy"""


csv_file = '/Users/cyrillefougere/Desktop/ENSAE 2023:2024/S1/Python et Data Science/Databases/Italy_Type of farming.csv'

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

plt.title('Repartition of Farm Types in Italy')

plt.show()
