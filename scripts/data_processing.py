import openpyxl
import pandas as pd
import os
import googlemaps
import time

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

    # Clean addresses
    def clean_address(address):
        if isinstance(address, str):
            cleaned_address = address.strip().replace(" ,", ",").replace("  ", " ")
            return cleaned_address
        return address

    df['ADRESSE GUICHET'] = df['ADRESSE GUICHET'].apply(clean_address)

    # Select columns
    df_map = df[['REGION', 'LOCALITE', 'NOM_BANQUE', 'CATEGORIE', 'CODE GUICHET', 'NOM GUICHET', 'ADRESSE GUICHET']].copy()

    def construct_full_address(row):
        address_parts = [
            row['ADRESSE GUICHET'],
            row['NOM GUICHET'],
            row['CODE GUICHET'],
            row['CATEGORIE'],
            row['NOM_BANQUE'],
            row['LOCALITE'],
            row['REGION']
        ]
        cleaned_parts = [part for part in address_parts if part is not None and str(part).strip() != ""]
        full_address = ", ".join(cleaned_parts)
        print(f"Full Address: {full_address}")  # Print the full address HERE
        return full_address

    df_map['full_address'] = df_map.apply(construct_full_address, axis=1)

    # Print header for debugging
    print(df.columns)

    # Initialize Google Maps client (using environment variable for API key)
    api_key = os.environ.get("GOOGLE_MAPS_API_KEY")
    if api_key is None:
        raise ValueError("GOOGLE_MAPS_API_KEY environment variable not set.")
    print(f"API Key (first 5 chars): {api_key[:5] if api_key else None}")  # Print the first 5 characters

    gmaps = googlemaps.Client(key=api_key)

    def geocode_with_google(address):
        if not address:  # Check if address is empty or None
            print("Address is empty or None")
            return None, None
        try:
            geocode_result = gmaps.geocode(address)
            print(f"Geocode Result: {geocode_result}")  # Print the raw result
            if geocode_result:
                location = geocode_result[0]['geometry']['location']
                return location['lat'], location['lng']
            else:
                print(f"Geocoding failed for: {address}")
                return None, None
        except Exception as e:
            print(f"Error geocoding {address}: {e}")
            time.sleep(2)  # Increase the delay to 2 seconds (or more)
            return None, None

    df_map['latitude'], df_map['longitude'] = zip(*df_map['full_address'].apply(geocode_with_google))

    # Select and reorder columns for the final output
    df_map = df_map[['ADRESSE GUICHET', 'LOCALITE', 'REGION', 'latitude', 'longitude']]

    data_dir = "data"
    bank_locations_geocoded_file = os.path.join(data_dir, "bank_locations_geocoded.csv")
    bank_locations_file = os.path.join(data_dir, "bank_locations.csv")

    os.makedirs(data_dir, exist_ok=True)

    df_map.to_csv(bank_locations_geocoded_file, index=False, encoding='utf-8')
    df_map.to_csv(bank_locations_file, index=False, encoding='utf-8')

    print(f"Geocoding complete. Data saved to {bank_locations_geocoded_file}")
    print(f"Data saved to {bank_locations_file}")

    print("DataFrame Info:")
    df_map.info()
    print("\nFirst 5 Rows of DataFrame:")
    print(df_map.head())

    print("\nColumns in df_map:")
    print(df_map.columns)

    print("Current working directory:", os.getcwd())

    # Check if files were created (for debugging)
    print(f"File exists (bank_locations_geocoded.csv): {os.path.exists(bank_locations_geocoded_file)}")
    print(f"File exists (bank_locations.csv): {os.path.exists(bank_locations_file)}")


except Exception as e:
    print(f"An error occurred: {e}")
