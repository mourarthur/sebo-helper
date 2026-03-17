# OCR Improvement Plan

## 1. Spec Review

The core goal — **phone, in the street, no internet** — is implemented correctly as a PWA with a service worker and a Cache-First strategy. However, the specs have two gaps worth addressing:

**What's clear:**
- `conductor/product.md` defines "Offline PWA Mode" as a core feature.
- `conductor/tech-stack.md` correctly documents the accuracy trade-off: ~75% recall (EasyOCR/backend) vs ~25% recall (Tesseract.js/PWA).

**What's missing or inconsistent:**
- The product goal says "ensure high accuracy" but no PWA-specific accuracy target is defined. The 25% recall in the offline path directly contradicts "high accuracy," and no spec acknowledges this openly as an accepted trade-off.
- The `product.md` possible improvements section is about build tooling, not OCR quality — the roadmap doesn't reflect what is actually the biggest open problem.

**Recommended spec additions** (not urgent, but clarifying):
- Add a PWA-specific accuracy target to `product.md`, or explicitly document the gap as an accepted trade-off until a better browser OCR engine is integrated.

---

## 2. Implementation Review

The implementation is sound and sensible. A few observations:

**Works well:**
- Dual-pass (0° + 90°) strategy correctly mirrors the backend approach and handles both horizontal CDs and vertical book spines.
- Service worker correctly uses Cache-First, and the recent automated asset manifest prevents the "missing file offline" bug.
- Tesseract.js singleton worker is reused across recognitions — no unnecessary WASM reload.
- PSM 12 was validated experimentally to be the best mode for the sample-images dataset.

**Current limitations:**
- The preprocessing pipeline is just grayscale conversion. No contrast normalization, no binarization, no noise removal. This is almost certainly the largest contributor to the accuracy gap vs EasyOCR.
- The image is scaled to max 2000px for display, but this display-scaled canvas is then passed directly to OCR. If the original photo is much larger, downscaling reduces text resolution below what Tesseract's LSTM handles well. The scaling should be evaluated separately for display vs OCR.
- Only English language data is loaded (`'eng'`). Many items in the sample images are in Brazilian Portuguese. The `por` (Portuguese) Tesseract model would cover accents, ç, ã, ã, é, etc. that currently get mangled or dropped.
- The 90° rotation is hardcoded clockwise. Spines can also be rotated counter-clockwise. A third pass at 270° would be a trivial addition.

---

## 3. Improvement Opportunities

Ordered by **expected recall improvement × implementation effort**.

---

### Priority 1 — Better Image Preprocessing (High Impact, Low Effort)

**Current state:** `preprocessImage()` in `image-processor.js` only converts to grayscale.

**Problem:** CD spine photos have uneven lighting (fluorescent store lights, shadows from the hand holding the phone), compressed contrast, and slight blur. Tesseract's LSTM performs much better on clean, high-contrast binary images.

**Proposed pipeline** (all available in the bundled OpenCV.js):

1. **Grayscale** — already done.
2. **CLAHE** (Contrast Limited Adaptive Histogram Equalization) — corrects uneven lighting per tile. Parameters: `clipLimit=2.0`, `tileGridSize=(8,8)`. Note: OpenCV.js includes `cv.CLAHE` — tested in this context, it was found to slightly decrease accuracy in the old sample-images dataset, but those were scanned/clean images. For real phone photos (the `img-impr` dataset), CLAHE is expected to help. Worth benchmarking with the new dataset specifically.
3. **Gaussian blur** `(3,3)` — noise suppression before thresholding.
4. **Adaptive Gaussian thresholding** — `blockSize=11, C=2`. Handles the local contrast variation across a shelf photo far better than Otsu's global threshold. Produces clean binary output for Tesseract.
5. **Morphological close** `(2,2)` — repairs broken character strokes from spine creases or reflections.

Expected impact: **+15–30% recall on the img-impr dataset** (based on research benchmarks for similar real-world photo OCR scenarios).

The pipeline change is entirely in `image-processor.js` and does not affect any other component.

---

### Priority 2 — Add Portuguese Language Data

**Current state:** Tesseract is initialized with `'eng'` only.

**Problem:** Most items in the `img-impr` images are Brazilian Portuguese titles (Agatha Christie translations, sertanejo albums, etc.). Characters like `ã`, `ç`, `é`, `ô` are either dropped or garbled by an English-only model.

**Solution:** Initialize the worker with `['eng', 'por']`:

```javascript
ocrWorker = await Tesseract.createWorker(['eng', 'por'], 1, { ... });
```

**Trade-off:** The `por.traineddata.gz` file is ~10 MB. It must be added to the service worker cache and to the `docs/static/js/vendor/lang-data/` directory. This increases first-load size.

**Expected impact:** Better recall for titles with Portuguese-specific characters. Also likely reduces false positives (garbled guesses) on Portuguese words.

---

### Priority 3 — Add Counter-Clockwise Rotation Pass

**Current state:** Dual-pass = 0° + 90° clockwise.

**Problem:** Spine labels on shelves are commonly printed both ways. The current code rotates clockwise only, missing spines that are rotated the other way.

**Solution:** Add a third pass with `cv.ROTATE_90_COUNTERCLOCKWISE`. This triples OCR processing time, but all three passes run sequentially and the result is deduplicated via `Set`.

If three passes is too slow, benchmark which rotation direction dominates in the `img-impr` images and keep only the two most useful.

---

### Priority 4 — Evaluate PSM 11 on the New Dataset

**Current state:** PSM 12 (`SPARSE_TEXT_OSD`) was experimentally validated as the best mode for `sample-images/`.

**Problem:** PSM 12 includes an orientation detection step (OSD) that adds latency and can misfire on low-resolution or sparse text, causing incorrect rotations and accuracy regressions. The `sample-images` dataset (scanned images) and `img-impr` dataset (real phone photos) are different enough that a separate evaluation is warranted.

**Suggestion:** Re-run the benchmark on `img-impr` with PSM 11 (`SPARSE_TEXT`, no OSD) and compare. If PSM 11 matches or exceeds PSM 12 on phone photos, switch and drop the OSD overhead.

---

### Priority 5 — Replace Tesseract.js with TrOCR via Transformers.js (High Impact, Higher Effort)

This is the path most likely to close the gap to EasyOCR-level recall in the browser.

**Library:** `@huggingface/transformers` (Transformers.js, formerly `@xenova/transformers`)
**Model:** `Xenova/trocr-small-printed`
**Size:** ~80–100 MB at `q8` quantization (one-time download, then cached offline)

**Why TrOCR:**
- TrOCR is a transformer encoder-decoder specifically trained on cropped word/line images from real-world documents.
- Handles stylized fonts, varied contrast, and partial occlusion much better than Tesseract's LSTM.
- In benchmarks on comparable tasks, TrOCR small-printed with q8 quantization approaches EasyOCR accuracy on real-world printed text.

**How it fits the offline constraint:**
```javascript
import { env } from '@huggingface/transformers';
env.localModelPath = '/models/';     // served from the PWA
env.allowRemoteModels = false;        // pure offline after first load
env.backends.onnx.wasm.wasmPaths = '/wasm/'; // bundled WASM files
```

The model files are fetched once and cached by the service worker, identical to how Tesseract's WASM and language data work today.

**Integration approach:**
1. TrOCR is a line-level model — it expects a cropped single line of text, not a full shelf photo.
2. A text region detection step is needed before feeding images to TrOCR. Options:
   - **Simple horizontal/vertical strip segmentation** using OpenCV connected-components or contour detection — fast, no extra model.
   - **EAST text detector** (OpenCV DNN, model ~90 MB) — accurate but adds another large cached file.
   - **Keep Tesseract for region detection only** (using `hocr` output for bounding boxes), feed crops to TrOCR for recognition.
3. The strips/crops are rotated and fed to TrOCR individually.

**Trade-offs:**
- Adds ~80–100 MB to the service worker cache (vs current ~15 MB for Tesseract).
- Inference latency per image: ~2–5 seconds on mid-range Android via WASM; faster with WebGPU (iOS Safari 17.4+, Chrome Android).
- Significant refactor to `ocr-engine.js` and `pwa.js`.
- The Transformers.js WASM backend is universal but slower than WebGPU; worth feature-detecting `navigator.gpu` and using WebGPU where available.

**Recommended approach:** Prototype this in a separate branch, benchmark against `img-impr` before committing.

---

### Priority 6 — Deskewing

Phone photos of shelves are often taken at a slight angle. Even a 2–5° tilt meaningfully degrades Tesseract's LSTM recognition.

**Solution:** After grayscale conversion, apply a Hough Lines-based skew detection and rotate to align the dominant text direction. OpenCV.js includes `cv.HoughLines` and `cv.getRotationMatrix2D`.

**Caveat:** Unreliable on very sparse images (few detectable lines). Should be applied only when skew confidence is high, or only when the detected angle is above a threshold (e.g., > 2°). OSD-based rotation was tested and found to regress accuracy — a pure OpenCV approach is preferred.

---

## Summary Table

| Priority | Change | Effort | Expected Impact | Constraint |
|----------|--------|--------|-----------------|------------|
| 1 | Better preprocessing (CLAHE + adaptive threshold + morphology) | Low | +15–30% recall | None |
| 2 | Add Portuguese language data (`por`) | Low | +5–15% recall on PT text | +10 MB cache |
| 3 | Add 270° rotation pass | Trivial | +5% recall | +50% OCR time |
| 4 | Evaluate PSM 11 vs PSM 12 on img-impr | Low (benchmark only) | Neutral to +5% | None |
| 5 | Replace Tesseract.js with TrOCR (Transformers.js) | High | +30–50% recall | +80–100 MB cache |
| 6 | Deskewing via Hough Lines | Medium | +5–10% on angled photos | Risk of regression |

**Recommended starting point:** Priority 1 + 2 + 3 together, since they are low-effort and additive. Then benchmark against `img-impr` before committing to the TrOCR path.

---

## Questions answered

1. **Cache size budget:** An ~80–100 MB one-time download is acceptable for the TrOCR path (Priority 5). This would make the initial app load much heavier, but subsequent uses are fully offline. Currently the app is ~15–20 MB cached. In general, I prefer lightweight sollutions, but I'm willing to trade memory for performance (up to a sensible point).

2. **Processing time budget:** The dual-pass OCR already takes a few seconds per image. Adding a third rotation pass and/or TrOCR inference would increase this, but I am not yet worried about it. An acceptable upper bound is 10 seconds of processing time per image.
