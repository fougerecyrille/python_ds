import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load your CSV data into a DataFrame
or_farming = pd.read_csv('/Users/cyrillefougere/Desktop/ENSAE 2023:2024/S1/Python et Data Science/Databases/Organic farming_G5_ha.csv')

# Convert column names to lower case for case-insensitivity 
or_farming.columns = or_farming.columns.str.lower()

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
    bars = plt.bar(total_values['time_period'], total_values['obs_value'])
    
    # Add values at the top of the bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval, f'{yval:.2e}', ha='center', va='bottom', rotation=90)
    
    plt.title(f'Total Organic Agricultural Area in {country}')
    plt.xlabel('Year')
    plt.ylabel('Total Organic Agricultural Area (ha)')
    plt.show()
    
    # Calculate the percentage change relative to the base 100 index (2012)
    base_year_value = total_values.loc[total_values['time_period'] == 2012, 'obs_value'].values[0]
    percentage_change = (total_values['obs_value'] / base_year_value - 1) * 100
    
    plt.figure(figsize=(10, 5))
    
    # Plot the dot chart
    plt.plot(total_values['time_period'], percentage_change, marker='o', linestyle='-', color='b')
    
    plt.title(f'Progression of Organic Farming in {country} (Relative to 2012)')
    plt.xlabel('Year')
    plt.ylabel('Percentage Change (Base 2012 = 100)')
    plt.show()

# Choose a specific date (replace with the desired date)
specific_date = 2020

# Filter data for the specific date
specific_date_data = or_farming[or_farming['time_period'] == specific_date]

# Extract unique countries
countries = specific_date_data['geo'].unique()

# Create a pie chart for each country
for country in countries:
    country_data = specific_date_data[specific_date_data['geo'] == country]

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

    # Create a pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(areas_aggregated, labels=areas_aggregated.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
    plt.title(f'Organic Farming Repartition by Crops in {country} ({specific_date})')
    plt.show()