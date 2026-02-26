import pytest
# We'll import after creating the file or just use the expected name
# from app.services.matching import is_match

def test_simple_match():
    from app.services.matching import is_match
    assert is_match("Beatles - Revolver", ["Beatles - Revolver"]) == True
    assert is_match("BEATLES - REVOLVER", ["Beatles - Revolver"]) == True
    assert is_match("Beatles - Revolver", ["Agatha Christie", "Beatles - Revolver"]) == True

def test_no_match():
    from app.services.matching import is_match
    assert is_match("Rolling Stones - Let It Bleed", ["Beatles - Revolver"]) == False
    assert is_match("Unknown Title", []) == False

def test_partial_match():
    # Spec said "Initial matching can be simple string inclusion or exact match"
    # Let's aim for case-insensitive inclusion.
    from app.services.matching import is_match
    assert is_match("The Beatles - Revolver", ["Revolver"]) == True
    assert is_match("Revolver", ["The Beatles - Revolver"]) == True
