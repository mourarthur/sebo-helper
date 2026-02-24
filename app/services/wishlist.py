import json
import os
from typing import List

WISHLIST_FILE = "wishlist.json"

def save_wishlist(items: List[str]):
    """Saves the wishlist items, replacing the current list."""
    with open(WISHLIST_FILE, "w") as f:
        json.dump(items, f)

def get_wishlist() -> List[str]:
    """Retrieves the wishlist items from disk."""
    if not os.path.exists(WISHLIST_FILE):
        return []
    try:
        with open(WISHLIST_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def clear_wishlist():
    """Clears the wishlist from disk."""
    if os.path.exists(WISHLIST_FILE):
        os.remove(WISHLIST_FILE)
