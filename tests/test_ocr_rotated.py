import pytest
import os
from app.services.ocr import extract_text

@pytest.mark.parametrize("image_name, expected_keywords", [
    ("OCR2_colecao-agatha.jpeg", ["elefantes", "agatha", "christie"]),
    ("OCR3_colecao-agatha-boa.jpeg", ["morte", "nil", "agatha", "christie"]),
    ("OCR4_colecao-legiao.jpeg", ["urban"]),
])
def test_extract_text_rotated(image_name, expected_keywords):
    image_path = os.path.join("sample-images", image_name)
    if not os.path.exists(image_path):
        pytest.skip(f"Test image {image_path} not found")
    
    text = extract_text(image_path).lower()
    
    for keyword in expected_keywords:
        assert keyword.lower() in text, f"Keyword '{keyword}' not found in OCR result for {image_name}"
