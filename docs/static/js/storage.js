// app/static/js/storage.js

const STORAGE_KEYS = {
    WISHLIST: 'sebo-helper-wishlist',
    RESULTS: 'sebo-helper-results'
};

function saveWishlist(text) {
    // Clean and split by newline, filter empty
    const items = text.split('\n').map(s => s.trim()).filter(s => s.length > 0);
    localStorage.setItem(STORAGE_KEYS.WISHLIST, JSON.stringify(items));
    return items;
}

function getWishlist() {
    const data = localStorage.getItem(STORAGE_KEYS.WISHLIST);
    return data ? JSON.parse(data) : [];
}

function saveResults(titles) {
    localStorage.setItem(STORAGE_KEYS.RESULTS, JSON.stringify(titles));
}

function getResults() {
    const data = localStorage.getItem(STORAGE_KEYS.RESULTS);
    return data ? JSON.parse(data) : [];
}

function clearResults() {
    localStorage.removeItem(STORAGE_KEYS.RESULTS);
}

// Expose
window.storage = {
    saveWishlist,
    getWishlist,
    saveResults,
    getResults,
    clearResults
};
