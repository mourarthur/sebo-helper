import sys
import os
import glob

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.ocr import extract_text

def run_baseline():
    image_dir = "sample-images"
    output_file = "conductor/tracks/improve_ocr_20260201/baseline_results.txt"
    
    images = glob.glob(os.path.join(image_dir, "*"))
    results = []

    print(f"Running baseline OCR on {len(images)} images...")

    for img_path in sorted(images):
        print(f"Processing {img_path}...")
        try:
            text = extract_text(img_path)
            results.append(f"--- File: {os.path.basename(img_path)} ---\n{text}\n\n")
        except Exception as e:
            results.append(f"--- File: {os.path.basename(img_path)} ---\nERROR: {str(e)}\n\n")

    with open(output_file, "w") as f:
        f.writelines(results)
    
    print(f"Baseline results saved to {output_file}")

if __name__ == "__main__":
    run_baseline()
