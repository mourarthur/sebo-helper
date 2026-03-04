// app/static/js/pwa.js

// Offline Status
window.addEventListener('online', updateOnlineStatus);
window.addEventListener('offline', updateOnlineStatus);

function updateOnlineStatus() {
    const bannerId = 'offline-banner';
    let banner = document.getElementById(bannerId);
    
    if (!navigator.onLine) {
        if (!banner) {
            banner = document.createElement('div');
            banner.id = bannerId;
            banner.className = 'offline-banner';
            banner.innerText = 'You are currently offline. App is fully functional.';
            document.body.appendChild(banner);
        }
    } else {
        if (banner) {
            banner.remove();
        }
    }
}
updateOnlineStatus();

// Install Prompt
let deferredPrompt;
window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
    
    const installBtn = document.createElement('button');
    installBtn.id = 'installBtn';
    installBtn.className = 'btn btn-primary';
    installBtn.innerText = 'Install Sebo Helper';
    installBtn.style.display = 'block';
    installBtn.style.width = '100%';
    installBtn.style.marginBottom = '10px';
    
    installBtn.onclick = async () => {
        if (deferredPrompt) {
            deferredPrompt.prompt();
            const { outcome } = await deferredPrompt.userChoice;
            deferredPrompt = null;
            installBtn.remove();
        }
    };
    
    const appDiv = document.getElementById('pwa-app');
    appDiv.insertBefore(installBtn, appDiv.firstChild);
});

const cameraInput = document.getElementById('cameraInput');
const galleryInput = document.getElementById('galleryInput');
const extractBtn = document.getElementById('extractBtn');
const resultsList = document.getElementById('pwa-results-list');
const imageCanvas = document.getElementById('imageCanvas');
const wishlistInput = document.getElementById('wishlistInput');

// Load wishlist on start
const savedWishlist = window.storage.getWishlist();
if (savedWishlist.length > 0 && wishlistInput) {
    wishlistInput.value = savedWishlist.join('\n');
}

if (document.getElementById('saveWishlistBtn')) {
    document.getElementById('saveWishlistBtn').onclick = () => {
        const items = window.storage.saveWishlist(wishlistInput.value);
        alert(`Wishlist saved (${items.length} items)`);
    };
}

function handleFileSelect(e) {
    const file = e.target.files[0];
    if (!file) return;

    document.getElementById('status-indicator').innerText = "Loading image...";
    document.getElementById('canvasPlaceholder').style.display = 'none';
    if (extractBtn) extractBtn.style.display = 'none';

    const ctx = imageCanvas.getContext('2d');
    const img = new Image();
    img.onload = () => {
        // Simple scale if too large for display (not for processing yet)
        const maxWidth = window.innerWidth - 40;
        const scale = Math.min(1, maxWidth / img.width);
        imageCanvas.width = img.width * scale;
        imageCanvas.height = img.height * scale;
        
        ctx.drawImage(img, 0, 0, imageCanvas.width, imageCanvas.height);
        imageCanvas.style.display = 'block';
        document.getElementById('status-indicator').innerText = "Image loaded.";
        
        if (extractBtn) {
            extractBtn.style.display = 'block';
            console.log('Show extract button');
        }
    };
    img.onerror = () => {
        document.getElementById('status-indicator').innerText = "Error loading image.";
    };
    img.src = URL.createObjectURL(file);
}

if (cameraInput) {
    cameraInput.addEventListener('change', handleFileSelect);
}
if (galleryInput) {
    galleryInput.addEventListener('change', handleFileSelect);
}

if (extractBtn) {
    extractBtn.onclick = async () => {
        try {
            document.getElementById('status-indicator').innerText = "Preprocessing image...";
            document.getElementById('status-indicator').style.backgroundColor = '#fff3cd';
            
            // 1. Preprocess
            const processedCanvas = preprocessCanvas(imageCanvas);
            
            // 2. Run OCR
            document.getElementById('status-indicator').innerText = "Running OCR (Tesseract)...";
            const text = await runOCR(processedCanvas);
            
            // 3. Display Results
            document.getElementById('status-indicator').innerText = "OCR Complete!";
            document.getElementById('status-indicator').style.backgroundColor = '#d4edda';
            document.getElementById('progress-container').style.display = 'none';
            
            const wishlist = window.storage.getWishlist();
            resultsList.innerHTML = '';
            const lines = text.split('
').filter(line => line.trim().length > 0);
            if (lines.length === 0) {
                resultsList.innerHTML = '<li>No text found in image</li>';
            } else {
                lines.forEach(line => {
                    const li = document.createElement('li');
                    li.textContent = line.trim();
                    li.style.borderBottom = '1px solid #eee';
                    li.style.padding = '5px 0';
                    
                    if (window.matching.isMatch(line.trim(), wishlist)) {
                        li.style.backgroundColor = '#d4edda';
                        li.style.fontWeight = 'bold';
                        li.textContent += ' (MATCH!)';
                    }
                    
                    resultsList.appendChild(li);
                });
            }
        } catch (err) {
            console.error(err);
            document.getElementById('status-indicator').innerText = "OCR Error: " + err.message;
            document.getElementById('status-indicator').style.backgroundColor = '#f8d7da';
        }
    };
}

function updateOpenCvStatus() {
    if (typeof isCvReady === 'function' && isCvReady()) {
        document.getElementById('status-indicator').innerText = "OpenCV is ready! (v2)";
        document.getElementById('status-indicator').style.backgroundColor = '#d4edda';
        return true;
    } else if (typeof cv !== 'undefined' && cv.getBuildInformation) {
        // Already ready but isCvReady() is false (sync issue)
        document.getElementById('status-indicator').innerText = "OpenCV is ready (sync fixed)! (v2)";
        document.getElementById('status-indicator').style.backgroundColor = '#d4edda';
        return true;
    }
    return false;
}

async function testOpenCV() {
    if (updateOpenCvStatus()) {
        // Already ready
    } else {
        document.getElementById('status-indicator').innerText = "Waiting for OpenCV to load (this can take 10-20s, 10MB file)...";
        document.getElementById('status-indicator').style.backgroundColor = '#fff3cd';
    }
}

window.addEventListener('opencv-ready', () => {
    updateOpenCvStatus();
});

// Check immediately on script load
updateOpenCvStatus();

async function testOCR() {
    try {
        document.getElementById('status-indicator').innerText = "Initializing OCR...";
        await initTesseract();
        document.getElementById('status-indicator').innerText = "OCR Initialized! Ready to scan.";
        document.getElementById('status-indicator').style.backgroundColor = '#d1ecf1';
    } catch (e) {
        console.error(e);
        document.getElementById('status-indicator').innerText = "Error: " + e.message;
        document.getElementById('status-indicator').style.backgroundColor = '#f8d7da';
    }
}

// Expose test functions globally for buttons
window.testOCR = testOCR;
window.testOpenCV = testOpenCV;

window.addEventListener('ocr-progress', (e) => {
    const detail = e.detail;
    const progressContainer = document.getElementById('progress-container');
    const progressBar = document.getElementById('ocr-progress-bar');
    const progressText = document.getElementById('progress-text');
    
    if (detail.progress !== undefined && detail.progress >= 0 && detail.progress <= 1) {
        progressContainer.style.display = 'block';
        const percent = Math.round(detail.progress * 100);
        progressBar.value = percent;
        progressText.innerText = `${detail.status}: ${percent}%`;
    } else {
        progressText.innerText = detail.status;
    }

    const log = document.getElementById('log');
    if (detail.status === 'recognizing text') {
            log.innerText = `Recognizing: ${(detail.progress * 100).toFixed(0)}%`;
    } else {
            log.innerText = detail.status;
    }
});
