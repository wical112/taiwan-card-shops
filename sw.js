/* 台灣卡店地圖 — service worker
   Shell precache (offline 即開) + Leaflet SWR + OSM tile 上限快取。
   改版時 bump VERSION 觸發更新。 */
const VERSION = "v2-2026-05-16";
const SHELL = "shell-" + VERSION;
const TILES = "tiles-" + VERSION;
const LIB   = "lib-"   + VERSION;
const TILE_MAX = 350;

const SHELL_URLS = [
  "./", "./index.html", "./manifest.webmanifest", "./icon.svg",
];

self.addEventListener("install", e => {
  e.waitUntil(
    caches.open(SHELL).then(c => c.addAll(SHELL_URLS)).then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", e => {
  e.waitUntil(
    caches.keys().then(keys => Promise.all(
      keys.filter(k => ![SHELL, TILES, LIB].includes(k)).map(k => caches.delete(k))
    )).then(() => self.clients.claim())
  );
});

async function capCache(name, max) {
  const c = await caches.open(name);
  const keys = await c.keys();
  if (keys.length > max) await Promise.all(
    keys.slice(0, keys.length - max).map(k => c.delete(k))
  );
}

self.addEventListener("fetch", e => {
  const req = e.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);

  // OSM tiles — cache-first, capped runtime cache
  if (/tile\.openstreetmap\.org$/.test(url.hostname)) {
    e.respondWith((async () => {
      const c = await caches.open(TILES);
      const hit = await c.match(req);
      if (hit) return hit;
      try {
        const res = await fetch(req);
        if (res.ok) { c.put(req, res.clone()); capCache(TILES, TILE_MAX); }
        return res;
      } catch { return hit || Response.error(); }
    })());
    return;
  }

  // Leaflet CDN — stale-while-revalidate
  if (url.hostname === "cdn.jsdelivr.net") {
    e.respondWith((async () => {
      const c = await caches.open(LIB);
      const hit = await c.match(req);
      const net = fetch(req).then(res => {
        if (res.ok) c.put(req, res.clone());
        return res;
      }).catch(() => hit);
      return hit || net;
    })());
    return;
  }

  // Same-origin shell — cache-first, fall back to network then cached index
  if (url.origin === self.location.origin) {
    e.respondWith((async () => {
      const c = await caches.open(SHELL);
      const hit = await c.match(req, { ignoreSearch: true });
      if (hit) return hit;
      try {
        const res = await fetch(req);
        if (res.ok) c.put(req, res.clone());
        return res;
      } catch {
        return (await c.match("./index.html")) || Response.error();
      }
    })());
  }
});
