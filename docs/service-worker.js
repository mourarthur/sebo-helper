const CACHE_NAME = 'sebo-helper-v2';
const ASSETS_TO_CACHE = [
  './index.html', './',
  './static/manifest.json',
  './static/css/style.css',
  './static/js/ocr-engine.js',
  './static/js/image-processor.js',
  './static/js/storage.js',
  './static/js/matching.js',
  './static/js/pwa.js',
  './static/js/vendor/tesseract.min.js',
  './static/js/vendor/worker.min.js',
  './static/js/vendor/tesseract-core.wasm.js',
  './static/js/vendor/opencv.js',
  './static/js/vendor/lang-data/eng.traineddata.gz',
  './static/icons/icon-192x192.png',
  './static/icons/icon-512x512.png'
];

self.addEventListener('install', (event) => {
  console.log('[Service Worker] Installing Service Worker ...', event);
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('[Service Worker] Caching App Shell');
        return cache.addAll(ASSETS_TO_CACHE);
      })
  );
});

self.addEventListener('activate', (event) => {
  console.log('[Service Worker] Activating Service Worker ....', event);
  event.waitUntil(
    caches.keys().then((keyList) => {
      return Promise.all(keyList.map((key) => {
        if (key !== CACHE_NAME) {
          console.log('[Service Worker] Removing old cache.', key);
          return caches.delete(key);
        }
      }));
    })
  );
  return self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then((response) => {
        if (response) {
          return response;
        }
        return fetch(event.request);
      })
  );
});
