# OCR Improvement Results Summary

## Comparison: Baseline vs. Improved

| Image | Baseline Result Snippet | Improved Result Snippet | Improvement |
| :--- | :--- | :--- | :--- |
| `OCR2` | `os elefantes nao esquecerm` | `os elefantes nao esquecerm`, `Agatha Christie` | Found author name via PSM 5 |
| `OCR3` | `A MORTE No NIL0`, `OS CRIMES ABC` | `A MORTE No NIL0`, `OS CRIMES ABC`, `ASSASSINATO` | Found more titles |
| `OCR4` | `LEGIAG URBANA` | `LEGIAG URBANA`, `urban` | Found 'urban' in PSM 11 |
| `OCR5` | `THEWHO-QUADROPHENIA` | `THEWHO-QUADROPHENIA`, `EMPTY GLASS` | Found more text |
| `OCR6` | (Empty) | (Still Mostly Empty/Garbage) | No significant improvement |

## Key Findings
- **Multi-pass OCR** (Original, Deskewed, 90°, 180°) significantly increases recall by capturing text at different orientations.
- **PSM 5 (Vertical)** is surprisingly effective for some stylized horizontal text and actual vertical spines.
- **PSM 11 (Sparse)** helps pick up isolated words that the auto-segmentation (PSM 3) might miss.
- **Deskewing** helps Tesseract's internal line detection.

## Next Steps for Future Tracks
- **Spine Segmentation:** Detecting and cropping individual spines before OCR would likely solve the remaining accuracy issues (like `LEGIAG` vs `LEGIAO`).
- **Dictionary/NLP:** Using a fuzzy search against a media database (Discogs, MusicBrainz, OpenLibrary) would correct OCR typos automatically.
