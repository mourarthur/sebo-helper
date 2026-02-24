from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Sebo Helper" in response.text

def test_upload_image():
    # Creating a dummy image in memory
    from io import BytesIO
    from PIL import Image
    
    file_content = BytesIO()
    image = Image.new("RGB", (100, 100), color="red")
    image.save(file_content, format="JPEG")
    file_content.seek(0)
    
    response = client.post(
        "/upload",
        files={"file": ("test.jpg", file_content, "image/jpeg")}
    )
    assert response.status_code == 200
    assert "filename" in response.json()
    assert response.json()["filename"] == "test.jpg"

def test_wishlist_endpoints():
    # 1. Clear results/wishlist if necessary for clean test
    # (Optional: might want a fixture if tests depend on persistent state)
    
    # 2. Get wishlist (empty)
    response = client.get("/wishlist")
    assert response.status_code == 200
    # Could be empty or have items from other tests if not using fixture
    # Let's assume clean state for now or focus on the flow
    
    # 3. Post items
    items = ["New Artist - New Album"]
    response = client.post("/wishlist", json={"items": items})
    assert response.status_code == 200
    assert response.json()["message"] == "Wishlist updated"
    
    # 4. Get items again
    response = client.get("/wishlist")
    assert response.status_code == 200
    assert "New Artist - New Album" in response.json()["wishlist"]
