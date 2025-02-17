import openpyxl
import pandas as pd

excel_file = "data/detail-implantation-bancaire-2022.xlsx"

# Load the workbook using openpyxl
workbook = openpyxl.load_workbook(excel_file)
sheet = workbook.active  # Get the active sheet

# Get the header row values (handling merged cells and None values)
header_row = []
merged_ranges = list(sheet.merged_cells.ranges)  # Convert to a list for easier searching

for cell in sheet[1]:  # Assuming header is in the first row (row 1)
    cell_value = cell.value
    if cell_value:  # If the cell has a value
        header_row.append(cell_value)
    else:  # If the cell is merged or has no value
        found = False
        for merged_range in merged_ranges:
            if cell.coordinate in merged_range:
                header_cell = sheet[merged_range.min]  # Use .min for older versions
                header_row.append(header_cell.value)
                found = True
                break
        if not found: # if it is a None value and not in a merged cell range
            header_row.append(None) # Add a None value to the header

# Remove potential None values from the header row
header_row = [h for h in header_row if h is not None]

# Create a list to store the data rows
data_rows = []
for row in sheet.iter_rows(min_row=2):  # Start from the second row (data rows)
    data_row = []
    for cell in row:
      data_row.append(cell.value)
    data_rows.append(data_row)



# Create the DataFrame using the extracted header and data
df = pd.DataFrame(data_rows, columns=header_row)

def clean_address(address):
    if isinstance(address, str): # Check if it's a string
        address = address.strip()
        address = address.replace(" ,", ",")
        address = address.replace("  ", " ")
        return address
    return address # Return if it's not a string (e.g., None)

df['ADRESSE GUICHET'] = df['ADRESSE GUICHET'].apply(clean_address)

df_map = df[['REGION', 'LOCALITE', 'NOM_BANQUE', 'CATEGORIE', 'NOM GUICHET', 'ADRESSE GUICHET']].copy()

df_map.to_csv("data/bank_locations.csv", index=False, encoding='utf-8')
print("Data saved to data/bank_locations.csv")
