from typing import List

def is_match(title: str, wishlist: List[str]) -> bool:
    """
    Checks if a title matches any item in the wishlist.
    Matching is case-insensitive and checks for string inclusion.
    """
    title_lower = title.lower()
    for item in wishlist:
        item_lower = item.lower()
        if item_lower in title_lower or title_lower in item_lower:
            return True
    return False
