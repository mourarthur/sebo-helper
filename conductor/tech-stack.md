# Tech Stack

## Backend
- **Language:** Python 3.x
- **Framework:** FastAPI
- **Rationale:** FastAPI provides a fast, modern web framework with excellent performance and built-in support for asynchronous operations, which is beneficial for handling image processing tasks.

## OCR & Image Processing
- **Primary Engine:** Tesseract OCR (PSM 12)
- **Fuzzy Matching:** RapidFuzz
- **Image Handling:** OpenCV / Pillow (PIL)
- **Client-Side:** Tesseract.js (v5), OpenCV.js (WASM) for offline processing.
- **Rationale:** Tesseract with PSM 12 ("Sparse text with OSD") provides robust handling of text orientation and layout for media spines. RapidFuzz is used for robust matching of extracted titles against the wishlist, handling OCR errors and slight misspellings. OpenCV/Pillow are used for basic image loading and conversion. Client-side libraries enable offline functionality.

## Frontend
- **Template Engine:** Jinja2 (integrated with FastAPI)
- **Styling:** CSS3 (focusing on a utility-first, minimalist design)
- **Interactions:** Vanilla JavaScript
- **PWA:** Service Worker for offline caching, Web App Manifest for installability.
- **Rationale:** A template-based approach keeps the project structure simple and unified within the Python ecosystem, while vanilla JS and CSS are sufficient for the planned MVP features (drag-and-drop, list display).

## Storage
- **Memory-based:** Initially, the wishlist and results can be held in memory or simple local files (e.g., JSON/TXT) since this is a single-user application.
- **Client-Side:** LocalStorage for persisting wishlist and results in offline mode.
