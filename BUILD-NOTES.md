# Build notes — Downtown Orthodontics

Built 2026-08-24 from `CLIENT-BRIEF.md` using the `orthoboost-web:build-site` skill.
16 pages. The homepage layout was explicitly held constant.

## How the site is generated

Every page copies the homepage's `<style>` blocks, header, footer, mobile bar and JS
**verbatim**, by slicing `index.html` rather than re-authoring chrome. That machinery is
in `build/`:

| File | Job |
|---|---|
| `build/chrome.py` | Slices `index.html` for the shared chrome; `page()` assembles a full document. Also holds `LINKMAP`. |
| `build/common.py` | Shared page parts: page hero, CTA band, FAQ rows, checkmark lists. Import-safe. |
| `build/gen_appointment.py` | appointment-request + confirmation |
| `build/gen_services.py` | braces, invisalign, early-orthodontics, retainers |
| `build/gen_rest.py` | dr-sam-daher, why-choose-us |
| `build/gen_support.py` | financing, faq, contact |
| `build/gen_utility.py` | privacy-policy, terms, accessibility, 404 |

**To change chrome, edit `index.html` and re-run all five generators.** Do not hand-edit
a generated page; the next run overwrites it.

```bash
for g in gen_appointment gen_services gen_rest gen_support gen_utility; do python build/$g.py; done
```

HTML blocks use `__TOKEN__` placeholders rather than `%`-formatting, because the copy is
full of literal percent signs (`0%`, `5%`, `100%`) and escaping them all was a bug source.

## Decisions worth knowing

**The homepage nav now points at real pages.** It previously pointed at in-page anchors.
Only `href` values changed; **no layout changed**. The scroll-spy JS was widened from
`a[href^="#"]` to accept `/#anchor` so the homepage keeps its active-nav highlight.

**The conversion path came home, and this supersedes an earlier interim decision.**
On 2026-08-24 Jules chose to keep the homepage CTA pointing at
`downtownorthodontics.ca/appointment-request/` on the client's existing WordPress site,
*because no appointment page existed to point at*. One does now, so every CTA sitewide
routes to `/appointment-request`. **Zero links to the old site remain.** If that is not
wanted, it is a one-line revert in `index.html` plus `chrome.py`'s `LINKMAP`.

**Footer legal links now exist**, which closes the Tier 2 "footer missing accessibility
link" finding that had been open since the first audit. It was blocked only on the pages
not existing.

**`cleanUrls: true`** is set in `vercel.json`, so `braces.html` serves at `/braces`.
Every internal link is written extensionless. Retrofitting this touched every file on
Siouxland, which is why it was set before the pages were generated.

**Pages deliberately NOT built**, per the skill's own derivation rules:
- **No reviews page.** Review count unknown and no verbatim quotes on file.
- **No team page.** The client supplies no bios or headshots. A short team block sits on
  `/why-choose-us` instead, with the gap flagged on the page.
- **No location pages.** Single office, so the city stays in the homepage H1.
- **No doctor hub.** Single doctor.
- **A standalone FAQ page ships** even though the practice is not education-heavy: eight
  client-voiced Q&As already existed and the client's own sitemap asks for `/faq`.

## Placeholders on the site, all visible

The brief lists these as `TBD`, so they ship as marked placeholders rather than invented
content. Each renders in the dashed `.slot` style so nobody mistakes it for copy.

1. **Review quotes**, on `/appointment-request`, `/financing` and all four service pages.
   The specs require a real quote beside the form; none exists. **Biggest content gap.**
2. **Dr. Daher's personal story**, on `/dr-sam-daher`. `DOCTOR-PAGE-SPEC` wants story
   before credentials: the origin, what shaped the conservative approach, and 60 words on
   life outside the practice. None is on file, and this build does not invent biography.
3. **Team introductions**, on `/why-choose-us`.
4. **Before/after cases**, on the homepage, still on-brand placeholder panels.
5. **Legal pages** carry a standing "sample text, not legal advice" notice and bracketed
   `[TO CONFIRM]` items. They need the practice's counsel and its own answers on
   processors, retention periods and cancellation policy.

## Forms are built but NOT wired

Three forms ship: the appointment request, one per service page, and a general-enquiry
form on `/contact`. All carry the standard hidden UTM and click-id set. **None posts
anywhere** — `action=""` — because no GoHighLevel webhook URL is on file. Finish with
`orthoboost-ghl-forms` then `orthoboost-leads-connect`; every site gets both.

Form rules honoured: 4 fields plus one pre-filled interest select, never six. Zero PHI.
The only `<textarea>` on the site is the contact page's general-enquiry box, which is the
one permitted exception. Inputs are 46px at 16px font so iOS does not zoom.

## Audit results, 2026-08-24

Static sweep across all 16 pages: **no findings.** Every internal link resolves and is
extensionless, no bare `href="#"`, no broken same-page anchors, no missing images, every
`<img>` has alt, titles and descriptions unique per page, canonicals match slugs, no
banned `AggregateRating` or `Review` markup, no form over five visible fields.

Measured over HTTP in headless Chrome at 390 / 768 / 1440 / 2560px: **all 16 pages clean.**
No horizontal overflow anywhere, content caps at 1200px, mobile action bar present below
900px, no broken images, no input under 46px or under 16px font.

**Two false-positive classes were found and corrected in the checking script, not the
site.** A 44px control lays out at 43.996, so a strict `< 44` flagged every correct
button; and desktop header nav text links measure 28–31px but collapse into the drawer at
mobile widths, where the 44px touch rule applies. The heuristic held again: a finding on
nearly every page is the check, not the site.

## Still open at launch

- The six audit items from the homepage report, unchanged.
- Wire the forms (GHL + leads backup), then set the confirmation page as the conversion
  goal in Ads, GA4 and Meta.
- Drop `noindex` and the `robots.txt` Disallow **together**, and only at launch. Utility
  pages keep `noindex` permanently.
- Tailwind and anime.js still load from CDNs. Compile and self-host before PageSpeed.
- Attorney review of the three legal pages.
- **The stack conflict is still unresolved.** The brief names WordPress + Elementor +
  RankMath Pro; this is static on Vercel; registrar is CloudFlare. Settle before cutover.
- Three Dr. Ty rulings from the homepage audit.
