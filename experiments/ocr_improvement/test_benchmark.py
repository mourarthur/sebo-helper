import os
import pytest
from unittest.mock import MagicMock, patch
import sys

# Add the project root to the python path to import app modules if needed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Placeholder for the benchmark module we are about to create
# We will need to import the function that runs the benchmark
# from experiments.ocr_improvement import benchmark

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

