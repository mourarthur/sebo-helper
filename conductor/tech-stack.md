# Tech Stack

## Backend
- **Language:** Python 3.x
- **Framework:** FastAPI
- **Rationale:** FastAPI provides a fast, modern web framework with excellent performance and built-in support for asynchronous operations, which is beneficial for handling image processing tasks.

## OCR & Image Processing
- **Primary Engine:** Tesseract OCR
- **Image Handling:** OpenCV / Pillow (PIL)
- **Rationale:** Tesseract is a robust, open-source OCR engine. Combined with OpenCV or Pillow, it allows for the necessary image pre-processing (grayscale, thresholding, rotation) to improve extraction accuracy from media spines.

## Frontend
- **Template Engine:** Jinja2 (integrated with FastAPI)
- **Styling:** CSS3 (focusing on a utility-first, minimalist design)
- **Interactions:** Vanilla JavaScript
- **Rationale:** A template-based approach keeps the project structure simple and unified within the Python ecosystem, while vanilla JS and CSS are sufficient for the planned MVP features (drag-and-drop, list display).

## Storage
- **Memory-based:** Initially, the wishlist and results can be held in memory or simple local files (e.g., JSON/TXT) since this is a single-user application.
