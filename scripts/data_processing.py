import openpyxl
import pandas as pd
import os
import googlemaps
import time

# ... (rest of your code)

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

# ... (rest of your code)
