Bank Address Chatbot
Bank Address Chatbot is a tool designed to help users quickly find bank branch addresses through a chatbot interface. The project processes raw banking data and serves it via a Flask API with a user-friendly web interface.

Features
Data Processing: Converts Excel datasets into a structured JSON format.
Flask API: Serves bank address data for querying.
Chatbot Interface: Provides an interactive, web-based interface.
Fuzzy Matching: Uses fuzzy string matching (via fuzzywuzzy) to improve search results. (For better performance, consider installing python-Levenshtein.)
Project Structure
cpp
Copier
Modifier
bank-address-chatbot-main/
├── .github/workflows/
│   ├── data_processing.yml
│   └── export-requirements.yml
├── data/
│   ├── addresses.json
│   ├── codes-postaux-localites-2018.xlsx
│   └── detail-implantation-bancaire-2022.xlsx
├── scripts/
│   ├── create_address_json.py
│   ├── load_data.py
│   └── style.css
├── static/
│   ├── index.html
│   └── script.js
├── LICENSE
├── README.md
├── pyproject.toml
└── requirements.txt
Installation
Clone the Repository:

bash
Copier
Modifier
git clone https://github.com/MohamedELHAMDY/bank-address-chatbot.git
cd bank-address-chatbot
Install Dependencies:

Ensure you are using Python 3.11 or later. Then run:

bash
Copier
Modifier
pip install -r requirements.txt
Your requirements.txt should include:

nginx
Copier
Modifier
pandas
flask
fuzzywuzzy
python-Levenshtein
gunicorn
Prepare the Data:

Run the data processing script to generate/update the JSON file:

bash
Copier
Modifier
python scripts/create_address_json.py
Usage
Run the Flask App:

Start the development server by running:

bash
Copier
Modifier
python scripts/load_data.py
The Flask app will run on http://127.0.0.1:5000.

Access the Chatbot Interface:

Open the static/index.html file in your browser, or navigate to the deployed URL if hosted on a server.

Production Deployment:

For production, use a WSGI server like gunicorn:

bash
Copier
Modifier
gunicorn -w 4 -b 0.0.0.0:5000 load_data:app
Deployment on Render
This project is ready for deployment on Render:

Python Version: 3.11.11 (or as specified in your environment)
Build Command:
bash
Copier
Modifier
pip install -r requirements.txt && python scripts/load_data.py
Deployment Time: Typically 2–5 minutes for free-tier deployments. Caching and using a paid plan can reduce this time.
Contributing
Contributions are welcome! Please fork this repository and submit a pull request with your enhancements or bug fixes.

License
This project is licensed under the MIT License.

Contact
If you have any questions or need support, please open an issue in the repository or contact the project maintainer.

