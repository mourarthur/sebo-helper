# Initial Concept
The user wants an application that can receive a photo of a stack of used media (books, CDs, DVDs) and extract the titles (e.g., band and album names) from the spines. This extracted data will then be compared against the user's wishlist to quickly identify items of interest.

## Target Audience
- Used media collectors and hobbyists who frequently visit physical stores.
- Librarians or archivists managing physical collections.
- Note: The primary user is currently the developer themselves, so multi-user functionality is not an immediate priority.

## Goals
- Minimize the time spent manually scanning shelves and spines in physical stores.
- Ensure high accuracy in text extraction from varied fonts and orientations on media spines.

## Core Features (MVP)
- **Mobile-friendly Capture:** Interface for capturing or uploading photos while browsing.
- **Spine-Optimized OCR:** Text extraction specifically tuned for the unique challenges of media spines (vertical text, stylized fonts).
- **Wishlist Management:** A dedicated interface to paste, save, and persist a list of desired items (titles).
- **Title Extraction List:** A plaintext list display of all titles extracted from the photo.
- **Offline PWA Mode:** Fully functional offline mode using client-side OCR (Tesseract.js/OpenCV.js) for use in locations without internet access.

## Wishlist Integration
- Simple manual entry system where the user can paste their wishlist directly into the application.