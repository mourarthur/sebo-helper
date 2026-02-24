# Specification: Wishlist Management and Match Highlighting

## Objective
The goal is to allow users to maintain a wishlist of titles and have the application automatically highlight any matches found during OCR processing of media spines.

## Functional Requirements
1. **Wishlist Persistence:**
   - Store the wishlist in a simple file (e.g., `wishlist.json`) on the server.
   - The wishlist should be a list of strings (titles).

2. **Wishlist Management API:**
   - `GET /wishlist`: Retrieve the current wishlist.
   - `POST /wishlist`: Update the wishlist (e.g., replace the entire list with a new one provided by the user).
   - `DELETE /wishlist`: Clear the wishlist.

3. **Wishlist UI:**
   - A dedicated section in the web interface to view and edit the wishlist.
   - A simple text area where the user can paste titles (one per line).
   - A "Save Wishlist" button.

4. **Match Highlighting:**
   - When OCR results are displayed, any title that "matches" an item in the wishlist should be visually highlighted (e.g., green background, bold text).
   - Matching should be case-insensitive.
   - Initial matching can be simple string inclusion or exact match. Future improvements could include fuzzy matching.

## Technical Details
- **Persistence:** Update `app/services/persistence.py` to handle wishlist storage.
- **Frontend:** Modify `app/templates/index.html` and `app/static/css/style.css`.
- **Logic:** Implement a matching utility in `app/services/matching.py` or similar.

## Success Criteria
- User can save a wishlist.
- User can upload a photo.
- Any extracted title that appears in the wishlist is clearly highlighted in the results list.
- Wishlist is preserved across sessions (stored on disk).
