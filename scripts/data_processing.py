import pandas as pd

excel_file = "data/detail-implantation-bancaire-2022.xlsx"
df = pd.read_excel(excel_file)

def clean_address(address):
    address = str(address).strip()
    address = address.replace(" ,", ",")
    address = address.replace("  ", " ")
    return address
#My comment
df['ADRESSE'] = df['ADRESSE'].apply(clean_address)

df_map = df[['REGION', 'LOCALITE', 'NOM_BANQUE', 'CATEGORIE', 'NOM_AGENCE', 'ADRESSE']].copy()

df_map.to_csv("data/bank_locations.csv", index=False, encoding='utf-8')
print("Data saved to data/bank_locations.csv") 
