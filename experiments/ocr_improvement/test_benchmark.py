import os
import pytest
from unittest.mock import MagicMock, patch, ANY
import sys

# Add the project root to the python path to import app modules if needed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Now import benchmark
from experiments.ocr_improvement import benchmark

def test_benchmark_script_exists():
    """Test that the benchmark script exists."""
    assert os.path.exists("experiments/ocr_improvement/benchmark.py")

def test_load_ground_truth():
    """Test loading ground truth text files."""
    # This test assumes we will have a function load_ground_truth(image_path)
    # We will mock the file reading
    
    from experiments.ocr_improvement.benchmark import load_ground_truth
    
    with patch("builtins.open", new_callable=MagicMock) as mock_open:
        mock_file = MagicMock()
        mock_file.read.return_value = "Expected Text"
        mock_open.return_value.__enter__.return_value = mock_file
        
        text = load_ground_truth("sample-images/test.jpg")
        assert text == "Expected Text"
        mock_open.assert_called_with("sample-images/test.txt", "r", encoding="utf-8")

def test_run_benchmark_iteration():
    """Test that the benchmark iterates over images."""
    # This tests the main loop logic
    from experiments.ocr_improvement.benchmark import run_benchmark
    
    mock_ocr = MagicMock(return_value="Extracted Text")
    
    with patch("os.listdir", return_value=["img1.jpg", "img1.txt", "img2.jpeg"]), \
         patch("experiments.ocr_improvement.benchmark.load_ground_truth", return_value="Ground Truth"), \
         patch("experiments.ocr_improvement.benchmark.perform_ocr", mock_ocr):
        
        results = run_benchmark("sample-images")
        
        # We expect 2 images (img1.jpg, img2.jpeg) to be processed
        assert len(results) == 2
        assert results[0]['image'] == 'img1.jpg'
        assert results[0]['ground_truth'] == 'Ground Truth'
        assert results[0]['extracted'] == 'Extracted Text'

def test_calculate_accuracy():
    """Test the accuracy calculation function."""
    from experiments.ocr_improvement.benchmark import calculate_accuracy
    
    # Perfect match
    assert calculate_accuracy("test", "test") == 100.0
    
    # Complete mismatch (empty)
    assert calculate_accuracy("test", "") == 0.0
    assert calculate_accuracy("", "test") == 0.0
    
    # Partial match
    # Levenshtein distance between "kitten" and "sitting" is 3.
    # Max length is 7.
    # Accuracy = (1 - 3/7) * 100 = 57.14...
    score = calculate_accuracy("kitten", "sitting")
    assert 57.0 < score < 58.0

    # Case insensitivity check (optional, but good for OCR)
    # If we decide to normalize case, this would be 100. 
    # But usually strict Levenshtein is case-sensitive.
    # Let's assume strict for now.
    assert calculate_accuracy("Test", "test") < 100.0

def test_preprocess_image_rotates():
    """Test that preprocess_image rotates the image based on OSD."""
    from experiments.ocr_improvement.benchmark import preprocess_image
    
    mock_image = MagicMock()
    mock_image.rotate.return_value = mock_image # Simulate rotation
    
    with patch("pytesseract.image_to_osd") as mock_osd:
        mock_osd.return_value = {
            'page_number': 0, 'orientation': 270, 'rotate': 90, 'orientation_conf': 1.0, 'script': 'Latin', 'script_conf': 0.8
        }
        
        rotated_image = preprocess_image(mock_image)
        
        mock_image.rotate.assert_called_with(-90, expand=True)
        assert rotated_image is mock_image # Check if it returns the rotated image


def test_perform_ocr_with_config():
    """Test that perform_ocr passes Tesseract config to pytesseract."""
    from experiments.ocr_improvement.benchmark import perform_ocr
    with patch("pytesseract.image_to_string") as mock_tesseract, \
         patch("PIL.Image.open"): # Mock Image.open as well
        
        test_image_path = "sample-images/test.jpg"
        
        # Test with default config
        perform_ocr(test_image_path)
        mock_tesseract.assert_called_with(ANY, config="", lang=None)

        # Test with custom config
        custom_config = "--psm 6 --oem 1"
        perform_ocr(test_image_path, config=custom_config)
        mock_tesseract.assert_called_with(ANY, config=custom_config, lang=None)

def test_perform_ocr_with_lang():
    """Test that perform_ocr passes language to pytesseract."""
    from experiments.ocr_improvement.benchmark import perform_ocr
    with patch("pytesseract.image_to_string") as mock_tesseract, \
         patch("PIL.Image.open"): # Mock Image.open as well
        
        test_image_path = "sample-images/test.jpg"
        
        # Test with default lang (None)
        perform_ocr(test_image_path)
        mock_tesseract.assert_called_with(ANY, config="", lang=None)
        
        # Test with custom lang
        custom_lang = "eng+por"
        perform_ocr(test_image_path, lang=custom_lang)
        mock_tesseract.assert_called_with(ANY, config="", lang=custom_lang)

def test_easyocr_engine_selection():
    """Test that easyocr engine is selected and called correctly."""
    from experiments.ocr_improvement.benchmark import run_benchmark
    
    with patch("experiments.ocr_improvement.benchmark.perform_ocr_easyocr", return_value="EasyOCR Text") as MockPerformEasyOCR, \
         patch("experiments.ocr_improvement.benchmark.load_ground_truth", return_value="Ground Truth"), \
         patch("os.listdir", return_value=["img1.jpg"]), \
         patch("experiments.ocr_improvement.benchmark.perform_ocr", MagicMock(return_value="Tesseract Text")):
        
        results = run_benchmark("sample-images", ocr_engine="easyocr")
        
        MockPerformEasyOCR.assert_called_once_with("sample-images/img1.jpg", ANY) # ANY for reader_instance
        
        assert results[0]['extracted'] == "EasyOCR Text"
        assert 'accuracy' in results[0]

def test_tesseract_engine_selection():
    """Test that tesseract engine is selected and called correctly."""
    from experiments.ocr_improvement.benchmark import run_benchmark, perform_ocr
    
    mock_perform_ocr = MagicMock(return_value="Tesseract Text")
    
    with patch("experiments.ocr_improvement.benchmark.perform_ocr", mock_perform_ocr) as MockPerformOcr, \
         patch("experiments.ocr_improvement.benchmark.load_ground_truth", return_value="Ground Truth"), \
         patch("os.listdir", return_value=["img1.jpg"]), \
         patch("experiments.ocr_improvement.benchmark.perform_ocr_easyocr", MagicMock(return_value="EasyOCR Text")): # Ensure perform_ocr_easyocr is not called
        
        # Run benchmark with tesseract engine (default)
        results = run_benchmark("sample-images", ocr_engine="tesseract")
        
        MockPerformOcr.assert_called_once()
        assert results[0]['extracted'] == "Tesseract Text"
        assert 'accuracy' in results[0]

