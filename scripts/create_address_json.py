import pandas as pd
import json
import os

# File paths
excel_file = "data/detail-implantation-bancaire-2022.xlsx"
json_file = "data/addresses.json"

# Ensure data directory exists
os.makedirs("data", exist_ok=True)
#
def process_data():
    """Load bank details from Excel and save as JSON."""
    try:
        df = pd.read_excel(excel_file, dtype=str)
        required_columns = ["REGION", "LOCALITE", "BANQUE", "CATEGORIE", "CODE GUICHET", "NOM GUICHET", "ADRESSE GUICHET"]
        
        if not all(col in df.columns for col in required_columns):
            raise ValueError("Missing required columns in the Excel file.")

        bank_data = df[required_columns].to_dict(orient="records")

        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(bank_data, f, ensure_ascii=False, indent=4)

        print(f"✅ Data successfully saved to {json_file}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    process_data()
