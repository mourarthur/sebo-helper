import pytesseract
import cv2
import os

img_path = "sample-images/OCR6_colecao-muitos-cds.jpeg"
img = cv2.imread(img_path)

for rot in [cv2.ROTATE_90_CLOCKWISE, cv2.ROTATE_90_COUNTERCLOCKWISE, cv2.ROTATE_180]:
    rotated = cv2.rotate(img, rot)
    gray = cv2.cvtColor(rotated, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    print(f"Rotation {rot}:")
    print(pytesseract.image_to_string(thresh, config="--psm 3").strip()[:100])