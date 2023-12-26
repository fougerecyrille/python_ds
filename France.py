""" Accès aux données et lecture """
chemin_acces = "/home/onyxia/work/ef_kvaareg__custom_9130147_spreadsheet.xlsx"
ttl_hold_nb = "Sheet 1"  # Nombre total d'exploitations par région française
df_hold = pd.read_excel(chemin_acces, sheet_name=ttl_hold_nb, engine='openpyxl')

#je comprends pas ça
# Replacing '(NUTS 2010)' with an empty string in 'Geographic indication'
df_hold['Geographic indication'] = df_hold['Geographic indication'].str.replace(' (NUTS 2010)', '')
print(df_hold)

# Drawing a pie chart according to these data
df_hold_modified = df_hold.iloc[1:]
print(df_hold_modified)
labels = df_hold_modified['Geographic indication']
sizes = df_hold_modified['Number of holdings']
plt.pie(sizes, labels=labels, autopct='%1.1f%%')
plt.title('Répartition géographique des exploitations')
plt.show()

