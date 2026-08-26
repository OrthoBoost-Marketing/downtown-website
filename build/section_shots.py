"""Build one screenshot page per homepage section, for visual review.

Scrolling a headless capture is unreliable: --screenshot fires at the load event, and a
scroll issued from a load handler (especially inside an iframe) does not always land. A tall
window is worse, because every vh unit then resolves against that height and the hero
balloons. So instead of scrolling to a section, each page HIDES the other sections. The
header stays, the target section sits directly beneath it, and vh resolves against a normal
900px viewport.

Entrance animations are also disabled: .reveal starts at opacity .01 WITH a 5px blur, and
headings animate per word via .hw spans, so an un-overridden capture shows blank bands.

Writes __sec-<id>.html files. They are throwaway; delete before committing.
"""
import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SECTIONS = ["paths", "doctor", "credentials", "financing", "reviews", "same-doctor",
            "ready", "faq", "visit", "book"]

OVERRIDE = """
<style id="shot-override">
  /* every entrance state off: opacity, transform, blur, per-word heading spans */
  .reveal, .reveal.in, .hw, .hero-mask > span, .hero-actions, .hero-cred, .split {
    opacity: 1 !important; transform: none !important; filter: none !important;
    visibility: visible !important; clip-path: none !important; transition: none !important;
  }
  /* isolate the section under test */
  body > section, body > .creds, body > .hero-screen, body > footer, body > .mbar { display: none !important; }
  body > #__T__, body > header { display: block !important; }
</style>
"""


def main():
    src = io.open(ROOT / "index.html", encoding="utf-8").read()
    ids = set(re.findall(r'<section[^>]*id="([^"]+)"', src))
    made = []
    for sec in SECTIONS:
        if sec not in ids:
            print("  skip %-14s (no section with that id)" % sec)
            continue
        out = src.replace("</head>", OVERRIDE.replace("__T__", sec) + "</head>", 1)
        # lazy images never load without a scroll, and an unloaded image collapses its box
        out = out.replace(' loading="lazy"', "")
        p = ROOT / ("__sec-%s.html" % sec)
        io.open(p, "w", encoding="utf-8", newline="").write(out)
        made.append(p.name)
        print("  wrote %s" % p.name)
    print("\n%d pages. Capture each at 1265x900, then delete the __sec-*.html files."
          % len(made))
    return 0


if __name__ == "__main__":
    sys.exit(main())
