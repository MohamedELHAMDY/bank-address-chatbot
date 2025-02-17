import openpyxl
import pandas as pd
import os
import json

excel_file = "data/detail-implantation-bancaire-2022.xlsx"
output_file = "data/addresses.json"  # Define the output JSON file path

try:
    # Load Excel data
    if not os.path.exists(excel_file):
        raise FileNotFoundError(f"Excel file not found at: {excel_file}")

    workbook = openpyxl.load_workbook(excel_file)
    sheet = workbook.active

    # Get header row from row 5
    header_row = [cell.value for cell in sheet[5]]

    # Read data rows starting from row 6
    data_rows = []
    for row in sheet.iter_rows(min_row=6):
        row_data = {}
        for i, cell in enumerate(row):
            row_data[header_row[i]] = cell.value  # Map cell value to header
        data_rows.append(row_data)

    df = pd.DataFrame(data_rows)

    print("DataFrame created successfully:", df.shape)  # Print the shape of the DataFrame
    print("Columns in DataFrame:", df.columns)  # Print column names for debugging

    # Clean addresses (if needed)
    def clean_address(address):
        if isinstance(address, str):
            cleaned_address = address.strip().replace(" ,", ",").replace("  ", " ")
            return cleaned_address
        return address

    if 'ADRESSE GUICHET' in df.columns:  # Check if the column exists
        df['ADRESSE GUICHET'] = df['ADRESSE GUICHET'].apply(clean_address)
    else:
        print("Warning: 'ADRESSE GUICHET' column not found in DataFrame.")

    # Create the address dictionary
    address_dict = {}

    for index, row in df.iterrows():
        # Combine relevant fields to create a unique identifier.
        # Adjust the fields used here to create the identifier as needed for your data.
        identifier = f"{row.get('NOM_BANQUE', '')} - {row.get('NOM GUICHET', '')} - {row.get('LOCALITE', '')}"
        address = row.get('ADRESSE GUICHET')  # Use .get() to handle missing columns
        if identifier not in address_dict:  # Only add if identifier is unique
            address_dict[identifier] = address
        else:
            print(f"Duplicate identifier found: {identifier}")

    # Save the address dictionary to a JSON file
    with open(output_file, "w", encoding="utf-8") as f:  # Use the defined output file path
        json.dump(address_dict, f, ensure_ascii=False, indent=4)

    print(f"Addresses saved to {output_file}")  # Print the output file path

except FileNotFoundError as e:
    print(f"Error: {e}")
except ValueError as e:  # Catch potential errors during Excel loading
    print(f"Error loading Excel file: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
