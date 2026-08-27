"""Chrome extractor + page assembler for the Downtown Orthodontics site.

Every page copies the homepage's <style> blocks, header, footer, mobile bar and JS
VERBATIM. Nothing here re-authors chrome: it slices index.html and re-emits it, so a
change to the homepage's chrome propagates by re-running the generators.

Run generators from the site root:  python build/gen_<page>.py
"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(ROOT, "index.html")

DOMAIN = "https://downtownorthodontics.ca"

# ---------------------------------------------------------------- indexing
# THE CUTOVER SWITCH. True means every page is noindex, because this build is served from a
# vercel.app staging URL and must not compete with the live domain. Set it False at cutover,
# and at the same time delete robots.txt, which carries its own blanket "Disallow: /".
#
# Pages that must stay noindex AFTER launch do NOT rely on this: they pass noindex=True to
# page() individually, so flipping this switch cannot accidentally expose them. Those are
# the four utility pages (privacy-policy, terms, accessibility, 404) and the appointment
# confirmation page, which is a thank-you page and has no business in search results.
#
# Until 2026-08-27 this switch did not exist and the noindex parameter below was accepted
# but never read, so neither half of this was actually possible.
REVIEW_BUILD = True

# Photographs ship twice: the client's full-resolution original in assets/photos/,
# and an 880px-wide derivative in assets/photos/w880/ built by build/make_w880.py.
# Every slot on the site displays at ~440px CSS or less, so 880px covers a 2x DPR
# exactly and the originals were shipping 3-6x more bytes than any slot could use.
# disp() is the display path; og:image and JSON-LD "image" keep the original, which
# is why the originals stay on disk.
def disp(photo):
    """assets/photos/x.jpg -> assets/photos/w880/x.jpg"""
    assert photo.startswith("assets/photos/") and "/w880/" not in photo, photo
    return photo.replace("assets/photos/", "assets/photos/w880/", 1)

# ---------------------------------------------------------------- chrome slices
_src = io.open(INDEX, encoding="utf-8").read()

def _between(start_marker, end_marker, src=None, inclusive=True):
    s = src if src is not None else _src
    i = s.index(start_marker)
    j = s.index(end_marker, i) + (len(end_marker) if inclusive else 0)
    return s[i:j]

# all four <style> blocks, in order, byte for byte
STYLES = "".join(
    m.group(0) for m in re.finditer(r"<style[^>]*>[\s\S]*?</style>", _src)
)

FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com" />\n'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />\n'
    '<link href="https://fonts.googleapis.com/css2?family=Nunito:ital,wght@0,200;0,300;0,400;0,500;0,600;0,700;0,800;1,200;1,300;1,400&display=swap" rel="stylesheet" />'
)

ICONS = (
    '<link rel="icon" type="image/png" sizes="48x48" href="/assets/downtown-orthodontics-favicon-48.png" />\n'
    '<link rel="apple-touch-icon" sizes="180x180" href="/assets/downtown-orthodontics-apple-touch-icon-180.png" />'
)

# TIER 4 fix: the tailwind.config block lived only in index.html, so on the other 16
# pages every brand utility (bg-petrol-deep, text-teal, border-line, shadow-soft)
# generated nothing - which painted financing.html's counters section white on white.
# It is chrome now, sliced from index.html like everything else.
TW_CONFIG = _between("<script>\n  tailwind.config", "</script>")

# Both runtime libraries are VENDORED under assets/vendor/ (see assets/vendor/README.md
# for source URLs, pinned versions and the refresh commands). No third-party request is
# made at page load any more; only Google Fonts stays remote, deliberately.
# tailwind.min.js is the browser JIT build (Tailwind 3.4.17), byte-identical to what the
# Tailwind Play CDN served, so TW_CONFIG above is still read at runtime exactly as
# before. Load order matters: the JIT script first, then the config it reads.
# Paths are root-relative to match the head's other local assets (ICONS, og:image,
# preload) and so they resolve identically from a nested URL under vercel cleanUrls.
TAILWIND = ('<script src="/assets/vendor/tailwind.min.js"></script>\n' + TW_CONFIG)
ANIME = '<script src="/assets/vendor/anime.iife.min.js"></script>'

ANNOUNCE = _between('  <!-- ANNOUNCEMENT', "  </div>\n", inclusive=True)
HEADER = _between('  <header class="nav">', "  </header>\n")
FOOTER = _between("  <footer>", "  </footer>\n")
MBAR = _between('  <nav class="mbar"', "  </nav>\n")
DRAWER = _between('  <!-- MOBILE DRAWER', "  <!-- /MOBILE DRAWER -->\n")
SCRIPTS = _between("  <script>\n", "  </script>\n")

# The homepage's own in-page anchors become real destinations sitewide. This changes
# hrefs only; no chrome layout changes. See BUILD-NOTES.md.
LINKMAP = {
    'href="#top"': 'href="/"',
    'href="#paths"><b>Braces, clear &amp; metal</b>': 'href="/braces"><b>Braces, clear &amp; metal</b>',
    'href="#paths"><b>Kids &amp; early care</b>': 'href="/early-orthodontics"><b>Kids &amp; early care</b>',
    'href="#paths"><b>Invisalign &amp; Quick 6 Fix</b>': 'href="/invisalign"><b>Invisalign &amp; Quick 6 Fix</b>',
    'href="#faq"><b>Retainers &amp; aftercare</b>': 'href="/retainers"><b>Retainers &amp; aftercare</b>',
    'href="#qa"><b>Common questions</b>': 'href="/faq"><b>Common questions</b>',
    'href="#how">How it works</a>': 'href="/#how">How it works</a>',
    'href="#doctor">Meet Dr. Daher</a>': 'href="/dr-sam-daher">Meet Dr. Daher</a>',
    'href="#financing">Pricing</a>': 'href="/financing">Pricing</a>',
    'href="#visit">Visit</a>': 'href="/contact">Visit</a>',
    'href="#book"><span class="cta-lg">': 'href="/appointment-request"><span class="cta-lg">',
    'href="#book">Book yours': 'href="/appointment-request">Book yours',
    'href="#paths">Braces, clear &amp; metal</a>': 'href="/braces">Braces, clear &amp; metal</a>',
    'href="#paths">Kids &amp; early care</a>': 'href="/early-orthodontics">Kids &amp; early care</a>',
    'href="#paths">Invisalign &amp; Quick 6 Fix</a>': 'href="/invisalign">Invisalign &amp; Quick 6 Fix</a>',
    'href="#faq">Retainers &amp; aftercare</a>': 'href="/retainers">Retainers &amp; aftercare</a>',
    'href="#doctor">Meet Dr. Daher</a>': 'href="/dr-sam-daher">Meet Dr. Daher</a>',
    'href="#how">How it works</a>': 'href="/#how">How it works</a>',
    'href="#visit">Visit us</a>': 'href="/contact">Visit us</a>',
    'href="#qa">Questions</a>': 'href="/faq">Questions</a>',
    'href="#book">': 'href="/appointment-request">',
    # TIER 2 requires Privacy, Terms and a Web Accessibility Statement in the footer.
    # These were plain text because the pages did not exist; the build creates them.
    '<span>Concept mockup &middot; Privacy &middot; Terms</span>':
        '<span class="foot-legal"><a href="/contact">Contact</a>'
        '<a href="/privacy-policy">Privacy Policy</a>'
        '<a href="/terms">Terms &amp; Conditions</a>'
        '<a href="/accessibility">Accessibility Statement</a></span>',
}

def relink(html):
    for a, b in LINKMAP.items():
        html = html.replace(a, b)
    return html

HEADER_X = relink(HEADER)
FOOTER_X = relink(FOOTER)
ANNOUNCE_X = relink(ANNOUNCE)
MBAR_X = relink(MBAR)
DRAWER_X = relink(DRAWER)

# ---------------------------------------------------------------- page assembly
def head(title, desc, slug, noindex=False, preload=None, schema=None, og_image=None):
    canon = DOMAIN + "/" if slug == "" else DOMAIN + "/" + slug
    img = og_image or "/assets/photos/dt-7.jpg"
    out = [
        "<!doctype html>",
        '<html lang="en-CA">',
        "<head>",
        '<meta charset="utf-8" />',
        '<meta name="viewport" content="width=device-width, initial-scale=1" />',
        "<title>%s</title>" % title,
        '<meta name="description" content="%s" />' % desc,
    ]
    # Two independent reasons to be noindex: the whole build is in review, or this
    # particular page is never meant to be indexed. Either one is enough.
    if REVIEW_BUILD or noindex:
        out.append('<meta name="robots" content="noindex, nofollow" />')
    else:
        out.append('<meta name="robots" content="index, follow" />')
    out += [
        '<link rel="canonical" href="%s" />' % canon,
        '<meta property="og:type" content="website" />',
        '<meta property="og:site_name" content="Downtown Orthodontics" />',
        '<meta property="og:locale" content="en_CA" />',
        '<meta property="og:title" content="%s" />' % title,
        '<meta property="og:description" content="%s" />' % desc,
        '<meta property="og:url" content="%s" />' % canon,
        '<meta property="og:image" content="%s%s" />' % (DOMAIN, img),
        '<meta name="twitter:card" content="summary_large_image" />',
        ICONS,
    ]
    if preload:
        out.append('<link rel="preload" as="image" href="%s" fetchpriority="high" />' % preload)
    out.append(FONTS)
    if schema:
        out.append('<script type="application/ld+json">\n%s\n</script>' % schema)
    out.append(TAILWIND)
    out.append(ANIME)
    out.append(STYLES)
    out.append("</head>")
    return "\n".join(out)


def page(title, desc, slug, body, noindex=False, preload=None, schema=None, og_image=None):
    return "\n".join([
        head(title, desc, slug, noindex, preload, schema, og_image),
        "<body>",
        ANNOUNCE_X,
        "\n  <!-- NAV -->",
        HEADER_X,
        DRAWER_X.rstrip(),
        body.rstrip(),
        "\n  <!-- FOOTER -->",
        FOOTER_X,
        SCRIPTS,
        MBAR_X.rstrip(),
        "</body>",
        "</html>",
        "",
    ])


def write(filename, html):
    path = os.path.join(ROOT, filename)
    io.open(path, "w", encoding="utf-8", newline="").write(html)
    print("  wrote %-38s %6d bytes" % (filename, len(html.encode("utf-8"))))
