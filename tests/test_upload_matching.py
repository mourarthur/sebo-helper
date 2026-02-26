from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch
from io import BytesIO
from PIL import Image

client = TestClient(app)

def test_upload_with_matching():
    # 0. Clear previous results and wishlist
    client.post("/clear")
    client.post("/wishlist", json={"items": []})
    
    # 1. Set wishlist
    wishlist_items = ["Beatles", "Agatha Christie"]
    client.post("/wishlist", json={"items": wishlist_items})
    
    # 2. Mock OCR to return specific titles
    with patch("app.main.extract_text") as mock_ocr:
        mock_ocr.return_value = "The Beatles - Revolver\nRandom Book Title\nAgatha Christie - Peril at End House"
        
        # 3. Upload dummy image
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
        
        # We expect "all_titles" to now be a list of dicts with match info
        assert "all_titles" in data
        titles = data["all_titles"]
        
        # We sort titles by text to ensure stable comparison if set() shuffled them
        titles.sort(key=lambda x: x["text"])
        
        # Sorted order: Agatha..., Random..., The Beatles...
        assert titles[0]["text"] == "Agatha Christie - Peril at End House"
        assert titles[0]["is_match"] == True
        
        assert titles[1]["text"] == "Random Book Title"
        assert titles[1]["is_match"] == False
        
        assert titles[2]["text"] == "The Beatles - Revolver"
        assert titles[2]["is_match"] == True
