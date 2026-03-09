import easyocr
import cv2
import numpy as np
from typing import Optional

# Singleton instance for EasyOCR reader
_reader: Optional[easyocr.Reader] = None

def get_reader() -> easyocr.Reader:
    """
    Returns a singleton instance of the EasyOCR Reader.
    Initializes with English and Portuguese support.
    """
    global _reader
    if _reader is None:
        # gpu=False ensures it runs on CPU if no CUDA is available.
        _reader = easyocr.Reader(['en', 'pt'], gpu=False)
    return _reader

def extract_text(image_path: str) -> str:
    """
    Extracts text from an image using a Dual-Pass EasyOCR strategy.
    
    Iteration 2 findings showed that:
    1. EasyOCR is significantly more robust for CD spines (80% recall).
    2. A single rotation-aware pass causes regressions in dense CD layouts.
    3. A Dual-Pass approach (standard + rotated) provides the best coverage 
       for both horizontal CD spines and vertical book spines.
    """
    try:
        reader = get_reader()
        
        # Pass 1: Standard detection (Optimized for horizontal/dense text)
        results_standard = reader.readtext(image_path)
        text_standard = "\n".join([res[1] for res in results_standard])
        
        # Pass 2: Rotation-aware detection (Optimized for vertical book/CD spines)
        # We focus on 90 and 270 degrees which are most common for spines.
        results_rotated = reader.readtext(image_path, rotation_info=[90, 270])
        text_rotated = "\n".join([res[1] for res in results_rotated])
        
        # Combine both passes to ensure maximum coverage
        combined_text = text_standard + "\n" + text_rotated
        
        return combined_text.strip()
    except Exception as e:
        print(f"Error during EasyOCR processing: {e}")
        return ""
