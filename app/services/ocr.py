import pytesseract
import cv2
import numpy as np

def extract_text(image_path: str) -> str:
    """
    Extracts text from an image using Tesseract OCR with PSM 12.
    
    This configuration (Sparse text with OSD) was found to be the most effective
    for the book spine dataset, outperforming multi-pass strategies.
    """
    img = cv2.imread(image_path)
    if img is None:
        return ""

    # Tesseract expects RGB, OpenCV gives BGR
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # PSM 12: Sparse text with OSD. 
    # This handles different orientations and sparse text regions effectively.
    config = "--psm 12"
    
    try:
        text = pytesseract.image_to_string(img_rgb, config=config).strip()
        return text
    except Exception as e:
        print(f"Error during OCR processing: {e}")
        return ""