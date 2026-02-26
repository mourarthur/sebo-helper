# Implementation Plan: Wishlist Management and Match Highlighting

## Phase 1: Wishlist Persistence & API [checkpoint: b726a02]
- [x] Task: Create `app/services/wishlist.py` to handle wishlist persistence (save, get, clear).
- [x] Task: Add unit tests for `app/services/wishlist.py` in `tests/test_wishlist.py`.
- [x] Task: Add FastAPI endpoints to `app/main.py` for `/wishlist` (GET, POST).
- [x] Task: Conductor - User Manual Verification 'Phase 1: Wishlist Persistence & API' b726a02

## Phase 2: Wishlist UI
- [x] Task: Add a new CSS class for highlighted matches in `app/static/css/style.css`. 622d207
- [x] Task: Update `app/templates/index.html` to include a wishlist management section (text area and save button). 0eb67a1
- [ ] Task: Add JavaScript logic in `app/templates/index.html` to fetch and save the wishlist.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Wishlist UI'

## Phase 3: Match Highlighting Logic
- [ ] Task: Create `app/services/matching.py` with a robust matching function (e.g., case-insensitive, fuzzy).
- [ ] Task: Add unit tests for `app/services/matching.py` in `tests/test_matching.py`.
- [ ] Task: Update `app/main.py`'s `/upload` endpoint to return match information with each title.
- [ ] Task: Update `app/templates/index.html`'s `updateResultsList` function to apply highlighting based on match information.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Match Highlighting Logic'

## Phase 4: Final Refinement & Verification
- [ ] Task: Optimize fuzzy matching (e.g., using RapidFuzz or similar if needed).
- [ ] Task: Ensure responsive design for both wishlist and results lists.
- [ ] Task: Final end-to-end verification.
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Final Refinement & Verification'
