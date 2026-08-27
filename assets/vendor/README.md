# assets/vendor

Third-party runtime libraries, vendored. These are NOT our code. They were previously
loaded from public CDNs on every page; they are served from this origin now so the site
makes no third-party request at page load.

Google Fonts (Nunito) is deliberately still remote. Do not vendor it.

Both files are referenced from `build/chrome.py` (constants `TAILWIND` and `ANIME`) and,
for the homepage, from `index.html` directly. `chrome.py` holds the script tags as
literals rather than slicing them out of `index.html`, so if you change one you must
change the other or the homepage and the other 16 pages will disagree.

Paths in the generated HTML are root-relative (`/assets/vendor/...`), matching the head's
other local assets, so they resolve the same from any URL depth under Vercel `cleanUrls`.

---

## tailwind.min.js

- Source URL: https://cdn.tailwindcss.com
- Pinned version: Tailwind CSS **3.4.17** (the CDN root 302-redirects to `/3.4.17`)
- Downloaded: 2026-08-27
- Byte size: 407,279 bytes

This is the **browser JIT build**, not a compiled stylesheet. It scans the DOM at runtime
and reads the inline `tailwind.config` object that `chrome.py` injects right after it, so
it cannot be swapped for a plain `.css` file without also compiling a real Tailwind
config. Replacing it with a compiled stylesheet is a separate piece of work.

Refresh:

```
curl -sL -o assets/vendor/tailwind.min.js https://cdn.tailwindcss.com/3.4.17
```

## anime.iife.min.js

- Source URL: https://cdn.jsdelivr.net/npm/animejs@4/lib/anime.iife.min.js
- Pinned version: anime.js **4.1.4** (from the file's own `@version` banner)
- Downloaded: 2026-08-27
- Byte size: 83,975 bytes

Note on the version: the old `@4` URL is a semver range, and jsdelivr resolves `animejs@4`
to 4.5.0 today, but 4.5.0 no longer ships `lib/anime.iife.min.js` at all, so the range URL
was falling back to 4.1.4. That is one more reason this is vendored: the URL the site used
to depend on can stop resolving without warning. Moving past 4.1.4 means picking a new
entry point from the package, not just bumping the number.

Refresh (pinned, and this exact URL is what was downloaded, byte for byte):

```
curl -sL -o assets/vendor/anime.iife.min.js https://cdn.jsdelivr.net/npm/animejs@4.1.4/lib/anime.iife.min.js
```
