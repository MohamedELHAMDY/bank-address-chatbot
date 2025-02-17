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

# Corrected column indices to match the Excel file structure
region_index = 1  # Column B (REGION) - Corrected
localite_index = 2  # Column C (LOCALITE) - Corrected
nom_banque_index = 3  # Column D (BANQUE) - Corrected
categorie_index = 4  # Column E (CATEGORIE) - Corrected
nom_guichet_index = 6  # Column G (NOM GUICHET) - Corrected
adresse_guichet_index = 7  # Column H (ADRESSE GUICHET) - Corrected

# Create DataFrame using indices
df = pd.DataFrame(data_rows[1:], columns=data_rows[0])  # Skip first row (header)

def clean_address(address):
    if isinstance(address, str):
        return address.strip().replace(" ,", ",").replace("  ", " ")
    return address

df['ADRESSE GUICHET'] = df.iloc[:, adresse_guichet_index - 1].apply(clean_address)  # Use corrected index and subtract 1

# Create df_map using indices - THIS IS THE KEY CORRECTION
df_map = df.iloc[:, [region_index - 1, localite_index - 1, nom_banque_index - 1, categorie_index - 1, nom_guichet_index - 1, adresse_guichet_index - 1]].copy()

df_map.columns = ['REGION', 'LOCALITE', 'NOM_BANQUE', 'CATEGORIE', 'NOM GUICHET', 'ADRESSE GUICHET']  # Set correct column names

df_map.to_csv("data/bank_locations.csv", index=False, encoding='utf-8')
print("Data saved to data/bank_locations.csv")
