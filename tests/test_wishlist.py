import os
import json
import pytest
from app.services.wishlist import save_wishlist, get_wishlist, clear_wishlist

WISHLIST_FILE = "test_wishlist.json"

@pytest.fixture
def temp_wishlist_file(monkeypatch):
    # Using app.services.wishlist.WISHLIST_FILE
    monkeypatch.setattr("app.services.wishlist.WISHLIST_FILE", WISHLIST_FILE)
    if os.path.exists(WISHLIST_FILE):
        os.remove(WISHLIST_FILE)
    yield
    if os.path.exists(WISHLIST_FILE):
        os.remove(WISHLIST_FILE)

def test_wishlist_flow(temp_wishlist_file):
    # 1. Initial wishlist should be empty
    assert get_wishlist() == []
    
    # 2. Save wishlist
    items = ["Artist A - Album 1", "Artist B - Album 2"]
    save_wishlist(items)
    
    # 3. Get wishlist
    loaded = get_wishlist()
    assert len(loaded) == 2
    assert "Artist A - Album 1" in loaded
    assert "Artist B - Album 2" in loaded
    
    # 4. Save wishlist should replace previous list
    new_items = ["Artist C - Album 3"]
    save_wishlist(new_items)
    loaded = get_wishlist()
    assert len(loaded) == 1
    assert "Artist C - Album 3" in loaded
    
    # 5. Clear wishlist
    clear_wishlist()
    loaded = get_wishlist()
    assert len(loaded) == 0
