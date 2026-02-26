from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch
from io import BytesIO
from PIL import Image

client = TestClient(app)

def test_full_flow():
    # 1. Clear state
    client.post("/clear")
    
    # 2. Setup Wishlist with some titles
    wishlist = ["The Beatles", "Agatha Christie", "Pink Floyd"]
    client.post("/wishlist", json={"items": wishlist})
    
    # 3. Verify wishlist is saved
    response = client.get("/wishlist")
    assert response.json()["wishlist"] == wishlist
    
    # 4. Upload image (Mocked OCR)
    mock_text = "The Beatles - Abbey Road\nAgata Christie - Murder\nDark Side of the Moon\nSome Other Band"
    with patch("app.main.extract_text") as mock_ocr:
        mock_ocr.return_value = mock_text
        
        file_content = BytesIO()
        image = Image.new("RGB", (100, 100), color="red")
        image.save(file_content, format="JPEG")
        file_content.seek(0)
        
        response = client.post(
            "/upload",
            files={"file": ("test.jpg", file_content, "image/jpeg")}
        )
        assert response.status_code == 200
        data = response.json()
        
        titles = data["all_titles"]
        
        def find_title(text):
            return next(t for t in titles if t["text"] == text)
            
        assert find_title("The Beatles - Abbey Road")["is_match"] == True
        assert find_title("Agata Christie - Murder")["is_match"] == True
        assert find_title("Dark Side of the Moon")["is_match"] == False
        
    # 5. Clear results
    client.post("/clear")
    response = client.get("/results")
    assert response.json()["titles"] == []
