import os

def test_wishlist_js_logic_exists():
    template_path = "app/templates/index.html"
    assert os.path.exists(template_path)
    with open(template_path, "r") as f:
        content = f.read()
    
    # We expect these JS functions or fetch calls to be added
    assert "fetch('/wishlist')" in content
    assert "wishlist-input" in content
    assert "save-wishlist-btn" in content
    assert "fetchWishlist()" in content
