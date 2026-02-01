# Specification: Improve OCR Accuracy for Rotated Text

## Overview
This track aims to enhance the application's ability to extract text from media spines that are oriented vertically or at various angles. Currently, the OCR process may struggle with these orientations, leading to poor data extraction.

## Functional Requirements
- **Pre-processing Enhancement:** Implement or improve image pre-processing steps (e.g., rotation detection, image deskewing, or multiple-pass OCR with different rotations) to better handle vertical text.
- **Tesseract Configuration:** Explore and apply Tesseract configuration parameters that might optimize extraction for vertical text (e.g., Page Segmentation Modes).

## Non-Functional Requirements
- **Accuracy:** Significant improvement in text extraction accuracy for rotated text compared to the current baseline.
- **Maintainability:** Ensure the pre-processing logic is well-documented and modular.

## Acceptance Criteria
- OCR successfully extracts readable text from at least 80% of the vertical spines in the `sample-images` test set.
- The system correctly handles both horizontal and vertical text within the same image (or via sequential processing).
- Verification is performed manually by comparing OCR output against the actual text on the spines in the `sample-images` folder.

## Out of Scope
- Improving accuracy for extremely low-resolution images.
- Handwritten text recognition.
- Real-time video stream OCR.
