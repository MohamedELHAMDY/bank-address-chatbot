import openpyxl
import pandas as pd
import os
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import time  # Import the time module

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

# Limit rows for testing (remove in production)
# df = df.head(10)  # Process only the first 10 rows for testing

def clean_address(address):
    if isinstance(address, str):
        return address.strip().replace(" ,", ",").replace("  ", " ")
    return address

# Set correct column names - THIS IS CRUCIAL
df.columns = ['Unnamed: 0', 'REGION', 'LOCALITE', 'NOM_BANQUE', 'CATEGORIE', 'CODE GUICHET', 'NOM GUICHET', 'ADRESSE GUICHET']

df['ADRESSE GUICHET'] = df['ADRESSE GUICHET'].apply(clean_address)  # Use the *intended* name

df_map = df[['REGION', 'LOCALITE', 'NOM_BANQUE', 'CATEGORIE', 'NOM GUICHET', 'ADRESSE GUICHET']].copy()  # Use the *intended* name

# --- Geocoding ---
def geocode_address(address, retries=3):
    geolocator = Nominatim(user_agent="mawqi_tamwil_app")
    for attempt in range(retries):
        try
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
df_map.info()
print("\nFirst 5 Rows of df_map:")
print(df_map.head())

print("\nColumns in df_map:")
print(df_map.columns)

print("Current working directory:", os.getcwd())
