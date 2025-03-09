self.addEventListener("install", (event) => {
    event.waitUntil(
        caches.open("pwa-cache").then((cache) => {
            return cache.addAll(["/index.html"]);
        })
    );
});

self.addEventListener("activate", (event) => {
    console.log("Service Worker activated.");
    return self.clients.claim();
});

self.addEventListener("fetch", (event) => {
    if (event.request.mode === "navigate") {
        event.respondWith(fetch(event.request).catch(() => caches.match("/index.html")));
    } else {
        event.respondWith(fetch(event.request));
    }
});
