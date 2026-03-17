// app/static/js/image-processor.js

let cvReady = false;
console.time('OpenCV-Loading');

function onOpenCvReady() {
    if (cvReady) return; // Only fire once
    console.log('OpenCV.js is ready (via onRuntimeInitialized).');
    console.timeEnd('OpenCV-Loading');
    cvReady = true;
    window.dispatchEvent(new CustomEvent('opencv-ready'));
    
    const indicator = document.getElementById('status-indicator');
    if (indicator) {
        indicator.innerText = "OpenCV is ready!";
        indicator.style.backgroundColor = '#d4edda';
    }
}

// Setup Emscripten Module
window.Module = {
    onRuntimeInitialized: onOpenCvReady,
    print: (text) => console.log('[OpenCV]', text),
    printErr: (text) => console.error('[OpenCV Err]', text)
};

// Polling fallback
const checkInterval = setInterval(() => {
    if (cvReady) {
        clearInterval(checkInterval);
        return;
    }
    
    if (typeof cv !== 'undefined') {
        // Try to access a function to ensure it's fully initialized
        try {
            if (cv.getBuildInformation) {
                console.log("OpenCV detected via polling.");
                onOpenCvReady();
                clearInterval(checkInterval);
            }
        } catch (e) {
            // Ignored, not ready
        }
    }
}, 1000);

// Stop polling after 60 seconds
setTimeout(() => clearInterval(checkInterval), 60000);


/**
 * Loads a File object (from <input type="file">) into a cv.Mat
 * @param {File} file 
 * @returns {Promise<cv.Mat>}
 */
async function loadImageToMat(file) {
    if (!cvReady) {
        throw new Error("OpenCV is not ready yet. Please wait.");
    }
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (event) => {
            const img = new Image();
            img.onload = () => {
                const MAX_DIM = 2000;
                let width = img.width;
                let height = img.height;

                if (width > MAX_DIM || height > MAX_DIM) {
                    if (width > height) {
                        height = Math.round(height * (MAX_DIM / width));
                        width = MAX_DIM;
                    } else {
                        width = Math.round(width * (MAX_DIM / height));
                        height = MAX_DIM;
                    }
                }

                const canvas = document.createElement('canvas');
                canvas.width = width;
                canvas.height = height;
                const ctx = canvas.getContext('2d');
                ctx.drawImage(img, 0, 0, width, height);
                
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

/**
 * Preprocesses an image Mat for better OCR results.
 * Benchmarked on img-impr (real phone photos): grayscale-only outperforms all
 * binarization pipelines (adaptive, Otsu, CLAHE+adaptive) because Tesseract's
 * LSTM uses gradient information that binary thresholding destroys.
 * @param {cv.Mat} src
 * @returns {cv.Mat}
 */
function preprocessImage(src) {
    let dst = new cv.Mat();
    cv.cvtColor(src, dst, cv.COLOR_RGBA2GRAY, 0);
    return dst;
}

/**
 * Preprocesses a canvas and returns a new canvas with the result.
 * @param {HTMLCanvasElement} sourceCanvas 
 * @returns {HTMLCanvasElement}
 */
function preprocessCanvas(sourceCanvas) {
    if (!cvReady) throw new Error("OpenCV not ready");
    
    let src = cv.imread(sourceCanvas);
    let dst = preprocessImage(src);
    
    const outCanvas = document.createElement('canvas');
    cv.imshow(outCanvas, dst);
    
    src.delete();
    dst.delete();
    
    return outCanvas;
}

/**
 * Creates a 90-degree clockwise rotated copy of a canvas.
 * @param {HTMLCanvasElement} sourceCanvas 
 * @returns {HTMLCanvasElement}
 */
function rotateCanvas(sourceCanvas) {
    if (!cvReady) throw new Error("OpenCV not ready");
    
    let src = cv.imread(sourceCanvas);
    let dst = new cv.Mat();
    
    // Rotate 90 degrees clockwise
    cv.rotate(src, dst, cv.ROTATE_90_CLOCKWISE);
    
    const outCanvas = document.createElement('canvas');
    cv.imshow(outCanvas, dst);
    
    src.delete();
    dst.delete();
    
    return outCanvas;
}

/**
 * Creates a 90-degree counter-clockwise rotated copy of a canvas.
 * @param {HTMLCanvasElement} sourceCanvas
 * @returns {HTMLCanvasElement}
 */
function rotateCanvasCCW(sourceCanvas) {
    if (!cvReady) throw new Error("OpenCV not ready");

    let src = cv.imread(sourceCanvas);
    let dst = new cv.Mat();

    cv.rotate(src, dst, cv.ROTATE_90_COUNTERCLOCKWISE);

    const outCanvas = document.createElement('canvas');
    cv.imshow(outCanvas, dst);

    src.delete();
    dst.delete();

    return outCanvas;
}

// Expose utilities
window.loadImageToMat = loadImageToMat;
window.preprocessCanvas = preprocessCanvas;
window.rotateCanvas = rotateCanvas;
window.rotateCanvasCCW = rotateCanvasCCW;
window.isCvReady = () => cvReady;
