import os

def test_wishlist_match_css_class_exists():
    css_path = "app/static/css/style.css"
    assert os.path.exists(css_path)
    with open(css_path, "r") as f:
        content = f.read()
    assert ".wishlist-match" in content
