import os
import sys
import pytesseract
from PIL import Image

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
    args = parser.parse_args()
    
    benchmark_results = run_benchmark(args.directory)
    
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
