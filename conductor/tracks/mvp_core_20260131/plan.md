# Implementation Plan: Core MVP

## Phase 1: Project Scaffolding & Environment [checkpoint: b8371db]
- [x] Task: Set up Python environment and install dependencies (FastAPI, uvicorn, pytesseract, Pillow, opencv-python, jinja2, python-multipart). 8a0d9d9
- [x] Task: Create basic FastAPI application structure with a single "Hello World" route. 843158a
- [x] Task: Conductor - User Manual Verification 'Phase 1: Scaffolding' (Protocol in workflow.md)

## Phase 2: Backend Development (OCR & Processing) [checkpoint: a3c61b9]
- [x] Task: Implement image upload endpoint in FastAPI. 6349799
- [x] Task: Integrate Tesseract OCR. 44f065d
- [x] Task: Implement persistence for extracted text. adcadb3
- [x] Task: Conductor - User Manual Verification 'Phase 2: Backend' (Protocol in workflow.md)

## Phase 3: Frontend Development (UI & Integration)
- [x] Task: Create Jinja2 base template and minimalist CSS. 9ec1f48
- [ ] Task: Implement the main upload page.
    - [ ] Create HTML form and drag-and-drop area.
    - [ ] Implement Vanilla JS to handle file upload and display results from the backend.
- [ ] Task: Implement the "Results List" and "Clear" functionality.
    - [ ] Create UI for listing titles.
    - [ ] Connect "Clear" button to backend endpoint.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Frontend' (Protocol in workflow.md)

## Phase 4: Final Integration & Review
- [ ] Task: End-to-end testing of the upload -> OCR -> Display flow.
- [ ] Task: Final code cleanup and documentation update.
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Integration' (Protocol in workflow.md)
