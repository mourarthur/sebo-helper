// app/static/js/pwa.js

document.addEventListener('DOMContentLoaded', () => {
    console.log('PWA JS: DOMContentLoaded');

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
        if (appDiv) appDiv.insertBefore(installBtn, appDiv.firstChild);
    });

    const cameraInput = document.getElementById('cameraInput');
    const galleryInput = document.getElementById('galleryInput');
    const extractBtn = document.getElementById('extractBtn');
    const resultsList = document.getElementById('pwa-results-list');
    const imageCanvas = document.getElementById('imageCanvas');
    const wishlistInput = document.getElementById('wishlistInput');

    // Load wishlist on start
    if (window.storage) {
        const savedWishlist = window.storage.getWishlist();
        if (savedWishlist.length > 0 && wishlistInput) {
            wishlistInput.value = savedWishlist.join('\n');
        }
    }

    if (document.getElementById('saveWishlistBtn')) {
        document.getElementById('saveWishlistBtn').onclick = () => {
            if (window.storage && wishlistInput) {
                const items = window.storage.saveWishlist(wishlistInput.value);
                alert(`Wishlist saved (${items.length} items)`);
            }
        };
    }

    function handleFileSelect(e) {
        console.log('File selected event:', e);
        const file = e.target.files[0];
        if (!file) {
            console.log('No file selected');
            return;
        }

        const indicator = document.getElementById('status-indicator');
        const placeholder = document.getElementById('canvasPlaceholder');
        
        if (indicator) indicator.innerText = "Loading image...";
        if (placeholder) placeholder.style.display = 'none';
        if (extractBtn) extractBtn.style.display = 'none';

        const ctx = imageCanvas.getContext('2d');
        const img = new Image();
        
        img.onload = () => {
            console.log('Image loaded successfully');
            // Simple scale if too large for display (not for processing yet)
            const maxWidth = window.innerWidth - 40;
            const scale = Math.min(1, maxWidth / img.width);
            imageCanvas.width = img.width * scale;
            imageCanvas.height = img.height * scale;
            
            ctx.drawImage(img, 0, 0, imageCanvas.width, imageCanvas.height);
            imageCanvas.style.display = 'block';
            
            if (indicator) indicator.innerText = "Image loaded.";
            
            if (extractBtn) {
                extractBtn.style.display = 'block';
                console.log('Show extract button');
            }
        };
        
        img.onerror = (err) => {
            console.error('Error loading image:', err);
            if (indicator) indicator.innerText = "Error loading image.";
            if (extractBtn) extractBtn.style.display = 'none'; // Keep hidden on error
        };
        
        try {
            img.src = URL.createObjectURL(file);
        } catch (error) {
            console.error('URL.createObjectURL failed:', error);
            if (indicator) indicator.innerText = "Error creating image URL.";
        }
    }

    if (cameraInput) {
        cameraInput.addEventListener('change', handleFileSelect);
        console.log('Camera input listener attached');
    } else {
        console.error('Camera input element not found');
    }

    if (galleryInput) {
        galleryInput.addEventListener('change', handleFileSelect);
         console.log('Gallery input listener attached');
    } else {
        console.error('Gallery input element not found');
    }

    if (extractBtn) {
        extractBtn.onclick = async () => {
            try {
                const indicator = document.getElementById('status-indicator');
                const progressContainer = document.getElementById('progress-container');
                
                if (indicator) {
                    indicator.innerText = "Preprocessing image...";
                    indicator.style.backgroundColor = '#fff3cd';
                }
                
                // 1. Preprocess
                const processedCanvas = preprocessCanvas(imageCanvas);
                
                // 2. Run OCR
                if (indicator) indicator.innerText = "Running OCR (Tesseract)...";
                const text = await runOCR(processedCanvas);
                
                // 3. Display Results
                if (indicator) {
                    indicator.innerText = "OCR Complete!";
                    indicator.style.backgroundColor = '#d4edda';
                }
                if (progressContainer) progressContainer.style.display = 'none';
                
                const wishlist = window.storage ? window.storage.getWishlist() : [];
                if (resultsList) {
                    resultsList.innerHTML = '';
                    const lines = text.split('\n').filter(line => line.trim().length > 0);
                    if (lines.length === 0) {
                        resultsList.innerHTML = '<li>No text found in image</li>';
                    } else {
                        lines.forEach(line => {
                            const li = document.createElement('li');
                            li.textContent = line.trim();
                            li.style.borderBottom = '1px solid #eee';
                            li.style.padding = '5px 0';
                            
                            if (window.matching && window.matching.isMatch(line.trim(), wishlist)) {
                                li.style.backgroundColor = '#d4edda';
                                li.style.fontWeight = 'bold';
                                li.textContent += ' (MATCH!)';
                            }
                            
                            resultsList.appendChild(li);
                        });
                    }
                }
            } catch (err) {
                console.error(err);
                const indicator = document.getElementById('status-indicator');
                if (indicator) {
                    indicator.innerText = "OCR Error: " + err.message;
                    indicator.style.backgroundColor = '#f8d7da';
                }
            }
        };
    }
});

function updateOpenCvStatus() {
    const indicator = document.getElementById('status-indicator');
    if (!indicator) return false;

    if (typeof isCvReady === 'function' && isCvReady()) {
        indicator.innerText = "OpenCV is ready! (v3.1)";
        indicator.style.backgroundColor = '#d4edda';
        return true;
    } else if (typeof cv !== 'undefined' && cv.getBuildInformation) {
        // Already ready but isCvReady() is false (sync issue)
        indicator.innerText = "OpenCV is ready (sync fixed)! (v3.1)";
        indicator.style.backgroundColor = '#d4edda';
        return true;
    }
    return false;
}

async function testOpenCV() {
    const indicator = document.getElementById('status-indicator');
    if (updateOpenCvStatus()) {
        // Already ready
    } else {
        if (indicator) {
            indicator.innerText = "Waiting for OpenCV to load (this can take 10-20s, 10MB file)...";
            indicator.style.backgroundColor = '#fff3cd';
        }
    }
}

window.addEventListener('opencv-ready', () => {
    updateOpenCvStatus();
});

// Check immediately on script load (outside DOMContentLoaded just in case)
updateOpenCvStatus();

async function testOCR() {
    const indicator = document.getElementById('status-indicator');
    try {
        if (indicator) indicator.innerText = "Initializing OCR...";
        await initTesseract();
        if (indicator) {
            indicator.innerText = "OCR Initialized! Ready to scan.";
            indicator.style.backgroundColor = '#d1ecf1';
        }
    } catch (e) {
        console.error(e);
        if (indicator) {
            indicator.innerText = "Error: " + e.message;
            indicator.style.backgroundColor = '#f8d7da';
        }
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
        if (progressContainer) progressContainer.style.display = 'block';
        const percent = Math.round(detail.progress * 100);
        if (progressBar) progressBar.value = percent;
        if (progressText) progressText.innerText = `${detail.status}: ${percent}%`;
    } else {
        if (progressText) progressText.innerText = detail.status;
    }

    const log = document.getElementById('log');
    if (log) {
        if (detail.status === 'recognizing text') {
                log.innerText = `Recognizing: ${(detail.progress * 100).toFixed(0)}%`;
        } else {
                log.innerText = detail.status;
        }
    }
});
