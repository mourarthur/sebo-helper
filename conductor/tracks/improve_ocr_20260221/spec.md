# Specification: Improve OCR Performance

## Overview
This track focuses on significantly improving the Optical Character Recognition (OCR) accuracy, with a particular emphasis on handling the vertical and rotated text commonly found on media spines. The goal is to surpass the current Tesseract-based baseline by exploring advanced Tesseract tuning and evaluating alternative OCR engines.

## Functional Requirements
1.  **Benchmarking & Evaluation Framework:**
    -   Develop a Python script to iterate through the `sample-images/` directory.
    -   Implement a scoring mechanism (e.g., Levenshtein distance, fuzzy matching) to compare OCR output against the ground truth text files (e.g., `OCR2.txt`).
    -   Generate a report summarizing accuracy metrics for different configurations.
2.  **Tesseract Optimization:**
    -   Systematically test different Page Segmentation Modes (PSM) (specifically 6, 11, 12, etc.) and Engine Modes (OEM).
    -   Implement image preprocessing steps (rotation correction, contrast enhancement) if beneficial.
3.  **Alternative Engine Evaluation:**
    -   Evaluate at least one alternative OCR library (e.g., EasyOCR, PaddleOCR) known for better handling of diverse text orientations.
    -   Compare its performance (accuracy vs. speed) against the best Tesseract configuration.
4.  **Integration Candidate:**
    -   Identify the best-performing solution (Engine + Configuration).
    -   Update the main application's OCR service to use this improved solution.

## Non-Functional Requirements
-   **Accuracy Priority:** Accuracy is the primary metric; speed is secondary but must remain usable (e.g., < 5-10 seconds per image).
-   **Dependencies:** Any new libraries must be compatible with the existing Python environment and added to `requirements.txt`.

## Acceptance Criteria
-   [ ] A benchmarking script exists that automatically evaluates OCR performance against `sample-images/`.
-   [ ] A "winner" configuration is identified that shows a measurable improvement in text extraction accuracy compared to the current baseline.
-   [ ] The application backend is updated to use the improved OCR logic.
-   [ ] `requirements.txt` is updated if new libraries are introduced.

## Out of Scope
-   Real-time video stream processing.
-   Training a custom OCR model from scratch (we will use pre-trained models).