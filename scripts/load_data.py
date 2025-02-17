from flask import Flask, request, jsonify
import json
import os
from fuzzywuzzy import process

app = Flask(__name__)

# Load Data
DATA_FILE = os.path.join(os.path.dirname(__file__), "../data/addresses.json")
with open(DATA_FILE, "r", encoding="utf-8") as f:
    bank_data = json.load(f)

def fuzzy_search(query, choices, key):
    """Find best matches using fuzzy search"""
    matches = process.extract(query, [bank[key] for bank in choices], limit=5)
    return [bank for bank in choices if bank[key] in [m[0] for m in matches if m[1] > 70]]

@app.route("/get_address", methods=["GET"])
def get_address():
    bank_name = request.args.get("bank", "").strip().lower()
    location = request.args.get("location", "").strip().lower()

    if not bank_name or not location:
        return jsonify({"error": "Please provide both bank and location"})

    results = fuzzy_search(bank_name, bank_data, "BANQUE")
    results = fuzzy_search(location, results, "LOCALITE")

    return jsonify(results if results else {"message": "No results found"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
