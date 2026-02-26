import os

def test_results_highlighting_js_exists():
    template_path = "app/templates/index.html"
    assert os.path.exists(template_path)
    with open(template_path, "r") as f:
        content = f.read()
    
    # We expect updateResultsList to check for is_match and add the class
    assert "updateResultsList(titles)" in content
    assert "is_match" in content
    assert "wishlist-match" in content
