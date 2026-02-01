import pytesseract
import cv2
import os

img_path = "sample-images/OCR6_colecao-muitos-cds.jpeg"
img = cv2.imread(img_path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

for psm in [3, 4, 5, 6, 11, 12]:
    text = pytesseract.image_to_string(thresh, config=f"--psm {psm}").strip()
    print(f"PSM {psm}: {text[:100]}...")
