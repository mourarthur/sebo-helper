import os
import json
import pytest
from app.services.persistence import save_extracted_titles, get_extracted_titles, clear_extracted_titles

DATA_FILE = "test_results.json"

@pytest.fixture
def temp_data_file(monkeypatch):
    monkeypatch.setattr("app.services.persistence.DATA_FILE", DATA_FILE)
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
    yield
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)

def test_persistence_flow(temp_data_file):
    # 1. Save titles
    titles = ["Band A - Album 1", "Band B - Album 2"]
    save_extracted_titles(titles)
    
    # 2. Get titles
    loaded = get_extracted_titles()
    assert len(loaded) == 2
    assert "Band A - Album 1" in loaded
    
    # 3. Save more (append)
    save_extracted_titles(["Band C - Album 3"])
    loaded = get_extracted_titles()
    assert len(loaded) == 3
    
    # 4. Clear titles
    clear_extracted_titles()
    loaded = get_extracted_titles()
    assert len(loaded) == 0
