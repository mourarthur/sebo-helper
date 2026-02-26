import os

def test_wishlist_ui_elements_exist():
    template_path = "app/templates/index.html"
    assert os.path.exists(template_path)
    with open(template_path, "r") as f:
        content = f.read()
    
    # We expect these elements to be added
    assert 'id="wishlist-section"' in content
    assert 'id="wishlist-input"' in content
    assert 'id="save-wishlist-btn"' in content
