// app/static/js/image-processor.js

let cvReady = false;
console.time('OpenCV-Loading');

function onOpenCvReady() {
    if (cvReady) return; // Only fire once
    console.log('OpenCV.js is ready.');
    console.timeEnd('OpenCV-Loading');
    cvReady = true;
    // Dispatch event to notify the UI
    window.dispatchEvent(new CustomEvent('opencv-ready'));
    // If we're already on the PWA page, update the UI directly if the element exists
    const indicator = document.getElementById('status-indicator');
    if (indicator) {
        indicator.innerText = "OpenCV is ready!";
    }
}

// Emscripten hook via Module
if (typeof window.Module === 'undefined') {
    window.Module = {
        onRuntimeInitialized: onOpenCvReady
    };
} else {
    window.Module.onRuntimeInitialized = onOpenCvReady;
}

// Some builds might expect cv.onRuntimeInitialized
if (typeof window.cv !== 'undefined') {
    window.cv.onRuntimeInitialized = onOpenCvReady;
    // If it's already ready, call it
    if (window.cv.getBuildInformation) {
        onOpenCvReady();
    }
}

/**
 * Loads a File object (from <input type="file">) into a cv.Mat
 * @param {File} file 
 * @returns {Promise<cv.Mat>}
 */
async function loadImageToMat(file) {
    if (!cvReady) {
        throw new Error("OpenCV is not ready yet.");
    }
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (event) => {
            const img = new Image();
            img.onload = () => {
                const canvas = document.createElement('canvas');
                canvas.width = img.width;
                canvas.height = img.height;
                const ctx = canvas.getContext('2d');
                ctx.drawImage(img, 0, 0);
                
                try {
                    const mat = cv.imread(canvas);
                    resolve(mat);
                } catch (err) {
                    reject(err);
                }
            };
            img.onerror = () => reject(new Error("Failed to load image element"));
            img.src = event.target.result;
        };
        reader.onerror = () => reject(new Error("Failed to read file"));
        reader.readAsDataURL(file);
    });
}

// Expose utilities
window.loadImageToMat = loadImageToMat;
window.isCvReady = () => cvReady;
