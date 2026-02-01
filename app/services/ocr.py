import pytesseract
import cv2
import numpy as np
from typing import List, Set
from app.services.image_utils import detect_rotation, rotate_image

def _get_ocr_result(img: np.ndarray, psm: int) -> str:
    """Performs OCR on an image with a specific PSM mode."""
    config = f"--psm {psm}"
    try:
        return pytesseract.image_to_string(img, config=config).strip()
    except Exception:
        return ""

def _preprocess_image(img: np.ndarray) -> np.ndarray:
    """Applies standard pre-processing for OCR."""
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img
    
    # Otsu's thresholding
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh

def extract_text(image_path: str) -> str:
    """
    Extracts text from an image using a multi-pass Tesseract OCR strategy. 
    
    This function attempts multiple rotations and Page Segmentation Modes (PSM)
    to maximize text extraction from varied media spine orientations.
    """
    img = cv2.imread(image_path)
    if img is None:
        return ""

    raw_results: List[str] = []

    def process_rotation(image: np.ndarray):
        thresh = _preprocess_image(image)
        # Try different segmentation modes
        # 3: Auto, 5: Vertical, 11: Sparse
        for psm in [3, 5, 11]:
            text = _get_ocr_result(thresh, psm)
            if len(text) > 5:  # Ignore very short noise
                raw_results.append(text)

    # 1. Original orientation
    process_rotation(img)
    
    # 2. Deskewed orientation
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    angle = detect_rotation(gray)
    if abs(angle) > 1.0:
        deskewed = rotate_image(img, angle)
        process_rotation(deskewed)

    # 3. Fixed Rotations (90 CW, 90 CCW, 180)
    for rot in [cv2.ROTATE_90_CLOCKWISE, cv2.ROTATE_90_COUNTERCLOCKWISE, cv2.ROTATE_180]:
        rotated = cv2.rotate(img, rot)
        process_rotation(rotated)

    # Deduplicate and format results
    unique_results: List[str] = []
    seen: Set[str] = set()
    
    for res in raw_results:
        # Simple cleanup
        cleaned = res.strip()
        if cleaned and cleaned not in seen:
            unique_results.append(cleaned)
            seen.add(cleaned)
            
    return "\n---\n".join(unique_results)