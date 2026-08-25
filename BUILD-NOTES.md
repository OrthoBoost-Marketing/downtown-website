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
- **No reviews page — but this is now unblocked and worth revisiting.** It was skipped
  because the count was unknown and no quotes existed. Both changed on 2026-08-24: the
  profile carries **160 reviews at 4.4**, which is well past the kit's rough 40+ threshold
  for a standalone reviews page. Not built, because it was not asked for. Flagged.
- **No team page.** The client supplies no bios or headshots. A short team block sits on
  `/why-choose-us` instead, with the gap flagged on the page.
- **No location pages.** Single office, so the city stays in the homepage H1.
- **No doctor hub.** Single doctor.
- **A standalone FAQ page ships** even though the practice is not education-heavy: eight
  client-voiced Q&As already existed and the client's own sitemap asks for `/faq`.

## Marquees are permitted here (house rule, 2026-08-24)

**The kit's blanket "no carousels or sliders" rule is nullified for this site**, on Jules's
call, provided all three conditions hold. Do not report a marquee as an audit finding on
Downtown Orthodontics while they do:

1. **Tap, click, hover or focus pauses it**, and there is a real `<button>` pause toggle
   with `aria-pressed`.
2. **It drags on desktop and on mobile.**
3. **Everything inside stays visible to Google.**

The implementation is the reusable `.mq` component in the homepage stylesheet plus its
controller in the shared script block. It is a genuinely scrollable region
(`overflow-x:auto`), not a CSS transform, which is what makes native touch drag, momentum
and keyboard arrow scrolling work for free.

How each condition is met, and what it cost to get right:

- **Pause.** `pointerenter`/`focusin` pause; `pointerdown` holds. Desktop taps toggle via
  the pointer path. **Touch needed its own `touchstart`/`touchend` path**, because when the
  browser takes over a touch gesture for native panning it fires `pointercancel`, not
  `pointerup`, so pointer-based tap detection is unreliable on a phone.
- **Drag.** Mouse and pen are driven by the pointer handlers. Touch is native.
  `touch-action` must be **`pan-x pan-y`**; setting it to `pan-y` hands horizontal
  gestures to JS, and since the JS handler deliberately skips touch, that silently killed
  touch dragging altogether.
- **SEO.** All twelve review cards and all eight credential items sit in the static HTML
  and are **never `display:none` at any breakpoint** (verified at 320, 390, 768, 1440 and
  2560). The seamless loop is built from **JS-injected `aria-hidden` clones**, so crawlers
  see each item exactly once and there is no duplicate content. The old implementation was
  worse on both counts: it hid whole columns below 880px and 560px, and shipped
  `aria-hidden` duplicates in the markup.
- **Sub-pixel trap, worth remembering.** `track.scrollLeft += 0.35` does nothing:
  `scrollLeft` snaps to integers, so a sub-pixel increment is discarded every frame and the
  strip never moves. Accumulate the position in a JS variable and assign it whole, and
  resync that accumulator whenever the user drags, flicks or keys the strip.
- `prefers-reduced-motion` stops the auto-scroll entirely; it stays a draggable region.

## Reviews are real as of 2026-08-24

Pulled from the practice's live Google Business Profile: **4.4 out of 5 from 160 reviews**,
with twelve quotes running verbatim in the homepage marquee. The rating is **text only and
deliberately not marked up** as `AggregateRating`. No star glyphs sit beside the 4.4 either,
because five solid stars next to a 4.4 misrepresents it.

Per-page quote slots on the service, appointment and financing pages are **still visible
placeholders** — each wants a topic-matched quote, and assigning them is a content decision.

## Placeholders on the site, all visible

The brief lists these as `TBD`, so they ship as marked placeholders rather than invented
content. Each renders in the dashed `.slot` style so nobody mistakes it for copy.

1. **Per-page review quotes**, on `/appointment-request`, `/financing` and all four service
   pages. Real reviews now exist and run on the homepage; these slots need a topic-matched
   quote assigned to each page.
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
