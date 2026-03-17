// app/static/js/ocr-engine.js

let ocrWorker;

async function initTesseract() {
    if (ocrWorker) return ocrWorker;

    console.log("Initializing Tesseract...");
    
    try {
        ocrWorker = await Tesseract.createWorker(["eng", "por"], 1, {
            workerPath: './static/js/vendor/worker.min.js',
            corePath: './static/js/vendor/tesseract-core.wasm.js',
            langPath: './static/js/vendor/lang-data/',
            logger: m => {
                console.log(m);
                const event = new CustomEvent('ocr-progress', { detail: m });
                window.dispatchEvent(event);
            }
        });
        
        // Set PSM 12 (Sparse Text with OSD)
        // In Tesseract.js v5, PSM is available under Tesseract.PSM
        // 12 = Tesseract.PSM.SPARSE_TEXT_OSD
        await ocrWorker.setParameters({
            tessedit_pageseg_mode: Tesseract.PSM.SPARSE_TEXT_OSD,
        });

        console.log("Tesseract initialized.");
        return ocrWorker;
    } catch (err) {
        console.error("Failed to initialize Tesseract:", err);
        throw err;
    }
}

async function runOCR(imageSource) {
    if (!ocrWorker) {
        await initTesseract();
    }
    
    const ret = await ocrWorker.recognize(imageSource);
    return ret.data.text;
}

// Expose functions globally
window.initTesseract = initTesseract;
window.runOCR = runOCR;
