import pytest
from app.services.ocr import extract_text
from PIL import Image
from io import BytesIO
import os
from unittest.mock import patch, ANY
import numpy as np # For mocking cv2 image

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

def test_extract_text_uses_psm12():
    """Test that extract_text uses PSM 12 config for Tesseract."""
    # Mock pytesseract.image_to_string to check config argument
    with patch("app.services.ocr.pytesseract.image_to_string") as mock_tesseract_string, \
         patch("app.services.ocr.cv2.imread", return_value=np.zeros((100, 100, 3), dtype=np.uint8)):
        
        # Call extract_text with a dummy path
        extract_text("dummy_image.png")
        
        # Assert that image_to_string was called with '--psm 12'
        # Note: ANY is used for the image argument since we don't care about the exact array passed here
        mock_tesseract_string.assert_called()
        args, kwargs = mock_tesseract_string.call_args
        assert kwargs.get('config') == '--psm 12'

