from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_pwa_route():
    response = client.get("/pwa")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Sebo Helper PWA" in response.text
    assert 'rel="manifest"' in response.text

def test_service_worker_route():
    response = client.get("/service-worker.js")
    assert response.status_code == 200
    assert "application/javascript" in response.headers["content-type"]
    assert "CACHE_NAME" in response.text

def test_manifest_exists():
    response = client.get("/static/manifest.json")
    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]
