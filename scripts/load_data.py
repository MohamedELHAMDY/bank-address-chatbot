import json

# File path
json_file = "data/addresses.json"

def load_data():
    """Load processed bank address data."""
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ Data file not found. Run 'create_address_json.py' first.")
        return []

bank_data = load_data()

def search_bank(bank_name, locality):
    """Find a bank's address by name and locality."""
    for bank in bank_data:
        if bank["BANQUE"].lower() == bank_name.lower() and bank["LOCALITE"].lower() == locality.lower():
            return f"🏦 {bank['BANQUE']} - {bank['NOM GUICHET']} 📍 {bank['ADRESSE GUICHET']}"
    
    return "❌ No matching bank found. Try a different name or locality."

# CLI chatbot loop
print("💬 Welcome to Bank Address Chatbot! Type 'exit' to quit.")
while True:
    bank_name = input("Enter the bank name: ").strip()
    if bank_name.lower() == "exit":
        break
    locality = input("Enter the locality: ").strip()
    
    result = search_bank(bank_name, locality)
    print(result)
