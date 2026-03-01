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

## Phase 3: Core OCR Migration
- [ ] Task: Port Image Preprocessing.
    - [ ] Implement `preprocessImage(canvas)` in `image-processor.js`.
    - [ ] Port Grayscale logic (`cv.cvtColor`).
    - [ ] Port Thresholding logic (`cv.threshold` or adaptive).
    - [ ] (Optional) Port skew correction if feasible in JS.
- [ ] Task: Implement OCR Execution.
    - [ ] Connect preprocessed canvas to Tesseract.js `recognize`.
    - [ ] Configure Tesseract parameters (PSM 12 equivalent).
    - [ ] Display raw text output in UI.
- [ ] Task: Add Progress Feedback.
    - [ ] Implement progress bar using Tesseract.js logger callback.
    - [ ] Show "Preprocessing..." state.
- [ ] Task: Conductor - User Manual Verification 'Core OCR Migration' (Protocol in workflow.md)

## Phase 4: Data & Matching
- [ ] Task: Local Storage Management.
    - [ ] Create `static/js/storage.js`.
    - [ ] Implement `saveWishlist(text)` and `getWishlist()`.
    - [ ] Implement `saveResult(scanData)` and `getResults()`.
- [ ] Task: Client-Side Matching.
    - [ ] Import `fuzzball` or implementing basic Levenshtein in `static/js/matching.js`.
    - [ ] Implement matching logic: Compare extracted lines vs wishlist items.
    - [ ] Highlight matches in the UI.
- [ ] Task: Conductor - User Manual Verification 'Data & Matching' (Protocol in workflow.md)

## Phase 5: Refinement & Polish
- [ ] Task: UI Styling for Mobile.
    - [ ] Ensure touch targets are 44px+.
    - [ ] Add "Install App" prompt logic.
    - [ ] Verify "Offline" indicator visibility.
- [ ] Task: Performance Tuning.
    - [ ] Verify WASM caching (Network tab).
    - [ ] Optimize image resize before processing (limit max dimension to 2000px).
- [ ] Task: Conductor - User Manual Verification 'Refinement & Polish' (Protocol in workflow.md)
