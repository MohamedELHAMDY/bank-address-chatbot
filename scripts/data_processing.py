import openpyxl
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

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
        try:
            location = geolocator.geocode(address)
            if location:
                return location.latitude, location.longitude
            else:
                return None, None
        except (GeocoderTimedOut, GeocoderServiceError) as e:
            print(f"Geocoding failed for {address}: {e}")
            if attempt < retries - 1:
                print("Retrying...")
                continue
            else:
                print("Max retries reached. Giving up.")
                return None, None

df_map['latitude'], df_map['longitude'] = zip(*df_map['ADRESSE GUICHET'].apply(geocode_address))

# --- Save to CSV ---
df_map.to_csv("data/bank_locations_geocoded.csv", index=False, encoding='utf-8')  # Save geocoded data
print("Geocoding complete. Data saved to data/bank_locations_geocoded.csv")

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
