# Track: OCR Performance Improvement Iteration 2

## Overview
This track aims to further improve the OCR accuracy of the `sebo-helper` application using a new set of 8 CD spine images located in `training-images/img-impr/`. These images provide additional data points for tuning the extraction pipeline.

## Goals
- Establish a baseline accuracy on the new dataset using the current Tesseract PSM 12 implementation.
- Explore alternative OCR engines (EasyOCR) and preprocessing techniques.
- Improve title extraction accuracy specifically for varied CD spine layouts.

## Success Criteria
- Higher average accuracy on the new dataset compared to the baseline.
- Robust handling of vertical and horizontal text on spines.
