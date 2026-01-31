from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

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
