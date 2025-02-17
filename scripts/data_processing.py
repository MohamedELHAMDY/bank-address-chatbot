import pandas as pd

excel_file = "data/detail-implantation-bancaire-2022.xlsx"
df = pd.read_excel(excel_file)

print(df.columns)  # Print ALL column names to the console (Important for debugging)

def clean_address(address):
    address = str(address).strip()
    address = address.replace(" ,", ",")
    address = address.replace("  ", " ")
    return address

# Use the EXACT column name from your Excel file
df['ADRESSE GUICHET'] = df['ADRESSE GUICHET'].apply(clean_address)  # Corrected column name

df_map = df[['REGION', 'LOCALITE', 'NOM_BANQUE', 'CATEGORIE', 'NOM_AGENCE', 'ADRESSE GUICHET']].copy()

df_map.to_csv("data/bank_locations.csv", index=False, encoding='utf-8')
print("Data saved to data/bank_locations.csv")
