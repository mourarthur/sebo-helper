# Implementation Plan: Improve OCR Performance

## Phase 1: Setup & Benchmarking
- [ ] Task: Create a dedicated directory for the OCR experiments (e.g., `experiments/ocr_improvement`).
- [ ] Task: Create a Python script `benchmark.py` that iterates through `sample-images/`, runs the current OCR implementation, and compares the output with the ground truth `.txt` files.
- [ ] Task: Implement a scoring function (e.g., Levenshtein distance) to quantify accuracy.
- [ ] Task: Run the benchmark to establish the baseline accuracy and performance metrics. Record these in a `results/baseline.md` file.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Setup & Benchmarking' (Protocol in workflow.md)

## Phase 2: Tesseract Optimization
- [ ] Task: Modify `benchmark.py` to accept different Tesseract configurations (PSM, OEM) and preprocessing flags.
- [ ] Task: Run experiments with different PSM modes (specifically 6, 11, 12 for blocks/sparse text) and document the results.
- [ ] Task: Implement and test basic image preprocessing (e.g., rotation/deskewing using OpenCV) before passing to Tesseract.
- [ ] Task: Measure if preprocessing improves accuracy on the rotated/vertical text samples.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Tesseract Optimization' (Protocol in workflow.md)

## Phase 3: Alternative Engine Evaluation
- [ ] Task: Research and select a promising alternative OCR library (e.g., EasyOCR or PaddleOCR) compatible with the current Python environment.
- [ ] Task: Install the chosen library and add it to `requirements.txt`.
- [ ] Task: Create a wrapper in `benchmark.py` to use the new engine.
- [ ] Task: Run the benchmark using the new engine and compare results (accuracy and speed) against the best Tesseract configuration.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Alternative Engine Evaluation' (Protocol in workflow.md)

## Phase 4: Integration & Wrap-up
- [ ] Task: Select the best performing OCR solution (Engine + Config) based on the data.
- [ ] Task: Refactor the main application's OCR service (`app/services/ocr.py`) to use the winning solution.
- [ ] Task: Verify the end-to-end application flow with the new OCR logic.
- [ ] Task: Update project documentation (Tech Stack if changed) and clean up experimental scripts if necessary.
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Integration & Wrap-up' (Protocol in workflow.md)