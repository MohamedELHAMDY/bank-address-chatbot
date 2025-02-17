from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# Load bank data
DATA_FILE = os.path.join(os.path.dirname(__file__), "../data/addresses.json")

with open(DATA_FILE, "r", encoding="utf-8") as f:
    bank_data = json.load(f)

@app.route("/get_address", methods=["GET"])
def get_address():
    """Fetches bank addresses based on query"""
    bank_name = request.args.get("bank", "").strip().lower()
    location = request.args.get("location", "").strip().lower()

    results = [
        bank for bank in bank_data
        if bank_name in bank["BANQUE"].lower() and location in bank["LOCALITE"].lower()
    ]

    return jsonify(results if results else {"message": "No results found"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
