# Implementation Plan: Improve OCR Accuracy for Rotated Text

## Phase 1: Research and Baseline [checkpoint: db7dbdf]
- [x] Task: Research Tesseract PSM (Page Segmentation Modes) and rotation detection strategies.
- [x] Task: Establish a baseline accuracy metric by running current OCR on `sample-images`.
- [x] Task: Conductor - User Manual Verification 'Phase 1: Research and Baseline' (Protocol in workflow.md)

## Phase 2: Pre-processing & OCR Enhancements [checkpoint: ]
- [x] Task: Implement image rotation detection (e.g., using OpenCV's `minAreaRect` or Hough Transform). 3d1ff43
- [ ] Task: Implement image deskewing and pre-rotation logic in `app/services/ocr.py`.
    - [ ] Write Tests: Create `tests/test_ocr_rotated.py` with failing tests for rotated images.
    - [ ] Implement: Update `ocr.py` to handle rotated text.
- [ ] Task: Experiment with and integrate optimal Tesseract PSM settings for vertical/rotated text.
    - [ ] Write Tests: Update `tests/test_ocr_rotated.py` to assert better accuracy.
    - [ ] Implement: Apply PSM settings in `ocr.py`.
- [ ] Task: Implement a multi-pass OCR strategy if single-pass rotation detection is insufficient.
    - [ ] Write Tests: Add test cases for complex images needing multi-pass.
    - [ ] Implement: Update `ocr.py` logic.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Pre-processing & OCR Enhancements' (Protocol in workflow.md)

## Phase 3: Verification and Refinement [checkpoint: ]
- [ ] Task: Run improved OCR on the full `sample-images` set and document results.
- [ ] Task: Refactor OCR service for performance and clarity.
    - [ ] Write Tests: Ensure no regressions in existing tests.
    - [ ] Implement: Refactor `app/services/ocr.py`.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Verification and Refinement' (Protocol in workflow.md)
