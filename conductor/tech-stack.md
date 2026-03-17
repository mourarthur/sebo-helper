# Tech Stack
The PWA must remain fully functional after first load with no network access. All model files, language data, and WASM assets must be pre-cached by the service worker.

## Backend
- **Language:** Python 3.x
- **Framework:** FastAPI
- **Rationale:** FastAPI provides a fast, modern web framework with excellent performance and built-in support for asynchronous operations, which is beneficial for handling image processing tasks.

## OCR & Image Processing
- **Primary Engine (Backend/Local):** EasyOCR (Dual-Pass).
    - *Rationale:* Delivers superior accuracy (~75% recall) for CD/book spines compared to Tesseract (~25%). Handles complex layouts and fonts effectively.
- **Client-Side Engine (PWA):** Tesseract.js (v5) + OpenCV.js.
    - *Rationale:* Enables offline functionality directly in the browser. While less accurate than EasyOCR, a "Dual-Pass" strategy (Standard + 90° Rotated) is implemented to mitigate Tesseract's weakness with vertical text.
- **Image Handling:** OpenCV / Pillow (PIL).

## Frontend
- **Template Engine:** Jinja2 (integrated with FastAPI)
- **Styling:** CSS3 (focusing on a utility-first, minimalist design)
- **Interactions:** Vanilla JavaScript
- **PWA:** Service Worker for offline caching, Web App Manifest for installability.
- **Rationale:** A template-based approach keeps the project structure simple and unified within the Python ecosystem, while vanilla JS and CSS are sufficient for the planned MVP features (drag-and-drop, list display).

## Storage
- **Memory-based:** Initially, the wishlist and results can be held in memory or simple local files (e.g., JSON/TXT) since this is a single-user application.
- **Client-Side:** LocalStorage for persisting wishlist and results in offline mode.
