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