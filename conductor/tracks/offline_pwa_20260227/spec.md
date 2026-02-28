# Track: Offline PWA with Client-Side OCR

## Overview
This track focuses on transforming the existing `sebo-helper` web application into a fully offline-capable Progressive Web App (PWA). The core OCR logic, currently running on a Python backend, will be ported to the client-side using `Tesseract.js` and `OpenCV.js`. This allows the application to function entirely on a mobile device without an active internet connection, storing data locally.

## Goals
-   **Offline Capability:** The app must load and function without a network connection.
-   **Client-Side Processing:** Port image preprocessing (rotation, thresholding) and OCR extraction to the browser.
-   **Mobile UX:** Ensure the application is installable (Add to Home Screen) and camera-accessible.
-   **Data Persistence:** Persist wishlist and scan results on the device.

## Functional Requirements

### 1. PWA Foundation
-   **Manifest:** Create `manifest.json` with app name ("Sebo Helper"), icons, and display mode (`standalone`).
-   **Service Worker:** Implement a Service Worker to cache:
    -   HTML, CSS, JS application files.
    -   WASM binaries for `Tesseract.js` and `OpenCV.js`.
    -   Language data for Tesseract (eng.traineddata).

### 2. Client-Side OCR Pipeline
-   **Library Integration:**
    -   Integrate `Tesseract.js` (v5+) for OCR.
    -   Integrate `OpenCV.js` (WASM) for image preprocessing.
-   **Preprocessing Logic:**
    -   Replicate the Python backend's preprocessing steps in JavaScript using OpenCV.js:
        -   Grayscale conversion.
        -   Thresholding/Binarization.
        -   Orientation detection/correction (if feasible with Tesseract OSD or OpenCV).
-   **Text Extraction:**
    -   Configure Tesseract.js with PSM 12 (Sparse Text) equivalent settings.
    -   Extract text from the processed image canvas.

### 3. Data Management
-   **Wishlist:** Allow users to paste/edit their wishlist, stored in `localStorage` or `IndexedDB`.
-   **Results:** Store extracted text results locally.
-   **Matching:** Port the fuzzy matching logic (RapidFuzz equivalent) to JavaScript (e.g., `fuzzball.js` or similar lightweight library).

### 4. User Interface
-   **Camera Access:** Ensure the file input triggers the native camera on mobile devices.
-   **Progress Feedback:** Show detailed progress bars for:
    -   Loading WASM binaries (initial load).
    -   Image Preprocessing.
    -   OCR Extraction.
-   **Offline Indicator:** (Optional) Visually indicate when the app is offline.

## Non-Functional Requirements
-   **Performance:** Initial load of WASM binaries should be optimized (cached after first visit).
-   **Accuracy:** Strive for OCR accuracy parity with the Python backend.
-   **Browser Support:** Modern mobile browsers (iOS Safari, Android Chrome).

## Out of Scope
-   **Backend Sync:** No synchronization of data back to the Python server.
-   **Server-Side OCR:** The Python OCR endpoints will not be used in this mode.
