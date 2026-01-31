# Specification: Core MVP for Sebo Helper

## Goal
Implement a functional MVP that allows a user to upload a photo of media spines, extracts the text using Tesseract OCR, and displays the results in a simple list.

## Functional Requirements
- **Image Upload:** Endpoint to receive images (JPEG/PNG) from the frontend.
- **OCR Engine:** Integration with Tesseract OCR to extract text from images.
- **Image Pre-processing:** Basic pre-processing (using OpenCV/Pillow) to improve OCR accuracy for spines.
- **Results Storage:** Extracted text must be saved to a local file on the backend.
- **Web Interface:** A minimalist HTML page with:
    - Drag-and-drop image upload.
    - Display area for the list of extracted titles.
    - "Clear" button to delete saved results.

## Technical Details
- **Backend:** FastAPI (Python).
- **OCR:** Tesseract OCR (via `pytesseract`).
- **Frontend:** Jinja2 templates with Vanilla JS and CSS.
- **Persistence:** Local JSON or TXT file for storing extracted titles.
