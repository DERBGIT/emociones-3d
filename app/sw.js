/* Service worker de Emociones 3D.
 * - Precarga los archivos propios (index, glosario, manifest, iconos).
 * - Cachea en tiempo de ejecución las librerías de esm.sh y Tailwind.
 * - Estrategia: red primero para lo propio (para recibir versiones nuevas), caché de respaldo si no hay red;
 *   caché primero para las librerías externas (sus URL llevan versión fija).
 * Al publicar una versión nueva de la app o del glosario, suba VERSION.
 */
const VERSION = 'emociones3d-v5.0.1';
const PROPIOS = ['./', './index.html', './glosario.js', './glosario.json', './manifest.webmanifest',
  './icons/icon-192.png', './icons/icon-512.png', './icons/icon-maskable-512.png', './icons/apple-touch-icon.png'];
const EXTERNOS = ['https://esm.sh/', 'https://cdn.tailwindcss.com'];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(VERSION).then((c) => c.addAll(PROPIOS)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', (e) => {
  e.waitUntil(caches.keys().then((keys) => Promise.all(keys.filter((k) => k !== VERSION).map((k) => caches.delete(k)))).then(() => self.clients.claim()));
});

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = req.url;
  const esExterno = EXTERNOS.some((p) => url.startsWith(p));

  if (esExterno) {
    e.respondWith(caches.match(req).then((hit) => hit || fetch(req).then((res) => {
      if (res && (res.ok || res.type === 'opaque')) { const copia = res.clone(); caches.open(VERSION).then((c) => c.put(req, copia)); }
      return res;
    })));
    return;
  }

  if (new URL(url).origin === self.location.origin) {
    e.respondWith(fetch(req).then((res) => {
      if (res && res.ok) { const copia = res.clone(); caches.open(VERSION).then((c) => c.put(req, copia)); }
      return res;
    }).catch(() => caches.match(req).then((hit) => hit || (req.mode === 'navigate' ? caches.match('./index.html') : undefined))));
  }
});
