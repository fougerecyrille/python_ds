import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load your CSV data into a DataFrame
or_farming = pd.read_csv('/Users/cyrillefougere/Desktop/ENSAE 2023:2024/S1/Python et Data Science/Databases/Organic farming_G5_ha.csv')
print(or_farming.sample(25))

# Convert column names to lower case for case-insensitivity 
or_farming.columns = or_farming.columns.str.lower()

# Replace cultures and crops names with others 
dtld_nomenclature = {
    "UAAXK0000" : "Utilised agricultural area excluding kitchen gardens",
    "ARA" : "Arable land",
    "C0000" : "Cereals for the production of grain (including seed)",
    "C1000" : "Cereals (excluding rice) for the production of grain (including seed)",
    "C1100" : "Wheat and spelt",
    "C1110" : "Common wheat and spelt",
    "C1120" : "Durum wheat",
    "C1200" : "Rye and winter cereals mixture (maslin)",
    "C1300" : "Barley",
    "C1400" : "Oats and spring cereal mixtures (mixed grain other than maslin)",
    "C1500" : "Grain maize and corn-cob-mix",
    "C1600_1700_1900" : "Other cereals (including triticale and sorghum)",
    "C1600" : "Triticale",
    "C1700" : "Sorghum",
    "C2000" : "Rice",
    "P0000" : "Dry pulses and protein crops for the production of grain (including seed and mixtures of cereals and...)", 
    "P1100" : "Field peas",
    "P1200" : "Broad and field beans",
    "P1300" : "Sweet lupins",
    "P9100" : "Lentils",
    "P9200" : "Chick peas",
    "R0000" : "Root crops",
    "R1000" : "Potatoes (including seed potatoes)",
    "R2000" : "Sugar beet (excluding seed)",
    "R9000" : "Other root crops n.e.c.",
    "I0000" : "Industrial crops",
    "I1100" : "Oilseeds",
    "I1110" : "Rape and turnip rape seeds",
    "I1120" : "Sunflower seed",
    "I1130" : "Soya",
    "I1140" : "Linseed (oilflax)",
    "I1150" : "Cotton seed",
    "I1190" : "Other oilseed crops n.e.c.",
    "I2000" : "Fibre crops",
    "I3000" : "Tobacco",
    "I4000" : "Hops",
    "I5000" : "Aromatic, medicinal and culinary plants",
    "I6000_9000" : "Other industrial crops including energy crops n.e.c.",
    "G0000": "Plants harvested green from arable land",
    "G1000" : "Temporary grasses and grazing",
    "G2000" : "Leguminous plants harvested greens",
    "G3000" : "Green maize",
    "V0000_S0000" : "Fresh vegetables (including melons) and strawberries",
    "V0000" : "Fresh vegetables (including melons)",
    "V1000" : "Brassicas",
    "V2000" : "Leafy and stalked vegetables (excluding brassicas)",
    "V3000" : "Vegetables cultivated for fruit (including melons)",
    "V3100" : "Tomatoes",
    "V4000" : "Root, tuber and bulb vegetables",
    "V4100" : "Carrots",
    "V4210" : "Onions",
    "V5000" : "Fresh pulses",
    "V9000" : "Other fresh vegetables n.e.c.",
    "S0000" : "Strawberries",
    "ARA9" : "Other arable land crops",
    "E0000" : "Seeds and seedlings",
    "Q0000" : "Fallow land",
    "J0000" : "Permanent grassland",
    "PECR" : "Permanent crops",
    "H0000" : "Permanent crops for human consumption",
    "F0000" : "Fruits, berries and nuts (excluding citrus fruits, grapes and strawberries)",
    "F1000" : "Fruits from temperate climate zones",
    "F1100" : "Pome fruits",
    "F1110" : "Apples",
    "F1120" : "Pears",
    "F1190" : "Other pome fruits n.e.c.",
    "F1200" : "Stone fruits",
    "F1210" : "Peaches",
    "F1220" : "Nectarines",
    "F1230" : "Apricots",
    "F1240" : "Cherries",
    "F1250" : "Plums",
    "F1290" : "Other stone fruits n.e.c.",
    "F2000": "Fruits from subtropical and tropical climate zones",
    "F3000" : "Berries (excluding strawberries)",
    "F4000" : "Nuts",
    "T0000" : "Citrus fruits",
    "T1000" : "Oranges",
    "W1000" : "Grapes",
    "W1100" : "Grapes for wines",
    "O1000" : "Olives",
    "H9000" : "Other permanent crops for human consumption n.e.c.",
    "PECR9" : "Other permanent crops",
    "U1000" : "Cultivated mushrooms"
}
or_farming['crops'] = or_farming["crops"].replace(dtld_nomenclature)

# Replace country codes with names
or_farming['geo'] = or_farming['geo'].replace({'IT': 'Italy', 'EL': 'Greece', 'ES': 'Spain', 'FR': 'France', 'DE': 'Germany'})

# Extract unique countries and years
countries = or_farming['geo'].unique()
years = or_farming['time_period'].unique()

# Bar charts for the evolution of total agricultural area with organic methods
for country in countries:
    country_data = or_farming[or_farming['geo'] == country]
    
    # Sum values for different crops to get the total organic agricultural area
    total_values = country_data.groupby('time_period')['obs_value'].sum().reset_index()
    
    plt.figure(figsize=(10, 5))
    
    # Plot the bar chart
    bars = plt.bar(total_values['time_period'], total_values['obs_value'], color = 'g', width = 0.8)
    
    # Add values at the top of the bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval, f'{yval:.2e}', ha='center', va='top', rotation=90, color = "white")
    
    plt.title(f'Total Organic Agricultural Area in {country}')
    plt.xlabel('Year')
    plt.ylabel('Total Organic Agricultural Area (ha)')
    
    # Adjust layout to avoid overlapping with title
    plt.tight_layout()
    
    plt.show()
    
    # Calculate the percentage change relative to the base 100 index (2012)
    base_year_value = total_values.loc[total_values['time_period'] == 2012, 'obs_value'].values[0]
    percentage_change = (total_values['obs_value'] / base_year_value - 1) * 100
    
    plt.figure(figsize=(10, 5))
    
    # Plot the dot chart
    plt.plot(total_values['time_period'], percentage_change, marker='o', linestyle='-', color='g')
    
    plt.title(f'Progression of Organic Farming in {country} (Relative to 2012)')
    plt.xlabel('Year')
    plt.ylabel('Percentage Change (Base 2012 = 100)')
    
    # Adjust layout to avoid overlapping with title
    plt.tight_layout()
    
    plt.show()

# Choose a specific date (replace with the desired date)
specific_date = 2018

# Filter data for the specific date
specific_date_data = or_farming[or_farming['time_period'] == specific_date]

# Extract unique countries
countries = specific_date_data['geo'].unique()

# Create a pie chart for each country
for country in countries:
    country_data = specific_date_data[specific_date_data['geo'] == country]

    # Exclude "Utilised agricultural area excluding kitchen gardens" and "Arable land"
    country_data = country_data[country_data['crops'] != "Utilised agricultural area excluding kitchen gardens"]
    country_data = country_data[country_data['crops'] != "Arable land"]

    # Extract crops and corresponding areas
    crops = country_data['crops'].unique()
    areas = country_data.groupby('crops')['obs_value'].sum()

    # Aggregate crops accounting for less than 1%
    threshold = 0.01
    areas_aggregated = areas.copy()
    small_crops = areas_aggregated[areas_aggregated / areas_aggregated.sum() < threshold]
    other_crops_area = small_crops.sum()
    areas_aggregated = areas_aggregated[~areas_aggregated.index.isin(small_crops.index)]
    areas_aggregated['Other crops'] = other_crops_area

    # Sort crops based on areas in descending order
    areas_aggregated = areas_aggregated.sort_values(ascending=False)

    # Create a pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(areas_aggregated, labels=areas_aggregated.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
    plt.title(f'Organic Farming Repartition by Crops in {country} ({specific_date})')
    plt.show()