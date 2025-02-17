import openpyxl
import pandas as pd
import os
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import time

excel_file = "data/detail-implantation-bancaire-2022.xlsx"
postal_codes_file = "data/codes-postaux-localites-2018.xlsx"

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

    # Select columns for geocoding
    df_map = df[['REGION', 'LOCALITE', 'NOM_BANQUE', 'CATEGORIE', 'NOM GUICHET', 'ADRESSE GUICHET']].copy()

    # Load postal codes data
    postal_codes_df = pd.read_excel(postal_codes_file)

    def geocode_address(row, retries=3):
        # Construct address with or without postal code
        postal_code_row = postal_codes_df[
            (postal_codes_df['REGION_POSTALE'] == row['REGION']) &
            (postal_codes_df['LOCALITE'] == row['LOCALITE'])
        ]

        if not postal_code_row.empty:
            postal_code = postal_code_row['NOUVEAU CODE POSTAL'].iloc[0]
            address = f"{row['ADRESSE GUICHET']}, {row['LOCALITE']}, {row['REGION']} {postal_code}"
            print(f"Constructed address with postal code: {address}")
        else:
            address = f"{row['ADRESSE GUICHET']}, {row['LOCALITE']}, {row['REGION']}"
            print(f"Constructed address without postal code: {address}")

        # Geocode the constructed address
        if not address or not isinstance(address, str) or address.strip() == "":
            print("Geocoding failed: No address provided")
            return None, None

        geolocator = Nominatim(user_agent="mawqi_tamwil_app")
        for attempt in range(retries):
            try:
                print(f"Geocoding address: {address}")
                location = geolocator.geocode(address)  # Use the constructed address
                if location:
                    print(f"Geocoding successful: {location.latitude}, {location.longitude}")
                    return location.latitude, location.longitude
                else:
                    print(f"Geocoding failed for address: {address}")
                    return None, None
            except (GeocoderTimedOut, GeocoderServiceError) as e:
                print(f"Geocoding error for address {address}: {e}")
                if attempt < retries - 1:
                    print("Retrying...")
                    time.sleep(1)
                    continue
                else:
                    print("Max retries reached for address:", address)
                    return None, None
            time.sleep(1)

    print("DataFrame before geocoding:")
    print(df)

    df_map['latitude'], df_map['longitude'] = zip(*df_map.apply(geocode_address, axis=1))

    data_dir = "data"
    bank_locations_geocoded_file = os.path.join(data_dir, "bank_locations_geocoded.csv")
    bank_locations_file = os.path.join(data_dir, "bank_locations.csv")

    os.makedirs(data_dir, exist_ok=True)

    df_map.to_csv(bank_locations_geocoded_file, index=False, encoding='utf-8')
    df_map.to_csv(bank_locations_file, index=False, encoding='utf-8')

    print(f"Geocoding complete. Data saved to {bank_locations_geocoded_file}")
    print(f"Data saved to {bank_locations_file}")

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

    print("Current working directory:", os.getcwd())

except Exception as e:
    print(f"An error occurred: {e}")
