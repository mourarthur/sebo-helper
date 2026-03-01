from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_pwa_route():
    response = client.get("/pwa")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Sebo Helper PWA" in response.text
    assert 'id="imageCanvas"' in response.text
    assert 'id="extractBtn"' in response.text
    assert 'id="ocr-progress-bar"' in response.text
    assert 'id="pwa-results-list"' in response.text

def test_service_worker_route():
    response = client.get("/service-worker.js")
    assert response.status_code == 200
    assert "application/javascript" in response.headers["content-type"]
    assert "CACHE_NAME" in response.text

def test_static_files_exist():
    files = [
        "/static/manifest.json",
        "/static/js/ocr-engine.js",
        "/static/js/image-processor.js",
        "/static/js/vendor/tesseract.min.js",
        "/static/js/vendor/opencv.js",
        "/static/js/vendor/lang-data/eng.traineddata.gz"
    ]
    for file_path in files:
        response = client.get(file_path)
        assert response.status_code == 200, f"File {file_path} not found"
