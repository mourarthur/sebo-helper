// app/static/js/matching.js

function levenshtein(a, b) {
    if (a.length === 0) return b.length;
    if (b.length === 0) return a.length;
    const matrix = [];
    for (let i = 0; i <= b.length; i++) {
        matrix[i] = [i];
    }
    for (let j = 0; j <= a.length; j++) {
        matrix[0][j] = j;
    }
    for (let i = 1; i <= b.length; i++) {
        for (let j = 1; j <= a.length; j++) {
            if (b.charAt(i - 1) === a.charAt(j - 1)) {
                matrix[i][j] = matrix[i - 1][j - 1];
            } else {
                matrix[i][j] = Math.min(
                    matrix[i - 1][j - 1] + 1,
                    matrix[i][j - 1] + 1,
                    matrix[i - 1][j] + 1
                );
            }
        }
    }
    return matrix[b.length][a.length];
}

function ratio(a, b) {
    const len = Math.max(a.length, b.length);
    if (len === 0) return 100;
    const dist = levenshtein(a.toLowerCase(), b.toLowerCase());
    return (1 - dist / len) * 100;
}

function isMatch(text, wishlist) {
    if (!wishlist || wishlist.length === 0) return false;
    
    const threshold = 70;
    const normText = text.toLowerCase();
    
    for (const item of wishlist) {
        const normItem = item.toLowerCase();
        if (normItem.length < 3) continue; // Skip very short words
        
        // Exact substring check
        if (normText.includes(normItem)) return true;
        
        // Fuzzy check
        if (ratio(normText, normItem) > threshold) return true;
    }
    return false;
}

window.matching = {
    isMatch
};
