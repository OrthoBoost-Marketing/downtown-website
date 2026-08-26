"""post_media.py — the last build step. Run AFTER the gen_*.py scripts.

Two jobs, both idempotent:

  1. loading="lazy" + decoding="async" on every image and iframe that is NOT in the first
     viewport. "First viewport" is defined by the page's own <link rel="preload" as="image">
     (the LCP element) plus the brand logo, which sits in the sticky header on every page.
     Lazy-loading an LCP image delays it, which is why the exemption is data-driven rather
     than eyeballed.

  2. fetchpriority="high" on that preloaded hero image, so the browser does not queue it
     behind the stylesheet.

Image width/height come from the kit's own script and are NOT duplicated here:

    python "$KIT/plugin/skills/static-site-deploy/scripts/add_img_dims.py" .

Safe here because index.html sets `img { max-width: 100%; height: auto; }`, so the
attributes act as a pure aspect-ratio hint and cannot distort anything.
"""
import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

IMG = re.compile(r"<img\b[^>]*>", re.I)
IFRAME = re.compile(r"<iframe\b[^>]*>", re.I)
SRC = re.compile(r"""\bsrc\s*=\s*["']([^"']+)["']""", re.I)
PRELOAD = re.compile(r"""<link[^>]*rel=["']preload["'][^>]*as=["']image["'][^>]*>""", re.I)
HREF = re.compile(r"""\bhref\s*=\s*["']([^"']+)["']""", re.I)
HAS_LOADING = re.compile(r"\bloading\s*=", re.I)
HAS_DECODING = re.compile(r"\bdecoding\s*=", re.I)
HAS_FETCHPRI = re.compile(r"\bfetchpriority\s*=", re.I)


def eager_srcs(html):
    """Images that must load immediately: the preloaded LCP image, and the logo."""
    out = set()
    for link in PRELOAD.findall(html):
        m = HREF.search(link)
        if m:
            out.add(m.group(1))
    return out


def process(path):
    html = io.open(path, encoding="utf-8").read()
    before = html
    eager = eager_srcs(html)
    counts = {"lazy": 0, "eager": 0, "iframe": 0}

    def fix_img(m):
        tag = m.group(0)
        src_m = SRC.search(tag)
        src = src_m.group(1) if src_m else ""
        is_eager = src in eager or "Logo_" in src

        if is_eager:
            # Never lazy. Give the LCP image an explicit high priority.
            if src in eager and not HAS_FETCHPRI.search(tag):
                tag = tag[:-1].rstrip() + ' fetchpriority="high">'
                counts["eager"] += 1
            return tag

        add = ""
        if not HAS_LOADING.search(tag):
            add += ' loading="lazy"'
        if not HAS_DECODING.search(tag):
            add += ' decoding="async"'
        if not add:
            return tag
        counts["lazy"] += 1
        return tag[:-1].rstrip() + add + ">"

    def fix_iframe(m):
        tag = m.group(0)
        if HAS_LOADING.search(tag):
            return tag
        counts["iframe"] += 1
        return tag[:-1].rstrip() + ' loading="lazy">'

    html = IMG.sub(fix_img, html)
    html = IFRAME.sub(fix_iframe, html)

    if html != before:
        io.open(path, "w", encoding="utf-8", newline="").write(html)
    return counts


def main():
    pages = sorted(ROOT.glob("*.html"))
    if not pages:
        sys.exit("no .html files found in %s" % ROOT)
    total = {"lazy": 0, "eager": 0, "iframe": 0}
    for p in pages:
        c = process(p)
        for k in total:
            total[k] += c[k]
        if any(c.values()):
            print("  %-38s lazy %2d  hero %d  iframe %d"
                  % (p.name, c["lazy"], c["eager"], c["iframe"]))
    print("\n%d pages · %d images lazied · %d hero images prioritised · %d iframes lazied"
          % (len(pages), total["lazy"], total["eager"], total["iframe"]))


if __name__ == "__main__":
    main()
