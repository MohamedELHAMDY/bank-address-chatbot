import openpyxl
import pandas as pd
import os
import json

# Ensure script runs from correct location
script_dir = os.path.dirname(os.path.abspath(__file__))
excel_file = os.path.join(script_dir, "../data/detail-implantation-bancaire-2022.xlsx")
output_file = os.path.join(script_dir, "../data/addresses.json")

try:
    # Debugging: Check if file exists
    if not os.path.exists(excel_file):
        raise FileNotFoundError(f"Excel file not found at: {excel_file}")
    
    if os.path.getsize(excel_file) == 0:
        raise ValueError(f"Excel file {excel_file} is empty!")

    # Load Excel data
    workbook = openpyxl.load_workbook(excel_file, data_only=True)
    sheet = workbook.active

    # Read headers from the correct row (5th row is index 4)
    header_row = [cell.value for cell in sheet[5]]
    print("Header Row:", header_row)

    # Read data rows
    data_rows = []
    for row in sheet.iter_rows(min_row=6):
        row_data = {header_row[i]: cell.value for i, cell in enumerate(row) if header_row[i] is not None}
        data_rows.append(row_data)

    # Convert to DataFrame
    df = pd.DataFrame(data_rows)
    print("DataFrame Info:")
    df.info()

    # Clean addresses
    def clean_address(address):
        if isinstance(address, str):
            return address.strip().replace(" ,", ",").replace("  ", " ")
        return address

    if 'ADRESSE GUICHET' in df.columns:
        df['ADRESSE GUICHET'] = df['ADRESSE GUICHET'].apply(clean_address)

    # Create dictionary of addresses
    address_dict = {}
    for _, row in df.iterrows():
        identifier = f"{row.get('NOM_BANQUE', '')} - {row.get('NOM GUICHET', '')} - {row.get('LOCALITE', '')}"
        address = row.get('ADRESSE GUICHET')

        if identifier and address:
            address_dict[identifier] = address
        else:
            print(f"Warning: Missing identifier or address for row: {row.to_dict()}")

    # Save to JSON
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(address_dict, f, ensure_ascii=False, indent=4)

    print(f"Addresses saved to {output_file}")

except FileNotFoundError as e:
    print(f"Error: {e}")
    exit(1)  # Ensure GitHub Actions recognizes failure
except ValueError as e:
    print(f"Error loading Excel file: {e}")
    exit(1)
except Exception as e:
    print(f"An error occurred: {e}")
    exit(1)
