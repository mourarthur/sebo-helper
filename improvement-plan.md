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

> **⚠️ BENCHMARKED — DO NOT IMPLEMENT AS WRITTEN.**
> Benchmarked on the `img-impr` dataset (2026-03-17). Results across 8 images:
>
> | Pipeline | PSM 11 | PSM 12 |
> |---|---|---|
> | grayscale only (current) | 34.2% | 41.5% |
> | CLAHE only | 30.0% | 37.7% |
> | CLAHE + adaptive threshold + morph close | 8.6% | 14.2% |
> | CLAHE + Otsu | 24.7% | 29.5% |
> | Otsu only | 25.4% | 32.4% |
>
> **Finding:** Binarization (adaptive threshold, Otsu) consistently degrades recall on real phone photos. Tesseract's LSTM uses gradient information that binary thresholding destroys. CLAHE alone also provides no net benefit. **Grayscale-only is the optimal preprocessing for this dataset.** The improvement plan's expectation (+15–30%) was based on the wrong assumption that phone photos benefit from binarization.
>
> **Status: Closed — no change needed. Preprocessing remains grayscale-only.**

---

### Priority 2 — Add Portuguese Language Data

**Current state:** Tesseract is initialized with `'eng'` only.

**Problem:** Most items in the `img-impr` images are Brazilian Portuguese titles (Agatha Christie translations, sertanejo albums, etc.). Characters like `ã`, `ç`, `é`, `ô` are either dropped or garbled by an English-only model.

**Solution:** Initialize the worker with `['eng', 'por']`:

```javascript
ocrWorker = await Tesseract.createWorker(['eng', 'por'], 1, { ... });
```

**Trade-off:** The `por.traineddata.gz` file is ~6.5 MB. It must be added to the service worker cache and to the `docs/static/js/vendor/lang-data/` directory. This increases first-load size.

**Expected impact:** Better recall for titles with Portuguese-specific characters. Also likely reduces false positives (garbled guesses) on Portuguese words.

> **✅ IMPLEMENTED & BENCHMARKED (2026-03-17).**
> Measured on `img-impr` (8 images, grayscale + PSM 12 + 3-pass):
>
> | Config | Avg Recall |
> |---|---|
> | eng, 2-pass (baseline) | 38.8% |
> | eng+por, 2-pass | 38.8% |
> | eng+por, 3-pass (final) | 41.5% |
>
> **Finding:** +0.3pp from Portuguese on this specific dataset. The `img-impr` images happen to be predominantly English-language rock/pop CDs (AC/DC, Deep Purple, Kiss, etc.), so the benefit is minimal here. The +por support is still correct to ship — a sebo shelf photographed in a different session is more likely to contain Portuguese-language titles where it will matter.

---

### Priority 3 — Add Counter-Clockwise Rotation Pass

**Current state:** Dual-pass = 0° + 90° clockwise.

**Problem:** Spine labels on shelves are commonly printed both ways. The current code rotates clockwise only, missing spines that are rotated the other way.

**Solution:** Add a third pass with `cv.ROTATE_90_COUNTERCLOCKWISE`. This triples OCR processing time, but all three passes run sequentially and the result is deduplicated via `Set`.

If three passes is too slow, benchmark which rotation direction dominates in the `img-impr` images and keep only the two most useful.

> **✅ IMPLEMENTED & BENCHMARKED (2026-03-17).**
> Measured on `img-impr` (8 images, grayscale + PSM 12 + eng+por):
>
> | Config | Avg Recall |
> |---|---|
> | eng, 2-pass (baseline) | 38.8% |
> | eng, 3-pass | 41.2% |
> | eng+por, 3-pass (final) | 41.5% |
>
> **Finding:** +2.4pp from the CCW pass. Effective — confirms the img-impr shelf has spines oriented in both directions.

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

| Priority | Change | Effort | Measured Impact (img-impr) | Status |
|----------|--------|--------|----------------------------|--------|
| 1 | Better preprocessing (CLAHE + adaptive threshold + morphology) | Low | **−27pp** (14.2% vs 41.5% baseline) — harmful, do not apply | ❌ Closed — no change |
| 2 | Add Portuguese language data (`por`) | Low | **+0.3pp** (38.8% → 38.8% eng-only; minimal on this dataset) | ✅ Shipped (correct for PT-heavy sessions) |
| 3 | Add 270° (CCW) rotation pass | Trivial | **+2.4pp** (38.8% → 41.2%) | ✅ Shipped |
| 4 | Evaluate PSM 11 vs PSM 12 on img-impr | Low | PSM 12 wins by **+7pp** (41.5% vs 34.2%); keep PSM 12 | ✅ Closed — keep PSM 12 |
| 5 | Replace Tesseract.js with TrOCR (Transformers.js) | High | Not yet measured — next highest-value path | 🔲 Pending |
| 6 | Deskewing via Hough Lines | Medium | Not yet measured | 🔲 Pending |

**Baseline (before P2+P3):** 38.8% avg token recall on `img-impr` (gray + PSM 12 + eng + 2-pass).
**After P2+P3:** 41.5% avg token recall (+2.7pp).

**Next recommended step:** Priority 5 (TrOCR via Transformers.js) — the only remaining path likely to produce a step-change improvement. Prototype on a separate branch and benchmark against `img-impr` before merging.

---

## Questions answered

1. **Cache size budget:** An ~80–100 MB one-time download is acceptable for the TrOCR path (Priority 5). This would make the initial app load much heavier, but subsequent uses are fully offline. Currently the app is ~15–20 MB cached. In general, I prefer lightweight sollutions, but I'm willing to trade memory for performance (up to a sensible point).

2. **Processing time budget:** The dual-pass OCR already takes a few seconds per image. Adding a third rotation pass and/or TrOCR inference would increase this, but I am not yet worried about it. An acceptable upper bound is 10 seconds of processing time per image.
