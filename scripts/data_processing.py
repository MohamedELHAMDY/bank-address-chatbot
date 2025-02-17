import openpyxl
import pandas as pd
import os
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import time

excel_file = "data/detail-implantation-bancaire-2022.xlsx"

# Load the workbook using openpyxl
workbook = openpyxl.load_workbook(excel_file)
sheet = workbook.active

# Extract data rows (starting from row 6)
data_rows = []
for row in sheet.iter_rows(min_row=6):
    data_rows.append([cell.value for cell in row])

# Extract header row (from row 5)
header_row = [cell.value for cell in sheet[5]]

# Create DataFrame
df = pd.DataFrame(data_rows, columns=header_row)

# Clean addresses (before setting column names to avoid potential KeyError)
def clean_address(address):
    if isinstance(address, str):
        cleaned_address = address.strip().replace(" ,", ",").replace("  ", " ")
        return cleaned_address
    return address  # Return original value if not a string

df['ADRESSE GUICHET'] = df['ADRESSE GUICHET'].apply(clean_address)


# Set correct column names - THIS IS CRUCIAL
df.columns = ['Unnamed: 0', 'REGION', 'LOCALITE', 'NOM_BANQUE', 'CATEGORIE', 'CODE GUICHET', 'NOM GUICHET', 'ADRESSE GUICHET']

df_map = df[['REGION', 'LOCALITE', 'NOM_BANQUE', 'CATEGORIE', 'NOM GUICHET', 'ADRESSE GUICHET']].copy()

# --- Geocoding ---
def geocode_address(address, retries=3):
    if address is None or not isinstance(address, str) or address.strip() == "":  # Check for None, non-string, or empty address
        print("Geocoding failed: No address provided")  # Print failure message
        return None, None

    geolocator = Nominatim(user_agent="mawqi_tamwil_app")
    for attempt in range(retries):
        try:
            print(f"Geocoding address: {address}")  # Print the address being geocoded
            location = geolocator.geocode(address)
            if location:
                print(f"Geocoding successful: {location.latitude}, {location.longitude}")  # Print successful result
                return location.latitude, location.longitude
            else:
                print("Geocoding failed: No location found")  # Print failure message
                return None, None
        except (GeocoderTimedOut, GeocoderServiceError) as e:
            print(f"Geocoding failed for {address}: {e}")  # Print specific error
            if attempt < retries - 1:
                print("Retrying...")
                time.sleep(1) # Wait for 1 second before retrying
                continue
            else:
                print("Max retries reached. Giving up.")
                return None, None
        time.sleep(1) # Wait for 1 second after each attempt

print("DataFrame before geocoding:")
print(df) # Print the dataframe before geocoding

df_map['latitude'], df_map['longitude'] = zip(*df_map['ADRESSE GUICHET'].apply(geocode_address))

# --- Save to CSV ---
data_dir = "data"  # Define the data directory
bank_locations_geocoded_file = os.path.join(data_dir, "bank_locations_geocoded.csv")
bank_locations_file = os.path.join(data_dir, "bank_locations.csv")

# Create the data directory if it doesn't exist
os.makedirs(data_dir, exist_ok=True)


df_map.to_csv(bank_locations_geocoded_file, index=False, encoding='utf-8')  # Save geocoded data
df_map.to_csv(bank_locations_file, index=False, encoding='utf-8')  # Save geocoded data

print(f"Geocoding complete. Data saved to {bank_locations_geocoded_file}")
print(f"Data saved to {bank_locations_file}")

# Print statements for debugging (remove in production)
print("DataFrame Info:")
df.info()
print("\nFirst 5 Rows of DataFrame:")
print(df.head())

print("\ndf_map Info:")
print(df_map.info()
print("\nFirst 5 Rows of df_map:")
print(df_map.head())

print("\nColumns in df_map:")
print(df_map.columns)

print("Current working directory:", os.getcwd())
