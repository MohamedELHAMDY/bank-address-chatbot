import openpyxl
import pandas as pd

excel_file = "data/detail-implantation-bancaire-2022.xlsx"

# Load the workbook using openpyxl
workbook = openpyxl.load_workbook(excel_file)
sheet = workbook.active

# Extract data rows (including the header row)
data_rows = []
for row in sheet.iter_rows():  # Iterate through ALL rows
    data_rows.append([cell.value for cell in row])

# Identify column indices (adjust these if your columns are in different positions)
region_index = 0  # Column A
localite_index = 1 # Column B
nom_banque_index = 2 # Column C
categorie_index = 3 # Column D
nom_guichet_index = 5 # Column F
adresse_guichet_index = 6 # Column G

# Create DataFrame using indices
df = pd.DataFrame(data_rows[1:], columns=data_rows[0]) # Skip first row (header)

def clean_address(address):
    if isinstance(address, str):
        return address.strip().replace(" ,", ",").replace("  ", " ")
    return address

df['ADRESSE GUICHET'] = df.iloc[:, adresse_guichet_index].apply(clean_address)  # Use index

df_map = df[[df.columns[region_index], df.columns[localite_index], df.columns[nom_banque_index], df.columns[categorie_index], df.columns[nom_guichet_index], 'ADRESSE GUICHET']].copy()

df_map.to_csv("data/bank_locations.csv", index=False, encoding='utf-8')
print("Data saved to data/bank_locations.csv")
