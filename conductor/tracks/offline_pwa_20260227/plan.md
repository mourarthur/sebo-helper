# Implementation Plan - Offline PWA with Client-Side OCR

## Phase 1: Project Setup & Dependencies [checkpoint: 3f8c645]
- [x] Task: Initialize track structure and assets.
    - [x] Create `static/js/vendor` directory.
    - [x] Download/Copy `tesseract.min.js` (v5) and `worker.min.js` to vendor dir.
    - [x] Download/Copy `opencv.js` to vendor dir.
    - [x] Add `manifest.json` with app metadata and icons.
    - [x] Create `static/icons` directory and add placeholder icons (192x192, 512x512).
- [x] Task: Basic Service Worker Implementation.
    - [x] Create `service-worker.js` in root (or static, served from root).
    - [x] Implement strict caching for vendor JS and core CSS/HTML.
    - [x] Register Service Worker in `base.html` or new `pwa.html`.
- [x] Task: Create PWA Entry Point.
    - [x] Create `templates/pwa.html` (lightweight, mobile-focused structure).
    - [x] Add route `/pwa` in `main.py` to serve this template.
- [x] Task: Conductor - User Manual Verification 'Project Setup & Dependencies' (Protocol in workflow.md)

## Phase 2: Client-Side Infrastructure [checkpoint: 6ab0011]
- [x] Task: Integrate Tesseract.js.
    - [x] Create `static/js/ocr-engine.js`.
    - [x] Implement Tesseract initialization and worker creation.
    - [x] Test loading language data (eng.traineddata) from cache.
- [x] Task: Integrate OpenCV.js.
    - [x] Create `static/js/image-processor.js`.
    - [x] Implement `onRuntimeInitialized` check.
    - [x] Create helper function to read image from `<input>` to `cv.Mat`.
- [x] Task: UI for File/Camera Input.
    - [x] Add `<input type="file" accept="image/*" capture="environment">` to `pwa.html`.
    - [x] Display selected image on a `<canvas>` element.
- [x] Task: Conductor - User Manual Verification 'Client-Side Infrastructure' (Protocol in workflow.md)

## Phase 3: Core OCR Migration [checkpoint: e2589d9]
- [x] Task: Port Image Preprocessing.
    - [x] Implement `preprocessImage(canvas)` in `image-processor.js`.
    - [x] Port Grayscale logic (`cv.cvtColor`).
    - [x] Port Thresholding logic (placeholder added).
    - [ ] (Optional) Port skew correction if feasible in JS.
- [x] Task: Implement OCR Execution.
    - [x] Connect preprocessed canvas to Tesseract.js `recognize`.
    - [x] Configure Tesseract parameters (PSM 12 equivalent).
    - [x] Display raw text output in UI.
- [x] Task: Add Progress Feedback.
    - [x] Implement progress bar using Tesseract.js logger callback.
    - [x] Show "Preprocessing..." state.
- [x] Task: Conductor - User Manual Verification 'Core OCR Migration' (Protocol in workflow.md)

## Phase 4: Data & Matching [checkpoint: 0713fe8]
- [x] Task: Local Storage Management.
    - [x] Create `static/js/storage.js`.
    - [x] Implement `saveWishlist(text)` and `getWishlist()`.
    - [x] Implement `saveResult(scanData)` and `getResults()`.
- [x] Task: Client-Side Matching.
    - [x] Import `fuzzball` or implementing basic Levenshtein in `static/js/matching.js`.
    - [x] Implement matching logic: Compare extracted lines vs wishlist items.
    - [x] Highlight matches in the UI.
- [x] Task: Conductor - User Manual Verification 'Data & Matching' (Protocol in workflow.md)

## Phase 5: Refinement & Polish
- [x] Task: UI Styling for Mobile.
    - [x] Ensure touch targets are 44px+.
    - [x] Add "Install App" prompt logic.
    - [x] Verify "Offline" indicator visibility.
- [x] Task: Performance Tuning.
    - [x] Verify WASM caching (Network tab).
    - [x] Optimize image resize before processing (limit max dimension to 2000px).
- [ ] Task: Conductor - User Manual Verification 'Refinement & Polish' (Protocol in workflow.md)
