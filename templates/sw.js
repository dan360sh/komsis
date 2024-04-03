
// if ('serviceWorker' in navigator) {
//     navigator.serviceWorker.register('/sw.js', { scope: '/' }).then(function(reg) {
//       // регистрация сработала
//       console.log('Registration succeeded. Scope is ' + reg.scope);
//     }).catch(function(error) {
//       // регистрация прошла неудачно
//       console.log('Registration failed with ' + error);
//     });
//   };
  
  
  
//   const CACHE = 'offline-fallback-v1';
  
//   // При установке воркера мы должны закешировать часть данных (статику).
//   self.addEventListener('install', (event) => {
//       event.waitUntil(
//           caches
//               .open(CACHE)
//               .then((cache) => cache.addAll([
//                 //   '/static/css/style.css',
//                   '/'
//                   ]))
//               // `skipWaiting()` необходим, потому что мы хотим активировать SW
//               // и контролировать его сразу, а не после перезагрузки.
//               .then(() => self.skipWaiting())
//       );
//   });
  
//   self.addEventListener('activate', (event) => {
//       // `self.clients.claim()` позволяет SW начать перехватывать запросы с самого начала,
//       // это работает вместе с `skipWaiting()`, позволяя использовать `fallback` с самых первых запросов.
//       event.waitUntil(self.clients.claim());
//       console.log('Активирован');
//   });
  
//   self.addEventListener('fetch', function(event) {
//       // Можете использовать любую стратегию описанную выше.
//       // Если она не отработает корректно, то используейте `Embedded fallback`.
//       event.respondWith(networkOrCache(event.request)
//           .catch(() => useFallback()));
//   });
  
//   function networkOrCache(request) {
//       return fetch(request)
//         //   .then((response) => response.ok ? response : fromCache(request))
//           .catch(() => fromCache(request));
//   }
  
//   // Наш Fallback вместе с нашим собсвенным Динозавриком.
//   const FALLBACK = ""
//     //   '<div>\n' +
//     //   '    <div>Place-shop</div>\n' +
//     //   '    <div>you are offline</div>\n' +
//     //   '</div>';
  
//   // Он никогда не упадет, т.к мы всегда отдаем заранее подготовленные данные.
//   function useFallback() {
//       return Promise.resolve(new Response(FALLBACK, { headers: {
//           'Content-Type': 'text/html; charset=utf-8'
//       }}));
//   }
  
//   function fromCache(request) {
//       return caches.open(CACHE).then((cache) =>
//           cache.match(request).then((matching) =>
//               matching || Promise.reject('no-match')
//           ));
//   }
  