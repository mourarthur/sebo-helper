import os
import sys
import pytesseract
from PIL import Image
import easyocr

_easyocr_reader = None

def get_easyocr_reader():
    global _easyocr_reader
    if _easyocr_reader is None:
        # languages can be 'en', 'ch_sim', 'ja', 'ko', etc.
        _easyocr_reader = easyocr.Reader(['en', 'pt']) # 'en' for English, 'pt' for Portuguese
    return _easyocr_reader

def levenshtein_distance(s1: str, s2: str) -> int:
    """Calculates the Levenshtein edit distance between two strings."""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

def calculate_accuracy(s1: str, s2: str) -> float:
    """Calculates accuracy score based on Levenshtein distance (0-100)."""
    dist = levenshtein_distance(s1, s2)
    max_len = max(len(s1), len(s2))
    if max_len == 0:
        return 100.0 if dist == 0 else 0.0
    return (1 - dist / max_len) * 100

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

def perform_ocr(image_path: str, config: str = "", lang: str = None, preprocess: bool = False) -> str:
    """
    Runs Tesseract OCR on the image at the given path.
    Accepts Tesseract configuration string, language, and a preprocess flag.
    """
    try:
        image = Image.open(image_path)
        if preprocess:
            image = preprocess_image(image)
        text = pytesseract.image_to_string(image, config=config, lang=lang)
        return text.strip()
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return ""

def preprocess_image(image: Image.Image) -> Image.Image:
    """
    Performs basic image preprocessing, specifically rotation based on Tesseract OSD.
    """
    try:
        # Get OSD (Orientation and Script Detection) information
        osd_data = pytesseract.image_to_osd(image, output_type=pytesseract.Output.DICT)
        rotate_angle = osd_data.get('rotate', 0)
        
        if rotate_angle != 0:
            print(f"Detected rotation: {rotate_angle} degrees. Rotating image.")
            # PIL rotate is counter-clockwise, so we pass negative angle
            # expand=True resizes the image to fit the new dimensions
            return image.rotate(-rotate_angle, expand=True)
        return image
    except Exception as e:
        print(f"Error during preprocessing: {e}")
        return image

def perform_ocr_easyocr(image_path: str, reader_instance) -> str:
    """
    Runs EasyOCR on the image at the given path.
    """
    try:
        # EasyOCR expects image path or numpy array
        # It handles its own preprocessing and rotation
        result = reader_instance.readtext(image_path)
        extracted_text = " ".join([text[1] for text in result])
        return extracted_text.strip()
    except Exception as e:
        print(f"Error processing {image_path} with EasyOCR: {e}")
        return ""

def run_benchmark(images_dir: str, tesseract_config: str = "", lang: str = None, preprocess: bool = False, ocr_engine: str = "tesseract") -> list[dict]:
    """
    Iterates through images in the directory, runs OCR, and compares with ground truth.
    Returns a list of result dictionaries.
    """
    results = []
    supported_exts = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')
    
    # Initialize EasyOCR reader once if needed
    easyocr_reader_instance = None
    if ocr_engine == "easyocr":
        easyocr_reader_instance = get_easyocr_reader()

    for filename in os.listdir(images_dir):
        if filename.lower().endswith(supported_exts):
            image_path = os.path.join(images_dir, filename)
            ground_truth = load_ground_truth(image_path)
            
            if ocr_engine == "tesseract":
                extracted_text = perform_ocr(image_path, config=tesseract_config, lang=lang, preprocess=preprocess)
            elif ocr_engine == "easyocr":
                extracted_text = perform_ocr_easyocr(image_path, easyocr_reader_instance)
            else:
                raise ValueError(f"Unknown OCR engine: {ocr_engine}")
            
            # Simple Levenshtein accuracy
            accuracy = calculate_accuracy(ground_truth, extracted_text)
            
            results.append({
                'image': filename,
                'ground_truth': ground_truth,
                'extracted': extracted_text,
                'accuracy': accuracy
            })
            
    return results

def generate_markdown_report(results: list[dict], output_file: str):
    """Generates a markdown report from benchmark results."""
    import datetime
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# OCR Benchmark Results\n\n")
        f.write(f"**Date:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        avg_acc = 0.0
        if results:
            avg_acc = sum(r['accuracy'] for r in results) / len(results)
        
        f.write(f"**Average Accuracy:** {avg_acc:.2f}%\n")
        f.write(f"**Total Images:** {len(results)}\n\n")
        
        f.write("| Image | Accuracy | Ground Truth (Snippet) | Extracted (Snippet) |\n")
        f.write("| :--- | :--- | :--- | :--- |\n")
        
        for res in results:
            gt = res['ground_truth'].replace('\n', ' ')[:50]
            ext = res['extracted'].replace('\n', ' ')[:50]
            # Escape pipes to avoid breaking markdown table
            gt = gt.replace('|', '\\|')
            ext = ext.replace('|', '\\|')
            f.write(f"| {res['image']} | {res['accuracy']:.2f}% | {gt}... | {ext}... |\n")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run OCR Benchmark")
    parser.add_argument("directory", nargs="?", default="sample-images", help="Path to images directory")
    parser.add_argument("--report", help="Path to output markdown report")
    parser.add_argument("--psm", type=int, choices=range(0, 14), help="Tesseract Page Segmentation Mode (0-13)")
    parser.add_argument("--oem", type=int, choices=range(0, 4), help="Tesseract OCR Engine Mode (0-3)")
    parser.add_argument("--lang", default="eng", help="Tesseract language code(s) (e.g., eng, por, eng+por)")
    parser.add_argument("--config", default="", help="Additional Tesseract config string")
    parser.add_argument("--preprocess", action="store_true", help="Enable image preprocessing (rotation detection) for Tesseract.")
    parser.add_argument("--engine", default="tesseract", choices=["tesseract", "easyocr"], help="OCR engine to use (tesseract or easyocr)")
    
    args = parser.parse_args()

    tesseract_config = args.config
    if args.psm is not None:
        tesseract_config += f" --psm {args.psm}"
    if args.oem is not None:
        tesseract_config += f" --oem {args.oem}"

    benchmark_results = run_benchmark(args.directory, tesseract_config, args.lang, args.preprocess, args.engine)
    
    if args.report:
        generate_markdown_report(benchmark_results, args.report)
        print(f"Report generated at {args.report}")

    total_accuracy = 0.0
    for res in benchmark_results:
        print(f"Image: {res['image']}")
        print(f"Accuracy: {res['accuracy']:.2f}%")
        # Truncate output for readability if too long
        print(f"Ground Truth (first 100 chars): {res['ground_truth'][:100]}...")
        print(f"Extracted (first 100 chars): {res['extracted'][:100]}...")
        print("-" * 20)
        total_accuracy += res['accuracy']
    
    if benchmark_results:
        avg_accuracy = total_accuracy / len(benchmark_results)
        print(f"\nAverage Accuracy: {avg_accuracy:.2f}%")
