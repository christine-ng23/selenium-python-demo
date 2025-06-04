# -----------------------------
# TEST DATA MANAGEMENT (JSON-driven)
# -----------------------------

# core/user_data_loader.py
import json
import os

def load_user_data():
    path = os.path.join(os.path.dirname(__file__), 'users.json')
    with open(path, 'r') as f:
        return json.load(f)

