import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pynsee.download

import pandas as pd

excel_file_path = "/Users/cyrillefougere/Desktop/ENSAE 2023:2024/S1/Python et Data Science/Databases/Key farm indicators_Greece_NUTS2.xlsx"
ttl_hold_nb = "Sheet 1"  
df_hold = pd.read_excel(excel_file_path, sheet_name=ttl_hold_nb, engine='openpyxl')

print(df_hold)

#Essais git sur VSCode