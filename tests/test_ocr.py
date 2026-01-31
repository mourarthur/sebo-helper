import pytest
from app.services.ocr import extract_text
from PIL import Image
from io import BytesIO
import os

def test_extract_text_basic():
    # Create a simple image with text "TEST"
    from PIL import ImageDraw, ImageFont
    
    img = Image.new('RGB', (200, 100), color = (255, 255, 255))
    d = ImageDraw.Draw(img)
    # Using default font
    d.text((10,10), "TEST", fill=(0,0,0))
    
    temp_path = "test_ocr.png"
    img.save(temp_path)
    
    try:
        text = extract_text(temp_path)
        assert "TEST" in text.upper()
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
