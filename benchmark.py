#!/usr/bin/env python3
"""
Benchmark the OCR pipeline against the img-impr dataset.

Replicates the browser pipeline:
  - Preprocessing: grayscale → CLAHE → Gaussian blur → adaptive threshold → morph close
  - Tesseract PSM 12 (SPARSE_TEXT_OSD), languages: eng+por
  - Three passes: 0°, 90° CW, 90° CCW
  - Deduplicated combined output

Metric: token recall — fraction of ground-truth tokens found in OCR output.
"""

import os
import re
import unicodedata
import cv2
import numpy as np
import pytesseract
from pathlib import Path

TESSDATA_DIR = "/tmp/tessdata"
IMAGES_DIR = Path("training-images/img-impr")
GT_DIR = Path("training-images/ground-truth")
LANGS = "eng+por"
PSM = 12  # SPARSE_TEXT_OSD
MAX_DIM = 2000  # matches app's display/OCR scale

pytesseract.pytesseract.tesseract_cmd = "tesseract"
TESS_CONFIG = f"--tessdata-dir {TESSDATA_DIR} --psm {PSM} -l {LANGS}"


def load_image(path: Path) -> np.ndarray:
    img = cv2.imread(str(path), cv2.IMREAD_COLOR)
    h, w = img.shape[:2]
    if max(h, w) > MAX_DIM:
        scale = MAX_DIM / max(h, w)
        img = cv2.resize(img, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)
    return img


def preprocess(img: np.ndarray) -> np.ndarray:
    # Grayscale-only: benchmarked best on img-impr phone photos.
    # Binarization (adaptive/Otsu) destroys gradient info Tesseract LSTM needs.
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def run_ocr(img: np.ndarray) -> str:
    return pytesseract.image_to_string(img, config=TESS_CONFIG)


def three_pass_ocr(path: Path) -> set[str]:
    orig = load_image(path)
    cw = cv2.rotate(orig, cv2.ROTATE_90_CLOCKWISE)
    ccw = cv2.rotate(orig, cv2.ROTATE_90_COUNTERCLOCKWISE)

    text = "\n".join([
        run_ocr(preprocess(orig)),
        run_ocr(preprocess(cw)),
        run_ocr(preprocess(ccw)),
    ])

    lines = {l.strip() for l in text.splitlines() if l.strip()}
    return lines


def normalize(s: str) -> str:
    """Lowercase, strip accents, keep only alphanum."""
    s = s.lower()
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    return s


def tokenize(s: str) -> set[str]:
    tokens = normalize(s).split()
    return {t for t in tokens if len(t) >= 3}


def load_ground_truth(path: Path) -> set[str]:
    return tokenize(path.read_text(encoding="utf-8"))


def token_recall(gt_tokens: set[str], ocr_lines: set[str]) -> float:
    if not gt_tokens:
        return 1.0
    ocr_tokens = tokenize("\n".join(ocr_lines))
    matched = gt_tokens & ocr_tokens
    return len(matched) / len(gt_tokens)


def main():
    images = sorted(IMAGES_DIR.glob("*.jpg"))
    if not images:
        print(f"No images found in {IMAGES_DIR}")
        return

    results = []
    print(f"{'Image':<15} {'Recall':>7}  {'GT tokens':>10}  {'Matched':>8}")
    print("-" * 50)

    for img_path in images:
        gt_path = GT_DIR / (img_path.stem + ".txt")
        if not gt_path.exists():
            print(f"{img_path.name:<15}  (no ground truth)")
            continue

        gt_tokens = load_ground_truth(gt_path)
        ocr_lines = three_pass_ocr(img_path)
        recall = token_recall(gt_tokens, ocr_lines)
        matched = int(recall * len(gt_tokens))

        results.append(recall)
        print(f"{img_path.name:<15} {recall:>7.1%}  {len(gt_tokens):>10}  {matched:>8}")

    if results:
        avg = sum(results) / len(results)
        print("-" * 50)
        print(f"{'AVERAGE':<15} {avg:>7.1%}")
        print(f"\nImages evaluated: {len(results)}/{len(images)}")


if __name__ == "__main__":
    main()
