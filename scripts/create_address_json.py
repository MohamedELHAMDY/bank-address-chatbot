import openpyxl
import pandas as pd
import os
import json

excel_file = "data/detail-implantation-bancaire-2022.xlsx"  # Path relative to repository root
output_file = "data/addresses.json"  # Path relative to repository root

try:
    # Load Excel data
    if not os.path.exists(excel_file):
        raise FileNotFoundError(f"Excel file not found at: {excel_file}")

    workbook = openpyxl.load_workbook(excel_file)
    sheet = workbook.active

    header_row = [cell.value for cell in sheet[5]]  # Header row from row 5
    print("Header Row:", header_row)  # Print the header row

    data_rows = []
    for row in sheet.iter_rows(min_row=6):
        row_data = {}
        for i, cell in enumerate(row):
            row_data[header_row[i]] = cell.value
        data_rows.append(row_data)

    print("Data Rows:\n", data_rows)  # Print the data rows

    df = pd.DataFrame(data_rows)

    print("DataFrame Info:")
    df.info()  # Print DataFrame information

    print("DataFrame Head:\n", df.head())  # Print the first few rows of the DataFrame


    # Clean addresses (if needed)
    def clean_address(address):
        if isinstance(address, str):
            cleaned_address = address.strip().replace(" ,", ",").replace("  ", " ")
            return cleaned_address
        return address

    if 'ADRESSE GUICHET' in df.columns:
        df['ADRESSE GUICHET'] = df['ADRESSE GUICHET'].apply(clean_address)
    else:
        print("Warning: 'ADRESSE GUICHET' column not found in DataFrame.")

    # Create the address dictionary
    address_dict = {}

    for index, row in df.iterrows():
        identifier = f"{row.get('NOM_BANQUE', '')} - {row.get('NOM GUICHET', '')} - {row.get('LOCALITE', '')}"
        address = row.get('ADRESSE GUICHET')
        if identifier and address:  # Check for both identifier and address
            if identifier not in address_dict:
                address_dict[identifier] = address
            else:
                print(f"Duplicate identifier found: {identifier}")
        else:
            print(f"Warning: Missing identifier or address for row: {row}")

    # Save the address dictionary to a JSON file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(address_dict, f, ensure_ascii=False, indent=4)

    print(f"Addresses saved to {output_file}")

except FileNotFoundError as e:
    print(f"Error: {e}")
except ValueError as e:
    print(f"Error loading Excel file: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
