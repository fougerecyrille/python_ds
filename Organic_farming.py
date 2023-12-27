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