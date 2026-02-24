import os
import sys
import glob

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Import from app and experiments
try:
    from app.services.ocr import extract_text
    # We need to add the experiments directory to path as well to import benchmark
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
    from ocr_improvement.benchmark import calculate_accuracy, load_ground_truth
except ImportError as e:
    print(f"Error importing modules: {e}")
    sys.exit(1)

def run_benchmark_current_impl(images_dir: str):
    if not os.path.exists(images_dir):
        print(f"Directory not found: {images_dir}")
        return

    print(f"Benchmarking current implementation in app/services/ocr.py on {images_dir}")
    
    results = []
    supported_exts = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')
    
    files = [f for f in os.listdir(images_dir) if f.lower().endswith(supported_exts)]
    
    for filename in files:
        image_path = os.path.join(images_dir, filename)
        # Load ground truth using the helper from benchmark.py
        # If load_ground_truth is not available, we can mock it or reimplement
        ground_truth = load_ground_truth(image_path)
        
        try:
            extracted_text = extract_text(image_path)
            
            # Comparison
            accuracy = calculate_accuracy(ground_truth, extracted_text)
            
            results.append({
                'image': filename,
                'accuracy': accuracy
            })
            
            print(f"Image: {filename} | Accuracy: {accuracy:.2f}%")
            
        except Exception as e:
            print(f"Error processing {filename}: {e}")

    if results:
        avg_acc = sum(r['accuracy'] for r in results) / len(results)
        print(f"\nAverage Accuracy: {avg_acc:.2f}%")
        print(f"Total Images: {len(results)}")

if __name__ == "__main__":
    # Assuming run from project root
    target_dir = "sample-images"
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
    run_benchmark_current_impl(target_dir)
