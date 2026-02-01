import pytesseract
from PIL import Image
import cv2
import numpy as np
from app.services.image_utils import detect_rotation, rotate_image

def extract_text(image_path: str) -> str:
    """
    Extracts text from an image using Tesseract OCR.
    Tries multiple rotations and PSM modes to maximize extraction.
    """
    img = cv2.imread(image_path)
    if img is None:
        return ""

    results = []

    def run_ocr(image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Basic pre-processing
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # PSM modes: 3 (Auto), 5 (Vertical), 11 (Sparse)
        for psm in [3, 5, 11]:
            text = pytesseract.image_to_string(thresh, config=f"--psm {psm}").strip()
            if len(text) > 10:
                results.append(text)

    # 1. Original
    run_ocr(img)
    
    # 2. Deskewed
    angle = detect_rotation(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
    if abs(angle) > 1.0:
        deskewed = rotate_image(img, angle)
        run_ocr(deskewed)

    # 3. Rotations (90 CW, 90 CCW, 180)
    for rot in [cv2.ROTATE_90_CLOCKWISE, cv2.ROTATE_90_COUNTERCLOCKWISE, cv2.ROTATE_180]:
        run_ocr(cv2.rotate(img, rot))

    # Combine all unique results
    if not results:
        return ""
        
    unique_results = []
    seen = set()
    for res in results:
        if res not in seen:
            unique_results.append(res)
            seen.add(res)
            
    return "\n---\n".join(unique_results)
