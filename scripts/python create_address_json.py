import openpyxl
import pandas as pd
import os
import json

excel_file = "data/detail-implantation-bancaire-2022.xlsx"

try:
    # Load Excel data
    workbook = openpyxl.load_workbook(excel_file)
    sheet = workbook.active
    data_rows = []
    for row in sheet.iter_rows(min_row=6):
        data_rows.append([cell.value for cell in row])
    header_row = [cell.value for cell in sheet[5]]
    df = pd.DataFrame(data_rows, columns=header_row)

    # Clean addresses (if needed)
    def clean_address(address):
        if isinstance(address, str):
            cleaned_address = address.strip().replace(" ,", ",").replace("  ", " ")
            return cleaned_address
        return address

    df['ADRESSE GUICHET'] = df['ADRESSE GUICHET'].apply(clean_address)

    # Create the address dictionary
    address_dict = {}

    for index, row in df.iterrows():
        # Combine relevant fields to create a unique identifier.
        # Adjust the fields used here to create the identifier as needed for your data.
        identifier = f"{row['NOM_BANQUE']} - {row['NOM GUICHET']} - {row['LOCALITE']}"
        address = row['ADRESSE GUICHET']
        if identifier not in address_dict:  # Only add if identifier is unique
          address_dict[identifier] = address
        else:
          print(f"Duplicate identifier found: {identifier}")

    # Save the address dictionary to a JSON file
    with open("addresses.json", "w", encoding="utf-8") as f:
        json.dump(address_dict, f, ensure_ascii=False, indent=4)

    print("Addresses saved to addresses.json")

except Exception as e:
    print(f"An error occurred: {e}")
