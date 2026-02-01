import pytesseract
import cv2
import os
import glob

image_dir = "sample-images"
images = glob.glob(os.path.join(image_dir, "*"))

for img_path in sorted(images):
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    print(f"--- File: {os.path.basename(img_path)} ---")
    for psm in [3, 5, 6, 11]:
        text = pytesseract.image_to_string(thresh, config=f"--psm {psm}").strip()
        print(f"PSM {psm}: {text[:50]}...")
    print()
