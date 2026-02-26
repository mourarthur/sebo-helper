import os

def test_responsive_css_exists():
    css_path = "app/static/css/style.css"
    assert os.path.exists(css_path)
    with open(css_path, "r") as f:
        content = f.read()
    
    # We expect some media queries for smaller screens
    assert "@media" in content
