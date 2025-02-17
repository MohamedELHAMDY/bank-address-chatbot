import openpyxl
import pandas as pd

excel_file = "data/detail-implantation-bancaire-2022.xlsx"

# Load the workbook using openpyxl
workbook = openpyxl.load_workbook(excel_file)
sheet = workbook.active

# Get header row (handling merged cells robustly)
header_row = [cell.value for cell in sheet[1]] # Simplified header extraction

# Create data rows
data_rows = []
for row in sheet.iter_rows(min_row=2):
    data_rows.append([cell.value for cell in row]) # Simplified data extraction

# Create DataFrame
df = pd.DataFrame(data_rows, columns=header_row)

def clean_address(address):
    if isinstance(address, str):
        return address.strip().replace(" ,", ",").replace("  ", " ")
    return address

df['ADRESSE GUICHET'] = df['ADRESSE GUICHET'].apply(clean_address)

df_map = df[['REGION', 'LOCALITE', 'NOM_BANQUE', 'CATEGORIE', 'NOM GUICHET', 'ADRESSE GUICHET']].copy()

df_map.to_csv("data/bank_locations.csv", index=False, encoding='utf-8')
print("Data saved to data/bank_locations.csv")
