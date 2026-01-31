import pytesseract
from PIL import Image
import cv2
import numpy as np

def extract_text(image_path: str) -> str:
    """
    Extracts text from an image using Tesseract OCR.
    Includes basic pre-processing to improve accuracy.
    """
    # Load image using OpenCV
    img = cv2.imread(image_path)
    if img is None:
        return ""

    # Pre-processing
    # 1. Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 2. Thresholding (Otsu's binarization)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Extract text from processed image
    text = pytesseract.image_to_string(thresh)
    
    return text.strip()
