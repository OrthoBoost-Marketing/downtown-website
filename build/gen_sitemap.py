"""gen_sitemap.py - writes sitemap.xml for the 17-page tree.

Closes the Tier 3 audit finding "robots.txt names no sitemap", which had been open
because no sitemap existed at all.

Run it as part of the build, after the generators. It reads nothing from them: the URL
list below is explicit on purpose, so adding a page is a deliberate edit here rather
than a glob that silently picks up whatever happens to be in the directory.

DOMAIN IS PROVISIONAL. downtownorthodontics.ca is the domain in CLIENT-BRIEF.md, but the
stack question for this project is unresolved: the positioning brief specifies WordPress
plus Elementor, the client record says hosting is client-side, and what exists is static
on Vercel. If that resolves any way other than "this build goes live on
downtownorthodontics.ca", the loc values here are wrong. Confirm before submitting the
sitemap to Search Console.

Two pages are deliberately excluded:
  /404                                a 404 must never be in a sitemap
  /appointment-request-confirmation   a post-submit thank-you page. Indexing it puts a
                                      "thanks for booking" page in search results and
                                      lets people reach it without ever submitting,
                                      which also corrupts any conversion measurement
                                      keyed to that URL.

The legal pages ARE included. They are thin but real, and excluding them is what makes a
site look like it is hiding them.
"""
import datetime
import os

DOMAIN = "https://downtownorthodontics.ca"

# (path, priority, changefreq). Order is the order they appear in the file.
PAGES = [
    ("/",                      "1.0", "monthly"),
    ("/braces",                "0.9", "monthly"),
    ("/invisalign",            "0.9", "monthly"),
    ("/early-orthodontics",    "0.8", "monthly"),
    ("/retainers",             "0.8", "monthly"),
    ("/appointment-request",   "0.9", "monthly"),
    ("/dr-sam-daher",          "0.8", "monthly"),
    ("/why-choose-us",         "0.7", "monthly"),
    ("/reviews",               "0.7", "weekly"),
    ("/financing",             "0.8", "monthly"),
    ("/faq",                   "0.6", "monthly"),
    ("/contact",               "0.7", "monthly"),
    ("/privacy-policy",        "0.2", "yearly"),
    ("/terms",                 "0.2", "yearly"),
    ("/accessibility",         "0.2", "yearly"),
]

EXCLUDED = ["/404", "/appointment-request-confirmation"]


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    today = datetime.date.today().isoformat()

    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path, prio, freq in PAGES:
        out.append("  <url>")
        out.append("    <loc>%s%s</loc>" % (DOMAIN, path))
        out.append("    <lastmod>%s</lastmod>" % today)
        out.append("    <changefreq>%s</changefreq>" % freq)
        out.append("    <priority>%s</priority>" % prio)
        out.append("  </url>")
    out.append("</urlset>")
    out.append("")

    target = os.path.join(root, "sitemap.xml")
    with open(target, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(out))

    print("  wrote sitemap.xml   %d urls, %d excluded (%s)"
          % (len(PAGES), len(EXCLUDED), ", ".join(EXCLUDED)))


if __name__ == "__main__":
    main()
