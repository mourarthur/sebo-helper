# PSM Mode Experiment Results Summary

## Objective
To evaluate the impact of different Tesseract Page Segmentation Modes (PSM) on OCR accuracy for the `sample-images` dataset.

## Methodology
The `benchmark.py` script was used with the `--psm` argument to test four different PSM modes: 3 (default), 6, 11, and 12. The average Levenshtein accuracy was calculated for each mode across all sample images.

## Results

| PSM Mode | Average Accuracy (%) |
| :------- | :------------------ |
| 3 (Default) | 11.52              |
| 6        | 12.46              |
| 11       | 12.98              |
| 12       | **20.95**          |

### Image-Specific Highlights (PSM 12)
- **OCR3.jpeg:** Showed the most significant improvement with an accuracy of 42.99%, suggesting PSM 12 is particularly effective for this image's layout.

## Conclusion
PSM 12 ("Sparse text. Find as much text as possible in no particular order.") provided the best overall average accuracy (20.95%) for the `sample-images` dataset, demonstrating a substantial improvement over the default PSM 3 and other tested modes.

Further experimentation with other parameters (OEM, language, preprocessing) combined with PSM 12 is recommended.

## Alternative Engine Evaluation: EasyOCR vs. Tesseract (PSM 12)

| Engine / Configuration | Average Accuracy (%) |
| :--------------------- | :------------------- |
| Tesseract (PSM 12)     | **20.95**            |
| EasyOCR                | 8.61                 |

### Observations
- EasyOCR performed significantly worse than Tesseract with PSM 12 on this specific dataset.
- This might be due to EasyOCR's default configuration not being optimized for the "spine text" use case, or the dataset itself being more aligned with Tesseract's strengths.
- Further tuning of EasyOCR (e.g., custom models, more aggressive preprocessing outside its internal capabilities) could potentially improve its performance, but for out-of-the-box usage on this dataset, Tesseract remains superior.

## Preprocessing Experiment Results (PSM 12 with OSD-based Rotation)

| Configuration        | Average Accuracy (%) |
| :------------------- | :------------------ |
| PSM 12 (No Preprocess) | **20.95**          |
| PSM 12 (With Preprocess) | 20.35             |

### Observations
- OSD-based rotation for preprocessing, as implemented, resulted in a slight decrease in overall accuracy.
- Tesseract's OSD can be unreliable on images with sparse text or low resolution, leading to "Too few characters. Skipping this page" errors and potentially incorrect rotations.
- This suggests that a more robust rotation detection mechanism (e.g., OpenCV-based deskewing or a multi-pass approach) might be necessary, or OSD should be applied selectively.