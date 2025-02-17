import openpyxl
import pandas as pd

excel_file = "data/detail-implantation-bancaire-2022.xlsx"

# Load the workbook using openpyxl
workbook = openpyxl.load_workbook(excel_file)
sheet = workbook.active

# Extract data rows (starting from row 6)
data_rows = []
for row in sheet.iter_rows(min_row=6):  # Start from row 6
    data_rows.append([cell.value for cell in row])

# Extract header row (from row 5)
header_row = [cell.value for cell in sheet[5]]

# Create DataFrame
df = pd.DataFrame(data_rows, columns=header_row)

def clean_address(address):
    if isinstance(address, str):
        return address.strip().replace(" ,", ",").replace("  ", " ")
    return address

# Set correct column names - THIS IS CRUCIAL
df.columns = ['REGION', 'LOCALITE', 'NOM_BANQUE', 'CATEGORIE', 'CODE GUICHET', 'NOM GUICHET', 'ADRESSE GUICHET']

df['ADRESSE GUICHET'] = df['ADRESSE GUICHET'].apply(clean_address)  # Use the *intended* name

df_map = df[['REGION', 'LOCALITE', 'NOM_BANQUE', 'CATEGORIE', 'NOM GUICHET', 'ADRESSE GUICHET']].copy()  # Use the *intended* name

# Print statements for debugging (remove in production)
print("DataFrame Info:")
df.info()
print("\nFirst 5 Rows of DataFrame:")
print(df.head())

print("\ndf_map Info:")
df_map.info()
print("\nFirst 5 Rows of df_map:")
print(df_map.head())

print("\nColumns in df_map:")
print(df_map.columns)

df_map.to_csv("data/bank_locations.csv", index=False, encoding='utf-8')
print("Data saved to data/bank_locations.csv")
