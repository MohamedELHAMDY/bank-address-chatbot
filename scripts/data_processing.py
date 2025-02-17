import pandas as pd

excel_file = "data/detail-implantation-bancaire-2022.xlsx"
df = pd.read_excel(excel_file)

print(df.columns)  # Print ALL column names to the console (Essential for debugging)

def clean_address(address):
    address = str(address).strip()
    address = address.replace(" ,", ",")
    address = address.replace("  ", " ")
    return address

# Find the "ADRESSE" column regardless of extra characters or encoding
address_column = None
for col in df.columns:
    if "ADRESSE" in col.upper():  # Check for "ADRESSE" (case-insensitive)
        address_column = col
        break

if address_column:
    print(f"Using column: {address_column}")  # Print the actual column name being used
    df[address_column] = df[address_column].apply(clean_address)
    df_map = df[['REGION', 'LOCALITE', 'NOM_BANQUE', 'CATEGORIE', 'NOM_AGENCE', address_column]].copy()
    df_map.rename(columns={address_column: 'ADRESSE GUICHET'}, inplace=True) # Rename for consistency

    df_map.to_csv("data/bank_locations.csv", index=False, encoding='utf-8')
    print("Data saved to data/bank_locations.csv")
else:
    raise KeyError("No column containing 'ADRESSE' found. Check your Excel file.")
