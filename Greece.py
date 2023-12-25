import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pynsee.download

import pandas as pd

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

# Créez un camembert en utilisant matplotlib
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)

# Ajoutez un titre
plt.title('Répartition géographique des exploitations')

# Affichez le camembert
plt.show()