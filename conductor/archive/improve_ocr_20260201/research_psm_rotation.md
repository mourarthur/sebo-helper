# Research: Tesseract PSM and Rotation Detection

## Tesseract Page Segmentation Modes (PSM)

Relevant modes for book spines:

- **`--psm 0` (Orientation and Script Detection - OSD):**
  - **Purpose:** Detects orientation (0, 90, 180, 270 degrees) and script.
  - **Pros:** Built-in, easy to use via `pytesseract.image_to_osd()`.
  - **Cons:** Requires a minimum amount of characters to work reliably. Short spine titles might fail.

- **`--psm 1` (Automatic page segmentation with OSD):**
  - **Purpose:** Full automation.
  - **Pros:** Handles mixed content.
  - **Cons:** Might be too aggressive or slow for simple spine crops.

- **`--psm 3` (Fully automatic page segmentation, no OSD):**
  - **Purpose:** Default mode.
  - **Pros:** Good baseline.
  - **Cons:** Assumes horizontal text.

- **`--psm 5` (Single uniform block of vertically aligned text):**
  - **Purpose:** Explicitly for vertical text.
  - **Pros:** Potential silver bullet for vertical spines (Japanese-style or stacked characters).
  - **Cons:** Fails on rotated horizontal text (text that reads top-to-bottom but characters are rotated 90 degrees).

- **`--psm 6` (Single uniform block of text):**
  - **Purpose:** Good for a block of text.
  - **Pros:** Less assumption about page structure than default.

- **`--psm 7` (Treat the image as a single text line):**
  - **Purpose:** Very specific.
  - **Pros:** excellent for isolated title lines.

## Rotation Detection Strategies

### 1. Tesseract OSD (Primary)
Use `pytesseract.image_to_osd(image)` to get the `Rotate` angle.
- **Logic:** If `Rotate: 90`, rotate image -90 degrees before OCR.
- **Risk:** Fails on short text or noisy images.

### 2. OpenCV Contour Analysis (Secondary/Deskewing)
- **Technique:** Find contours -> `cv2.minAreaRect` -> Get angle.
- **Logic:** Text lines usually form rectangular blocks. The angle of the bounding box indicates skew.
- **Application:** Good for small skew angles (e.g., < 10 degrees) caused by hand jitter.

### 3. Multi-Pass Brute Force (Robust Fallback)
If OSD confidence is low, run OCR on multiple versions of the image:
1.  Original (0°)
2.  Rotated 90° CW
3.  Rotated 90° CCW
4.  **Compare:** Check `confidence` score of the OCR result. Pick the highest.
5.  **Refinement:** Check for dictionary words (optional, requires dictionary).

## Selected Strategy for Implementation
1.  **Step 1:** Preprocess (Grayscale, Threshold).
2.  **Step 2:** Attempt **OSD**. If high confidence, rotate.
3.  **Step 3:** If OSD fails/low confidence, use **Multi-Pass Brute Force** (0°, 90°, -90°).
4.  **Step 4:** Within each pass, try both `--psm 6` (block) and `--psm 7` (line) if results are poor.
5.  **Step 5:** Investigate `--psm 5` specifically for cases where text characters are stacked vertically (if applicable).
