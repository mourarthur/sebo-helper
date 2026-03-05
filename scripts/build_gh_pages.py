import os
import shutil
import re

# Configuration
REPO_NAME = "sebo-helper"  # Default assumption, can be changed if user has different repo name
OUTPUT_DIR = "docs"
STATIC_DIR = "app/static"
TEMPLATE_FILE = "app/templates/pwa.html"
BASE_TEMPLATE = "app/templates/base.html"

def clean_and_create_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

def copy_static_assets():
    # Copy app/static to docs/static
    dest_static = os.path.join(OUTPUT_DIR, "static")
    shutil.copytree(STATIC_DIR, dest_static)
    
    # Move service-worker.js from docs/static/service-worker.js to docs/service-worker.js
    # (Since in local dev it's served from root but lives in static, or via route)
    # Actually, in the project structure, it is in app/static/service-worker.js
    # We want it at the root of docs/ for scope reasons.
    src_sw = os.path.join(dest_static, "service-worker.js")
    dst_sw = os.path.join(OUTPUT_DIR, "service-worker.js")
    if os.path.exists(src_sw):
        shutil.move(src_sw, dst_sw)
        print(f"Moved service-worker.js to root of {OUTPUT_DIR}")

def process_html():
    # We need to manually "render" the template since we aren't running Flask/FastAPI
    # 1. Read Base
    with open(BASE_TEMPLATE, "r") as f:
        base_content = f.read()
    
    # 2. Read PWA Template
    with open(TEMPLATE_FILE, "r") as f:
        pwa_content = f.read()

    # 3. Naive Jinja2 Inheritance Resolution (Specific to this project's simple structure)
    # Extract blocks from pwa.html
    title_match = re.search(r'{% block title %}(.*?){% endblock %}', pwa_content, re.DOTALL)
    title = title_match.group(1) if title_match else "Sebo Helper"

    head_meta_match = re.search(r'{% block head_meta %}(.*?){% endblock %}', pwa_content, re.DOTALL)
    head_meta = head_meta_match.group(1) if head_meta_match else ""
    
    content_match = re.search(r'{% block content %}(.*?){% endblock %}', pwa_content, re.DOTALL)
    content = content_match.group(1) if content_match else ""

    # Replace blocks in base_content
    html = base_content.replace('{% block title %}Sebo Helper{% endblock %}', title)
    html = html.replace('{% block head_meta %}{% endblock %}', head_meta)
    html = html.replace('{% block content %}{% endblock %}', content)

    # 4. Inject Privacy Meta Tags (Anti-Crawling)
    privacy_tags = '<meta name="robots" content="noindex, nofollow, noarchive, noimageindex, notranslate">'
    html = html.replace('<head>', f'<head>\n    {privacy_tags}')

    # 5. Fix Links/Paths for Static Hosting
    # Replace url_for('static', path='...') -> ./static/...
    # Regex for {{ url_for('static', path='/css/style.css') }}
    html = re.sub(r"\{\{ url_for\('static', path='(.*?)'\) \}\}", r".\1", html)
    
    # Replace absolute /static/ paths with relative ./static/
    html = html.replace('"/static/', '"./static/')
    html = html.replace("'/static/", "'./static/")
    
    # Replace service worker registration path
    html = html.replace("'/service-worker.js'", "'./service-worker.js'")
    html = html.replace('"/service-worker.js"', '"./service-worker.js"')
    
    # Replace Tesseract worker paths
    # We need to manually adjust the paths in ocr-engine.js because they are hardcoded
    # But wait, ocr-engine.js is a static file. 
    # We should probably do a replace on the file content in docs/static/js/ocr-engine.js
    
    # Write index.html
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w") as f:
        f.write(html)
    print("Generated docs/index.html")

def process_js_files():
    # Fix paths in ocr-engine.js
    ocr_path = os.path.join(OUTPUT_DIR, "static/js/ocr-engine.js")
    if os.path.exists(ocr_path):
        with open(ocr_path, "r") as f:
            content = f.read()
        
        # Replace absolute paths with relative ones for GH Pages
        # /static/js/vendor/ -> ./static/js/vendor/
        content = content.replace("'/static/", "'./static/")
        content = content.replace('"/static/', '"./static/')
        
        with open(ocr_path, "w") as f:
            f.write(content)
        print("Updated docs/static/js/ocr-engine.js")

def process_service_worker():
    sw_path = os.path.join(OUTPUT_DIR, "service-worker.js")
    with open(sw_path, "r") as f:
        content = f.read()
    
    # Update cache paths to be relative
    # The SW runs at root (docs/), so ./static/... is correct
    content = content.replace("'/static/", "'./static/")
    
    # Update the cache list to include the relative start URL
    # /pwa -> ./index.html (since we are generating index.html)
    content = content.replace("'/pwa'", "'./index.html', './'")
    
    with open(sw_path, "w") as f:
        f.write(content)
    print("Updated docs/service-worker.js")

def create_robots_txt():
    with open(os.path.join(OUTPUT_DIR, "robots.txt"), "w") as f:
        f.write("User-agent: *\nDisallow: /")
    print("Created docs/robots.txt")

def create_nojekyll():
    # .nojekyll prevents GitHub Pages from ignoring files starting with _
    with open(os.path.join(OUTPUT_DIR, ".nojekyll"), "w") as f:
        f.write("")

def main():
    print("Building static site for GitHub Pages...")
    clean_and_create_dir(OUTPUT_DIR)
    copy_static_assets()
    process_html()
    process_js_files()
    process_service_worker()
    create_robots_txt()
    create_nojekyll()
    print("Build complete in folder: docs/")

if __name__ == "__main__":
    main()
