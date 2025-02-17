import openpyxl
import pandas as pd
import os
import googlemaps
import time

excel_file = "data/detail-implantation-bancaire-2022.xlsx"

try:
    # ... (Load Excel data and clean addresses as before)

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
    api_key = os.environ.get("GOOGLE_MAPS_API_KEY")  # Correctly indented
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
                status = geocode_result[0].get('status')  # Check the status
                if status == 'OK':  # Check if the status is OK
                    location = geocode_result[0]['geometry']['location']
                    return location['lat'], location['lng']
                else:
                    print(f"Geocoding failed with status: {status} for address: {address}")
                    return None, None
            else:
                print(f"Geocoding failed for: {address}")
                return None, None
        except Exception as e:
            print(f"Error geocoding {address}: {e}")
            time.sleep(2)  # Increase the delay to 2 seconds (or more)
            return None, None

    df_map['latitude'], df_map['longitude'] = zip(*df_map['full_address'].apply(geocode_with_google))

    # ... (rest of your code)

except Exception as e:
    print(f"An error occurred: {e}")
