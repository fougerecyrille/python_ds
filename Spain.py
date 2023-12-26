import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pynsee.download

"""1. Drawing a pie chart illustrating the geographic repartition of the agricultural holdings in Spain,
by number of holdings and European NUTS2 regions"""

excel_file_path = "/Users/cyrillefougere/Desktop/ENSAE 2023:2024/S1/Python et Data Science/Databases/Key farm indicators_Spain_NUTS2.xlsx"
ttl_hold_nb = "Sheet 1"  
df_hold = pd.read_excel(excel_file_path, sheet_name=ttl_hold_nb, engine='openpyxl')

#Eliminating the rows corresponding to the Spanish cities of Ceuta and Melilla, situated in Northen Morocco
df_hold=df_hold[df_hold['Number of holdings'] !=0]

# Drawing a pie chart according to these data
labels = df_hold['Geographic indication']
sizes = df_hold['Number of holdings']
plt.pie(sizes, labels=labels, autopct='%1.1f%%')
plt.title('Geographic Repartition of the Agricultural Holdings in Spain')
plt.show()

"""2. Drawing a bar chart illustrating the total used agricultural area in Spain, by ha. and European NUTS2 regions"""

excel_file_path = "/Users/cyrillefougere/Desktop/ENSAE 2023:2024/S1/Python et Data Science/Databases/Key farm indicators_Spain_NUTS2.xlsx"
ttl_area_ha = "Sheet 4"  
df_area = pd.read_excel(excel_file_path, sheet_name=ttl_area_ha, engine='openpyxl')

#Eliminating the rows corresponding to the Spanish cities of Ceuta and Melilla, situated in Northen Morocco
df_area = df_area[df_area['Used agricultural area (ha)'] !=0]

# Drawing a bar chart according to these data
plt.bar(df_area['Geographic indication'],df_area['Used agricultural area (ha)'])
plt.xlabel('Geographic indication')
plt.ylabel('Used agricultural area (ha)')
plt.title('Used Agricultural Area in Greece by NUTS2 Regions')
#Trying the scientific notation to make it easier to read the bar chart
for i, value in enumerate(df_area['Used agricultural area (ha)']):
    plt.text(i, value + 10000, '{:.2e}'.format(value), ha='center', va='bottom', rotation=90)
plt.xticks(rotation=45, ha='right')
plt.show()

"""3. Drawing a bar chart illustrating the standard economic output, 
in euros, of agriculture, of every Spanish region"""

excel_file_path = "/Users/cyrillefougere/Desktop/ENSAE 2023:2024/S1/Python et Data Science/Databases/Key farm indicators_Spain_NUTS2.xlsx"
econ_output = "Sheet 7"  
df_output = pd.read_excel(excel_file_path, sheet_name=econ_output, engine='openpyxl')

#Eliminating the rows corresponding to the Spanish cities of Ceuta and Melilla, situated in Northen Morocco
df_output = df_output[df_output['Standard output (euros)'] !=0]

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