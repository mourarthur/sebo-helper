from typing import List
from rapidfuzz import fuzz

def is_match(title: str, wishlist: List[str], threshold: int = 70) -> bool:
    """
    Checks if a title matches any item in the wishlist.
    Matching is case-insensitive, checks for string inclusion,
    and uses fuzzy matching for robustness against OCR errors.
    """
    title_lower = title.lower()
    for item in wishlist:
        item_lower = item.lower()
        
        # 1. Simple substring match (fast)
        if item_lower in title_lower or title_lower in item_lower:
            return True
            
        # 2. Fuzzy match (robust)
        # partial_ratio is good for finding substrings with errors
        if fuzz.partial_ratio(item_lower, title_lower) >= threshold:
            return True
            
    return False
