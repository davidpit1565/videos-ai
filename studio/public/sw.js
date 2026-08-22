/* The studio's service worker. Its only job is notifications.
 *
 * Deliberately caches nothing. An offline cache on a tool whose whole point is showing the
 * real current numbers would be a way to show stale ones, and this project already spent a
 * day on a studio quietly serving data that was not current. */

self.addEventListener("install", (e) => self.skipWaiting());
self.addEventListener("activate", (e) => e.waitUntil(self.clients.claim()));

self.addEventListener("push", (event) => {
  let n = { title: "Actually Works", body: "" };
  try {
    if (event.data) n = { ...n, ...event.data.json() };
  } catch (_) {
    if (event.data) n.body = event.data.text();
  }
  event.waitUntil(
    self.registration.showNotification(n.title, {
      body: n.body,
      // the tag collapses repeats of the same kind rather than stacking twelve of them
      tag: n.tag || "aw",
      renotify: true,
      icon: "/icon-192.png",
      badge: "/icon-192.png",
      data: { url: n.url || "/studio" },
    }),
  );
});

self.addEventListener("notificationclick", (event) => {
  event.notification.close();
  const url = (event.notification.data && event.notification.data.url) || "/studio";
  event.waitUntil(
    (async () => {
      const all = await self.clients.matchAll({ type: "window", includeUncontrolled: true });
      // focus a studio window that is already open instead of opening a fourth one
      for (const c of all) {
        if (c.url.includes(self.location.origin)) {
          await c.focus();
          if ("navigate" in c) await c.navigate(url);
          return;
        }
      }
      await self.clients.openWindow(url);
    })(),
  );
});
