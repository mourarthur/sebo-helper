# Intro
This project, sebo-helper, is a FastAPI-powered web application designed to help media collectors (books, CDs, DVDs) identify items from their wishlist by scanning physical spines using OCR.

# Project Overview
The application allows users to upload photos of media shelves. It then uses Tesseract (specifically tuned with PSM 12 for sparse text and orientation detection) and EasyOCR to extract titles from the spines. These titles are then matched against a user-managed wishlist.

# Tech Stack
- Backend: Python 3.x, FastAPI, Uvicorn.
- OCR: Tesseract OCR (Primary, PSM 12), EasyOCR.
- Image Processing: OpenCV, Pillow (PIL).
- Frontend: Jinja2 Templates, Vanilla JavaScript, CSS3.
- Storage: Local JSON files (wishlist.json, results.json) for persistence.

# Building and Running

## Setup

1. Install Tesseract OCR: Ensure Tesseract is installed on your system.
2. Virtual Environment:
        python -m venv venv
        source venv/bin/activate  # On Linux/macOS
3. Dependencies:
        pip install -r requirements.txt


## Running the Application
        uvicorn app.main:app --reload
  
The server will start at http://127.0.0.1:8000.

# Testing
        pytest
        # For coverage:
        pytest --cov=app --cov-report=term-missing


# Development Conventions
The project follows a strict workflow managed by the conductor/ extension:
- Source of Truth: All tasks are tracked in conductor/tracks/<track_id>/plan.md.
- TDD: Write failing tests before implementing functionality.
- Code Style: Guidelines are located in conductor/code_styleguides/.
- Commit Messages: Use conventional commits (e.g., feat(ocr): ..., fix(ui): ...).
- Git Notes: Task summaries are attached to commits via git notes.
- MCP: Use the context7 MCP server to get appropriate documentation regarding the tech stack


# Directory Structure
- app/: Main application code (FastAPI routes, services).
- conductor/: Project management, guidelines, and track-specific plans.
- experiments/: Benchmarks and OCR improvement research.
- sample-images/: Data for testing OCR accuracy.
- tests/: Unit and integration tests.
- uploads/: Temporary storage for uploaded images.

