import pandas as pd
import json

# Load Excel file
file_path = "data/detail-implantation-bancaire-2022.xlsx"
output_json = "data/bank_addresses.json"

try:
    df = pd.read_excel(file_path, dtype=str)  # Read as string to avoid type issues

    # Keep only required columns
    required_columns = ["REGION", "LOCALITE", "BANQUE", "CATEGORIE", "CODE GUICHET", "NOM GUICHET", "ADRESSE GUICHET"]
    df = df[required_columns]

    # Convert DataFrame to dictionary
    bank_data = df.to_dict(orient="records")

    # Save as JSON
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(bank_data, f, ensure_ascii=False, indent=4)

    print(f"✅ Data successfully saved to {output_json}")

except Exception as e:
    print(f"❌ Error loading data: {e}")
