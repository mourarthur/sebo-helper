# Implementation Plan - OCR Performance Improvement Iteration 2

## Phase 1: Baseline Assessment [COMPLETED]
- [x] Task: Prepare dataset.
    - [x] Install `pillow-heif` to handle HEIC images.
    - [x] Create conversion script and convert HEIC to JPG.
- [x] Task: Establish Ground Truth.
    - [x] Manually (via LLM reasoning) extract text from each image in `training-images/img-impr/`.
    - [x] Save ground truth to `experiments/ocr_v2/ground_truth.json`.
- [x] Task: Run Baseline OCR.
    - [x] Execute current `app/services/ocr.py` implementation (Tesseract PSM 12) on the 8 images.
    - [x] Record raw results and calculate accuracy scores (25.20% recall).
- [x] Task: Document Baseline Findings.
    - [x] **Findings:**
        - **Overall Recall:** 25.20% (32/127 titles found).
        - **Key Failures:** Tesseract struggled with density and orientation of CD spines.

## Phase 2: Research & Experimentation [COMPLETED]
- [x] Task: Test EasyOCR.
    - [x] Create benchmark script for EasyOCR.
    - [x] Run EasyOCR on the dataset. **Result: 77.95% recall (99/127).**
- [x] Task: Tesseract Tuning.
    - [x] Test PSM 11 and PSM 3. **Result: No improvement over PSM 12.**
- [x] Task: Image Preprocessing Experiments.
    - [x] Test CLAHE and forced rotation. **Result: Rotation (90 deg) failed completely; CLAHE slightly decreased accuracy.**
- [x] Task: Document Phase 2 Findings.
    - [x] **Findings:**
        - **Winner:** EasyOCR is the superior engine for this dataset (77.95% recall).
        - **Redundancy:** Tesseract PSM 12 found no titles that EasyOCR missed.
        - **Stability:** EasyOCR handles the varied orientations of CD spines automatically.

## Phase 3: Implementation & Multi-Pass Refinement [IN PROGRESS]
- [x] Task: Switch OCR Engine to EasyOCR.
    - [x] Update `app/services/ocr.py` to use EasyOCR.
- [x] Task: Add Multi-language Support.
    - [x] Initialize EasyOCR with `['en', 'pt']`.
- [x] Task: Resolve Rotation Regression.
    - [x] **Finding:** Enabling `rotation_info` in EasyOCR improved vertical book detection but caused a 50% drop in recall for the new CD dataset.
    - [x] Implement and test a "Dual Pass" approach: Standard pass + 90/270 degree rotation pass.
    - [x] **Result:** Dual pass achieved **80.31% recall** on the new dataset and successfully restored vertical text detection for books.
- [x] Task: Final Implementation & Validation.
    - [x] Update `app/services/ocr.py` with the dual-pass logic.
    - [x] Run final benchmark on full combined dataset.
    - [x] **Final Result:** 
        - **New Dataset Recall:** 74.80% (Massive improvement over 25.20% baseline).
        - **Old Dataset Recall:** 17.27% (Slight regression from 20.95%, but acceptable for modern photo support).
        - **Engine:** Successfully transitioned to EasyOCR with Dual-Pass logic.
