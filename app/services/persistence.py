import json
import os
from typing import List

DATA_FILE = "results.json"

def save_extracted_titles(titles: List[str]):
    existing = get_extracted_titles()
    # Avoid duplicates if possible, or just append
    combined = list(set(existing + titles))
    with open(DATA_FILE, "w") as f:
        json.dump(combined, f)

def get_extracted_titles() -> List[str]:
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def clear_extracted_titles():
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
