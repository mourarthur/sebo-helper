# Sebo Helper

> **Note:** This is a "vibecoded" project. It was developed experimentally with an AI assistant to explore rapid prototyping and offline-first PWA capabilities. It is provided "as-is" for educational purposes.

**Sebo Helper** is a Progressive Web App (PWA) designed to help collectors find items from their wishlist in used media stores ("sebos"). It runs completely offline on your mobile device.

## Features
- **Offline First:** Works without an internet connection once installed.
- **Client-Side OCR:** Uses Tesseract.js and OpenCV.js to scan book/CD/DVD spines directly in the browser.
- **Wishlist Matching:** Instantly highlights titles that match your wishlist.
- **Privacy Focused:** All processing happens on your device. No images are uploaded to any server.

## Usage
1.  Go to the [Live Demo](https://mourarthur.github.io/sebo-helper/).
2.  Wait for the status to say **"Ready"**.
3.  **Install the App:**
    *   **iOS:** Tap the "Share" button -> "Add to Home Screen".
    *   **Android:** Tap the menu (three dots) -> "Install App" or "Add to Home Screen".
4.  Open the app from your home screen.
5.  Paste your wishlist items (one per line).
6.  Start scanning!

## Development
This project uses:
- Python (FastAPI) for the local dev environment.
- Tesseract.js & OpenCV.js for client-side processing.
- Vanilla JS/CSS for the frontend.

To run locally:
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```
