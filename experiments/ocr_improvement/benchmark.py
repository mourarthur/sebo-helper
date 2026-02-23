import os
import sys
import pytesseract
from PIL import Image

def load_ground_truth(image_path: str) -> str:
    """
    Loads the corresponding ground truth text file for a given image path.
    Assumes the text file has the same basename as the image but with .txt extension.
    """
    base_name = os.path.splitext(image_path)[0]
    txt_path = f"{base_name}.txt"
    try:
        with open(txt_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        return ""

def perform_ocr(image_path: str) -> str:
    """
    Runs Tesseract OCR on the image at the given path.
    """
    try:
        text = pytesseract.image_to_string(Image.open(image_path))
        return text.strip()
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return ""

def run_benchmark(images_dir: str) -> list[dict]:
    """
    Iterates through images in the directory, runs OCR, and compares with ground truth.
    Returns a list of result dictionaries.
    """
    results = []
    supported_exts = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')
    
    for filename in os.listdir(images_dir):
        if filename.lower().endswith(supported_exts):
            image_path = os.path.join(images_dir, filename)
            ground_truth = load_ground_truth(image_path)
            extracted_text = perform_ocr(image_path)
            
            results.append({
                'image': filename,
                'ground_truth': ground_truth,
                'extracted': extracted_text
            })
            
    return results

if __name__ == "__main__":
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        directory = "sample-images"
    
    benchmark_results = run_benchmark(directory)
    for res in benchmark_results:
        print(f"Image: {res['image']}")
        print(f"Ground Truth: {res['ground_truth']}")
        print(f"Extracted: {res['extracted']}")
        print("-" * 20)
