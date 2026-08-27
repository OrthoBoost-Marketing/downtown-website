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
for g in gen_appointment gen_services gen_rest gen_support gen_utility gen_reviews; do
    python build/$g.py
done
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

## Nav follows HEADER-SPEC (restructured 2026-08-25)

Five top-level items, which is the spec shape `Services / Why / Resources / Locations`
adapted for a single-office affordability practice:

**Treatments ▾** (the four money pages) · **Why us ▾** (Meet Dr. Daher, Why the specialist)
· **Pricing** · **Resources ▾** (Common questions, How it works, Contact us) ·
**Our address** · one `tel:` · one primary CTA.

What was wrong before, and why each move follows a rule:

- **`/why-choose-us` was orphaned**, linked from nowhere on the site. Rule 4 makes the
  Why-Us dropdown mandatory and puts **Meet the Doctor** in it as non-negotiable, the
  second most-visited page. Both now live there, and Why choose us is also in the footer.
- **The FAQ was inside the services dropdown.** Rule 3 says that dropdown is money pages
  only; rule 5 puts patient-utility items in Resources. The FAQ, How it works and Contact
  moved there.
- **"Visit" became "Our address"** anchoring the homepage map section, which is what rule 8
  specifies for a single location. A `Locations ▾` dropdown is for multi-office only.
- **Pricing keeps its promoted top-level slot** under rule 9, because this practice is
  positioned on affordability.
- "Treatments" is kept over "Services": nav label wording is explicitly in the spec's
  avatar flex layer, and it is the word the client's own site and Maya use.

Verified: 5 top-level items, exactly one `tel:`, exactly one primary CTA, zero social
icons, and the mobile drawer mirrors the desktop nav.

## Homepage now has every section Dr. Ty calls for (2026-08-25)

> **Heading corrected 2026-08-26.** This previously read "now match Dr. Ty's called-for
> **order**", which was an overclaim: the work below added the missing section *types*, and
> never touched sequence. The homepage does **not** run in the kit's order. See
> "Homepage section order does not match the kit" below for the actual diff.

The kit's homepage order is header → hero → trust bar → meet the doctor → **USP zigzag** →
CTA band → **authority logos** → reviews → services grid → locations → footer. Two of
those were missing and two existing sections were doing jobs the kit does not ask for.

**Authority logo bar added** inside the credentials section, per `AUTHORITY-LOGOS-SPEC`.
Four cells, one quiet label, muted to a single tone, wrapping to 2 columns at 390px with
marks at 30px. **Not a marquee**: rule 6 bans a scroller in this section and carousels are
in its banned list, so the site's marquee allowance does not extend here.

Only genuinely held credentials appear, each cell naming the actual relationship:

| Cell | Treatment | Relationship |
|---|---|---|
| Invisalign | Official Align file, muted to one tone at 85% | Scientific advisory board, top 1% provider |
| McGill University | Type only | Alma mater, McCutcheon award |
| Université de Montréal | Type only | Former associate professor |
| University of the Pacific | Type only | Former associate professor |

University marks stay **type only** deliberately: institutional logos are portal-gated and
cropping or recolouring them breaks the institutions' own brand standards.

**Marks deliberately absent, pending one confirmation from Maya:** an AAO or Canadian
Association of Orthodontists membership mark, Royal College of Dentists of Canada
certification, and **the Invisalign provider tier**. The practice's own Instagram bio says
"Blue Diamond" and its TikTok says "Platinum+", which contradict each other, and neither
came from the client. A Blue Diamond award is also visible on the shelf in the photo used
on the pricing row, so this is worth simply asking about.

**Two sections converted into the USP zigzag**, which the spec makes mandatory content for
an affordability avatar and which the homepage did not have:

- **"Specialist care, genuinely affordable"** was a four-counter animated band, which is a
  trust-bar pattern rather than a zigzag row. It is now the **pricing row** in the bulleted
  variant (the BrightWay pattern), with a real photo and a contextual text link to
  `/financing`. Never a button: booking lives in the header, hero and CTA band. The
  animated counters still live on `/financing`, which is where the money story belongs.
- **"What families ask first"** was a second FAQ block that duplicated the accordion below
  it, and it **attributed its questions to invented people** ("Sarah, from Yaletown,
  asks…"), which is a Tier 1 problem nobody had caught. It is now the **objection-killer
  row**, "Affordable never means an assembly line", running as the photo-free centred band
  variant the spec permits rather than reusing a third photograph or touching stock.

**"Accepting new patients" removed from the nav**, as asked.

The trust-bar requirement is satisfied by the hero chips, which `TRUST-BAR-SPEC` names as
an approved alternate placement. Worth knowing: the credentials marquee under the hero runs
8 items with tick icons, where that spec wants 3 to 5 cells and typography only. It is left
alone because the marquee is wanted, but it is a departure.

## Reviews are curated, not just real

Nine kept from the profile, down from twelve. Each one earns its place by proving a
specific claim the site makes, and generic praise was dropped however glowing, because
"so kind" and "fantastic staff" prove nothing a competitor could not also claim.

| Review | What it proves |
|---|---|
| **Lomish Bhangu** — turned down by one orthodontist, another had no real solution | "Complex and referred cases welcome". **The strongest proof on the whole profile.** |
| **Kim Patara** — original Invisalign in 2007, teeth have not shifted | Retention, and a result nobody else can claim |
| **Alex Bobylev** — repairing work done at a regular dentist, quicker and with less discomfort | Specialist versus general dentist, the site's central wedge |
| **Riaz Meghji** — "well worth the investment" | Handles the price objection |
| **S Ismail** — walks you through the plan, answers thoroughly | Clear treatment plan |
| **SassySips** — retainers, appointment the same day she called | Service speed, and retainer replacement |
| **Fiona Deng** — "Both of my kids like him a lot!" | Kids and family |
| **Dante Foreman** — scan, in and out quickly, info sent over | The free first visit |
| **Jayden Dinh** — happiest with the results, looked forward to the appointments | Completed treatment |

**Swapped 2026-08-26 (Tier 1 truth pass).** Iryna Ponomarenko and Skyla W were dropped
and replaced with Alex Bobylev and Jayden Dinh. Neither of the originals appears in
`build/reviews_data.py`, which is the recorded harvest and the only place verbatim text
plus a verified rating is stored, so their wording could not be checked word for word.
Every quote on the site now resolves to that file. Do not re-add a quote that is not in
it; harvest it into `reviews_data.py` first.

Do not pad this back out for the sake of a longer loop. The section lede was rewritten to
match what these reviews actually say, rather than the generic "the doctor and the
service" line that suited the placeholders.

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
4. **Legal pages** carry a standing "sample text, not legal advice" notice and bracketed
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

## Kit conformance audit, 2026-08-26 — nine fixes

Audited the homepage section by section against every `*-SPEC.md` in the kit (pulled to
`26b6370` first; the two new commits touched the deploy and forms skills, not the section
specs). Ten of the kit's eleven homepage sections were present, one was missing, and seven
of the present ones carried at least one deviation. Fourteen findings, nine closed here.

### F 01 — the services grid was an audience grid

"Three ways to begin" looked like Section 09 but was not one: its H3s were unsearchable
("The smile you finally make time for") and **all three cards pointed at
`/appointment-request`**, so `/braces`, `/invisalign`, `/early-orthodontics` and
`/retainers` had **no link from the homepage body at all** — only the nav dropdown and the
footer. Those four are each a keyword's SEO hub and an ad campaign's landing page.

Each card now opens its service page and leads with the searchable name. The layout did not
change. It stays at **three cards** because the spec allows 3, 6 or 9 and bans 4, so
`/retainers` — lowest demand of the four — is linked from the retainer FAQ answer instead.

### F 02 — the FAQ had no cost question, and the schema did not mirror the page

A cost + city question is mandatory and hiding it is named under Banned. Five questions ran
and none was about money, on an affordability-positioned practice.

Separately, and worse: **the FAQPage JSON-LD carried eight questions while five were
visible.** Cost, "age seven" and "I'm 40" were marked up but appeared nowhere on the page,
which is a structured-data mismatch. The block is now rebuilt from the six visible Q&As, in
order. The two that are not homepage content live properly on `/faq`, which has its own node.

### F 03 / F 04 — hours and directions

Hours were shipping in `openingHoursSpecification` only. They are client-confirmed, so they
now render in the locations card and the footer, identical in all three places. And **Get
directions**, which the spec calls the #1 action in that section, did not exist: booking held
the solid button for the fifth time on the page. Directions now takes the solid button and
booking steps down to the outline.

### F 05 — the doctor teaser used the one button its spec bans

Solid `Book with Dr. Daher`, where the spec allows exactly one ghost or outline CTA and lists
a second solid CTA under Banned. Now a single ghost `More about Dr. Daher` to the bio page;
the old `See the full record` link came out as the second CTA. A kicker carries the doctor's
full name, which previously survived only in the image alt.

**Trap:** the first version used `btn-outline`, which `.hero-actions .btn-outline` paints in
petrol (#313131) — near-black on the `.doc` section's near-black ground, contrast 1.6:1 and
effectively invisible. `btn-ghost-light` is the existing component for dark grounds. A guard
rule now catches any outline button dropped into `.doc` or `.ctaband`. This is the same bug
family as the black-on-black `.btn-primary` found on 2026-08-24.

### F 08 — the rating was in a comment

`4.4 out of 5 from 160 reviews` existed only in a source comment. It now runs as a rating
eyebrow, **text only, never `AggregateRating`**, with the door beneath the section and the
count line the spec allows when the count is strong. No `place_id` is on file, so the link is
the same Maps search URL the footer address uses.

### F 11 — the mid-page CTA band

The spec's default placement, directly after the USP zigzag, was empty; only the closing band
existed. Two bands now run, which is the maximum. **The first insertion landed in the wrong
place** because it anchored on a `(REAL QUESTIONS)` comment that was itself a leftover from
the FAQ-duplicate block converted to a zigzag row on 2026-08-25 — so the comment sat *before*
`#same-doctor` and put the band mid-zigzag. Both fixed; the orphan comment is gone.

### F 13 — media loading

`build/post_media.py` is the new **last build step** and must run after the generators:

```
for g in gen_appointment gen_services gen_rest gen_support gen_utility gen_reviews; do
    python build/$g.py
done
python "$KIT/plugin/skills/static-site-deploy/scripts/add_img_dims.py" .
python build/post_media.py        # LAST, because it repairs
```

**The order above is load bearing, and this file had it backwards until 2026-08-27.**
`post_media.py` must run AFTER the kit's `add_img_dims.py`, never before. The kit script
has a stray-solidus defect at its line 113 that writes new attributes after the closing
`/`, and `post_media.py` repairs that output. Reverse the two and 28 malformed tags come
back. See the docstring in `build/post_media.py`, which is the authority on this.

Both defects are now filed against the kit as
[PR 1](https://github.com/OrthoBoost-Marketing/orthoboost-website-kit/pull/1) (stop
producing it) and
[PR 2](https://github.com/OrthoBoost-Marketing/orthoboost-website-kit/pull/2) (repair what
exists). Until both merge, keep running `post_media.py` last.

It lazies every image and iframe *except* the page's own preloaded LCP image and the logo,
and adds `fetchpriority="high"` to that hero. The exemption is driven by each page's
`<link rel="preload">` rather than eyeballed, because lazy-loading an LCP image delays it.
`img { height: auto }` was added first, without which the kit's dimension attributes can
distort images.

**Kit bug worth a PR:** `add_img_dims.py` reports both brand logos as `MISSING` on every
page. It does not URL-decode `%20`, and the filenames contain a space. The files exist; the
logos simply get no dimensions, which costs nothing here since both are CSS-sized with
`width: auto`. Same defect class as the one already logged against `audit-site.mjs`.

### Verification

Twenty-two edits, each asserted to match exactly once before writing. Then 50 static checks
(section order, schema/page parity, link and asset resolution, button counts, tap targets)
plus a 16-page browser sweep at 390 and 1440: zero overflow, zero clipped elements, zero
sections rendering under 40px, footer hours on all 16, one H1 each. The only sweep hit at
1440 is the known desktop-nav false positive.

Three of the four first-run "failures" were the checking script, not the site: two matched
the word inside my own explanatory comments, and one demanded `class="revdoor"` where the
attribute is `"revdoor reveal"`. The fourth was real.

**Screenshot recipe, because two obvious approaches fail here.** A tall-window full-page
capture makes every `vh` unit resolve against that height, so the hero balloons to thousands
of pixels and every offset below it is wrong. And a scroll issued from a load handler does
not reliably land before `--screenshot` fires. `build/section_shots.py` sidesteps both: it
writes one throwaway page per section that *hides the other sections*, so the target sits
under the header at a normal 900px viewport. It also disables the entrance states — `.reveal`
starts at opacity `.01` **with a 5px blur**, and headings animate per word via `.hw` spans,
so an un-overridden capture shows blank bands. Delete the `__sec-*.html` files afterwards.

### Not fixed, and why

- **F 06** credentials stated three times (marquee, doctor chips, credentials section). The
  cross-section rule says drop the list from the doctor section; that is a content call on
  facts the client supplied, so it is proposed rather than done.
- **F 07** trust bar runs 8 iconed cells against a 3–5 typography-only rule. Jules's marquee
  ruling settled the scroller and nothing else. Needs a ruling.
- **F 09** reviews page, now warranted at 160 reviews (spec sizes 24–30 for high volume).
  Needs ~12 more reviews harvested.
- **F 10** authority band is 1 logo + 3 wordmarks. Blocked on Maya.
- **F 12** the before-and-after section still shows two gradient panels behind a handle, with
  a sub promising a transformation it cannot deliver. Blocked on consented cases.

## The reviews page, 2026-08-26 (17th page)

`REVIEWS-PAGE-SPEC`. The brief had derived *no reviews page* from "review count unknown and
no quotes"; both halves were false, so the page now exists with **28 reviews**, inside the
spec's 24 to 30 band for a high-volume practice.

### Every review is a verified five-star review, and here is how that was established

Google's review panel **exposes no accessible rating markup at all**: no `aria-label`, no
`title`, no schema, no numeric class. The stars are pure SVG with a grey base layer and no
readable gold overlay, so per-review ratings cannot be scraped. Reading them by eye, card by
card, would have cost dozens of screenshots.

What worked: **sort the panel by "Lowest rating" and read the ordered author list.** In that
order the transition to five-star lands exactly at "S Ismail", so the 28 authors before it
are the complete non-five-star set for this profile. That list is recorded in the header of
`build/reviews_data.py` and it is the reason **Atlas Hanen (4-star) was dropped** from the
candidates. Thirteen of the kept reviews were also spot-checked visually.

Do not add a review to that file without establishing its rating the same way.

### Harvesting notes, because this will be done again for other clients

- The panel is **virtualised**. Only 8 to 11 reviews exist in the DOM at a time.
- **Programmatic scrolling does not load more.** `scrollTop = scrollHeight`, synthetic
  `wheel` events and synthetic `scroll` events all leave the count unchanged. Only real
  input events do it: `computer` scroll actions at coordinates over the panel. Maps'
  own reviews pane refused to load past 8 by any method and had to be abandoned; the
  **Google *search* review dialog** (`#lrd=<hex>:<hex>,1,,,,`) is the one that paginates.
- Expand every truncated body by clicking each visible `More` first, then read
  `innerText` and strip the owner responses. Owner replies otherwise land inside the
  review text.
- Extract and stash results **immediately**. The user's tab closed twice mid-harvest and
  took the in-page working set with it.
- The tool's JS output is capped at roughly 1 kB, so long review bodies have to be pulled
  in slices; returning raw `outerHTML` is blocked outright as cookie-adjacent data.

### Schema: the one rule two of three reference sites get wrong

`Dentist` node **only**. No `AggregateRating`, no `Review` objects, anywhere on the page.
Marking up third-party reviews on your own site is self-serving, ineligible for rich
results, and a manual-action risk. The 4.4 is displayed prominently and marked up nowhere.

### Anatomy as built

Hero &rarr; aggregate band &rarr; skim layer &rarr; spotlight &rarr; masonry wall &rarr;
bridge &rarr; CTA band.

- **Skim layer** is a marquee of eight one-liners, permitted under the site's three house
  conditions and built from the homepage's own `.mq` component and shared controller, so it
  inherits tap/hover/focus pause, desktop and mobile dragging, and `touch-action: pan-x
  pan-y`. Every fragment also appears in full in a card below, so the marquee asserts
  nothing the wall does not. The seamless loop comes from **JS-injected `aria-hidden`
  clones**, so crawlers see each line exactly once.
- **Topic chips are Google's own review topics with Google's own counts**, read off the
  profile. Not our categories, and not editable without re-reading the profile.
- **Spotlight** is Sally Karimi: told by various professionals that jaw surgery was the only
  option, treated with Invisalign instead. It is the strongest proof on the profile for the
  conservative-treatment claim the rest of the site makes. Framed as one patient's account,
  because that is what it is.
- **Wall** is masonry via `column-count`, first 9 rendered and the other 18 shipped with
  `hidden` plus ~20 lines of vanilla load-more that only reveals nodes already in the
  document. Never JS-injected: that keeps all 28 crawlable and the page CLS-safe.

### Three defects caught while building it

1. **The homepage rating was already on the page.** A `.rating-line` block has displayed
   "4.4 out of 5, from 160 Google reviews" with the canonical `cid` link since 24 August.
   The 26 August audit finding claimed the rating "appears only in an HTML comment", which
   was **wrong**, and the rating eyebrow added on the strength of it made the score appear
   twice, then three times once the door's count line landed. Eyebrow reverted to a label,
   count line dropped. The rating now appears **once** in that section.
2. **`.rv-topics span` was too broad**, so it drew a pill around the section label and a
   second pill inside every chip. Scoped to `> span`.
3. **Star gold at `#d9a02b` is 2.33:1 on white**, under the 3:1 non-text minimum, and these
   stars carry meaning (`role="img"` with a label). Darkened to `#b07d10`, 3.63:1.

### Wiring

`HEADER-SPEC` rule 4 reserves a Why-Us slot for Reviews when the reviews are strong, so
the dropdown now carries it, and the footer Practice column does too. The homepage reviews
door points at `/reviews` rather than straight to Google; the reviews page carries the
outbound `cid` link itself.

Page CSS lives in the **shared stylesheet**, not a page-local `<style>`, so the
one-stylesheet-sliced-verbatim invariant the generators depend on still holds.

## Homepage section order does not match the kit (CLOSED 2026-08-26, see below)

> **Superseded.** The full reorder was approved and shipped the same day, in commit
> `c3f4180`. The spine now matches the kit exactly: 8 of 8 kit-consecutive pairs, zero
> inversions. The ledger below is kept because it is the measurement that justified the
> change, not because it still describes the page.

Measured, not assumed. The 26 August conformance audit laid its ledger out *in* kit order
and checked each section's **presence**; it never checked **position**. It should have.

| # | In `index.html` | Kit type | Kit wants it at |
|---|---|---|---|
| 1 | `header` | header | 1 |
| 2 | `#top` | hero | 2 |
| 3 | creds marquee | trust bar | 3 |
| 4 | `#paths` | **services grid** | **9** |
| 5 | `#doctor` | **meet the doctor** | **4** |
| 6 | `#credentials .authbar` | **authority logos** | **7** |
| 7 | `#financing` | **USP zigzag** | **5** |
| 8 | `#reviews` | reviews | 8 |
| 9 | `#same-doctor` | **USP zigzag** (row 2) | **5** |
| 10 | `#ready` | **CTA band** | **6** |
| 11 | `#visit` | locations | 10 |
| 12 | `#book` | CTA band, the permitted repeat | 6 |
| 13 | `footer` | footer | 11 |

**Nine of thirteen are in correct relative order.** The frame is right: header, hero and
trust bar open the page, and locations, closing band and footer close it. The middle is
shuffled, in three ways:

1. **The services grid is five slots too early.** It sits at 4, directly after the trust
   bar, where the kit puts it at 9, after reviews. This is the largest single displacement,
   and it changes what the page is: an audience directory up front rather than after the
   proof has been made.
2. **Meet the doctor falls after the services grid** rather than immediately after the
   trust bar, so the "who will treat you" answer arrives later than the kit intends.
3. **The CTA band, authority logos and reviews are interleaved.** Kit: zigzag → CTA band →
   authority logos → reviews. As built: authority logos → zigzag row 1 → reviews → zigzag
   row 2 → CTA band. The **zigzag is also not contiguous**: its two rows straddle reviews.

Five further sections sit between these and belong to no kit type (`#how`, `#results`,
`#why-specialist`, the bento, `#faq`). The kit does not ban extras, and they are not the
reason the order diverges.

**Was not fixed at the time, because reordering the homepage is exactly the "significant
layout change" that was ruled out on 2026-08-25.** Jules then approved the full reorder on
2026-08-26 after seeing that the kit's own reference build follows the canonical order
literally. Shipped in `c3f4180`. It is a sequencing decision, not a defect in any single
section. Options, cheapest first:

- **Leave it**, and record the deviation. The page reads well and every section is present.
- **Two moves** buy most of the conformance: `#paths` down to after `#reviews`, and
  `#doctor` up to directly after the trust bar. That fixes displacements 1 and 2 and leaves
  everything else alone.
- **Full reorder**, which additionally merges the two zigzag rows into a contiguous block
  and moves `#ready` ahead of the authority bar. Most conformant, largest change.

## Homepage trimmed and partly reordered (2026-08-26, Jules)

**Two block moves toward the kit order.** Nothing inside either section changed.

- `#doctor` → directly after the trust bar (kit position 4). "Who will actually treat you"
  now lands before anything is asked of the reader.
- `#paths` (services grid) → directly after `#reviews` (kit position 9). The page makes its
  case before it hands over a directory.

Kit-consecutive pairs respected went **3 of 10 to 5 of 10**, and positions 1 to 4 now match
the kit exactly. The coarse "in relative order" count stays 9 of 13, because the remaining
inversions are the ones only a full reorder fixes: the authority bar sits ahead of the
zigzag, and zigzag row 2 trails after the services grid.

`#same-doctor` lost its `--surface` inline background and takes `--bg`, so reviews, paths
and same-doctor do not run three identical tints in a row.

**Photo consequence of the doctor move, flagged in the markup and not solved:** the hero
uses `dt-7.jpg` and the doctor section uses `dt-6.jpg`, near-identical frames from the same
shoot. Four sections used to separate them; now they are adjacent and read as a duplicate.
Shuffling the existing set does not fix it, because `img-3127.jpg` is the only other
Dr. Daher shot and it carries the adults service card. **Fix with the Aug 12 shoot:** one
more portrait in different surroundings, or a doctor-with-patient frame for the hero, which
is `HERO-SPEC`'s first-priority subject anyway.

**Before-and-after section removed** (audit F 12). Two gradient placeholder panels behind a
drag handle, a sub promising "the kind of transformation we create", and a caption admitting
they were placeholders. It mapped to no kit section type. Its slider driver and its
"drag me" hint IIFE came out of the script block too: both guarded on the element existing,
so they were harmless, but dead code that looks live is how a section gets reintroduced.

**One CTA band, and it moved to the mid-page slot.** `#ready`, the dark band added earlier
the same day for audit F 11, was removed, and the existing closing band (`#book`) was moved
up from before the footer into `CTA-BAND-SPEC`'s default slot directly after the USP zigzag.
The page now ends on the locations map.

Jules's call, made with the trade-off stated: there is no closing ask before the footer. Two
things already in place soften it, and both were measured rather than assumed: **two real
booking links still follow the band** (one in the locations card, one further down) and the
**mobile sticky bar** carries Call, Book and Directions on every screen. The spec's optional
"repeat near page bottom" is therefore unused; running a single band in the default slot is
conformant, and it is the bottom-of-page repeat that is now absent by choice.

Verified after both removals: no console errors, script and section tags balanced, brace and
paren counts balanced in the sliced script block, and all 17 pages clean at 390 and 1440
with zero overflow, zero clipped elements and zero sections under 40px.

## Still open at launch

- **Four of the fourteen kit-conformance findings** (F 06, 07, 10, 12 above): two need
  a Dr. Ty ruling, two need Maya. **F 09 is closed:** the reviews page ships with 28.
- Wire the forms (GHL + leads backup), then set the confirmation page as the conversion
  goal in Ads, GA4 and Meta.
- Drop `noindex` and the `robots.txt` Disallow **together**, and only at launch. Utility
  pages keep `noindex` permanently.
- Tailwind and anime.js still load from CDNs. Compile and self-host before PageSpeed.
- Attorney review of the three legal pages.
- **The stack conflict is still unresolved.** The brief names WordPress + Elementor +
  RankMath Pro; this is static on Vercel; registrar is CloudFlare. Settle before cutover.
- Three Dr. Ty rulings from the homepage audit, plus the trust-bar question (F 07).

## Closing pass: twelve register items (2026-08-27, Jules)

Twelve open items were ruled on in one sitting and executed in a single pass, four agents
working on disjoint files. Partitioned by file OWNERSHIP rather than by task, because
`index.html` is both the homepage and the source `build/chrome.py` slices chrome from, so
two agents editing it concurrently would silently clobber each other.

### Rulings applied

- **Trust bar: 8 iconed marquee cells to 4 static typographic cells.** Matches the kit's
  BrightWay reference build, and fixes the one genuine cardinality violation on the page:
  `TRUST-BAR-SPEC` rule 2 says 3 to 5 cells. Kept, for patient-decision value rather than
  prestige: certified specialist, 30+ years, 0% in-house financing, direct insurance
  billing. The marquee is gone entirely, including the `role="region"` and the "drag or use
  the arrow keys" aria-label, which described behaviour that no longer exists.
- **H1 now reads "for all of Vancouver."**, not "Van City". Highest-weight string on the
  site, and the slang has negligible search volume. The `<h2>` "Loved across Van City"
  survives deliberately: the local register is worth keeping somewhere.
- **Bento kept** as a house section. The kit does not ban extra sections and its reference
  build carries one of its own, so this was a preference, not a violation.
- **Card borders now pass.** `--line` `#e1e8ee` to `#8b9094`: 1.24:1 to **3.22:1** on white
  and 3.00:1 on `--surface`. `--line-deep` was also failing and nobody had noticed, at
  1.19:1 on the dark band's chip fill, now **3.16:1**. Accepted: 2.78:1 on `--surface-2`,
  whose only bordered use is a 32px numeral disc, not a card. Clearing that too needs a
  visibly heavier line everywhere.

### Claims resolved

- **Price parity is absent, and this is now verified rather than asserted.** It had been
  reported removed three times on the strength of grepping phrasings, which is the wrong
  method. Correct method, and the one to use next time: extract every sentence containing
  the subject nouns and READ them. All 68 sentences naming both "braces" and "Invisalign"
  across the 17 pages are nav chrome, form selects, or clinical-suitability statements.
- **Social profile URLs and the Neera Arora quote never existed on the site.** Both were
  carried as open items for weeks. The only "social" hits were `twitter:card` meta, which
  is an Open Graph card declaration, not a profile link, and there is no `sameAs`.
- **Invisalign provider tier stays pending** by Jules's call. Unverified, so unchanged.
- **Shipping without the Aug 12 photography and without before/afters**, no placeholders.
- **There is no six-bullet services block.** That register item was double-counted: `#paths`
  runs 3 cards, which `SERVICES-GRID-SPEC` rule 1 allows. The real over-ceiling group was
  the trust bar, fixed above.
- **Four credentials appeared three times each, not one.** After the trust bar shrank,
  `MEET-THE-DOCTOR-SPEC`'s cross-section rule took `.doc-creds` from 6 chips to 3. "Former
  associate professor", the 2014 Invisalign award, "certified specialist" and "30+ years"
  are each now asserted once.

### Third-party scripts removed

Tailwind (**3.4.17**) and anime.js (**4.1.4**) are vendored under `assets/vendor/`, with
provenance and refresh commands in `assets/vendor/README.md`.

**The anime.js dependency was already broken and silent about it.** The old `animejs@4`
range URL resolves to 4.5.0 today, but 4.5.0 no longer ships `lib/anime.iife.min.js` at
all, so jsdelivr had been quietly falling back to 4.1.4. That URL could have started 404ing
on any deploy and killed the headline motion sitewide with no warning. Now pinned locally.
Moving past 4.1.4 means choosing a new entry point, not bumping a number.

Still the browser JIT build, not a compiled stylesheet, because `chrome.py` injects
`TW_CONFIG` for it to read at runtime. A compiled build is feasible as a follow-up: node
v24.15.0 and npm 11.12.1 are present, and all 324 runtime class manipulations toggle
hand-written state classes (`active`, `in`, `open`, `is-drag`) with **zero Tailwind
utilities toggled dynamically**, so no safelist would be needed. Gate it on a 17-page
visual diff.

### noindex is now actually selective

`head()` and `page()` had accepted a `noindex` argument since the beginning and **never read
it**, and no generator passed it. So the "selective noindex removal at cutover" promised in
the launch register was impossible: setting the flag did nothing, and the only way to open
the site to indexing was to delete the line, which would have exposed the utility pages too.

Now `REVIEW_BUILD` in `build/chrome.py` is the single cutover switch, and the five pages
that stay noindex forever pass `noindex=True` individually, so flipping the switch cannot
expose them: the four utility pages plus `appointment-request-confirmation`. Verified in all
four states of the truth table. `REVIEW_BUILD` stays `True`; this is a staging URL.
**`robots.txt` carries its own blanket `Disallow: /` and must come off separately.**

### Forms

Wired end to end except the endpoint. One constant, `GHL_WEBHOOK_URL` at
`build/common.py:26`, feeds all six form instances. Full field mapping, storage keys and a
cutover checklist are in `build/GHL-WIRING.md`.

Two things worth knowing, because the earlier audit got them wrong:

- The nine hidden attribution fields existed but were **static empty strings populated by
  nothing**. A code comment promised a first-touch cookie that had never been implemented.
  The audit had cleared the 14-vs-5 field count as "not a finding" on the strength of those
  fields existing.
- The **contact form carried no UTM fields at all**, so attribution was missing outright on
  one of the three forms. All three now share one definition so they cannot drift again.

While the endpoint is unset, no form can be submitted: controls render `disabled` with a
notice offering (604) 662-3290 as a `tel:` link. That is deliberate. The previous
`action=""` posted to the page and lost the lead with no trace. No cookie is set anywhere,
sidestepping rather than merely bounding the never-expiring-cookie defect in our WordPress
plugin. No analytics vendor, pixel or remote script was added.

The homepage loads `ob-leads.js` with **no config object**, so an ad visitor who lands on
`/` and converts elsewhere keeps this landing's attribution. It sits after the main
`<script>` block on purpose: `chrome.py` slices by the FIRST `"  <script>"` marker, so a
one-line tag with attributes cannot match it and does not propagate to the other 16 pages,
which load it with a full config. The four legal and utility pages load it not at all.

### Two kit bugs filed upstream

The stray-solidus defect we had been working around is now filed as
[PR 1](https://github.com/OrthoBoost-Marketing/orthoboost-website-kit/pull/1), and a second
distinct bug found alongside it as
[PR 2](https://github.com/OrthoBoost-Marketing/orthoboost-website-kit/pull/2).

PR 2 is the interesting one. `add_img_dims.py`'s early return, which is what makes the
script idempotent and is correct in itself, means an already-corrupted tag (which by
definition carries `width` and `height`) is never re-examined. **Corruption already on disk
is permanent and survives every rerun**, and fixing the injection does not heal it. Until
both merge, keep running `post_media.py` last.

### Also fixed this pass

- **This file documented the pipeline order backwards**, with `post_media.py` before the
  kit's `add_img_dims.py`. Anyone rebuilding from the documented commands rather than from
  the docstring would have silently reintroduced all 28 malformed tags. Both snippets also
  omitted `gen_reviews`, so the reviews page would have gone stale on every rebuild. The
  code was right and the documentation was wrong, which is the direction that actually
  bites, because documentation is what people reach for.
- A pre-existing stray `</div>` in the hero-screen block: div balance in `<body>` was **-1**
  and is now 0.
- Removed the `.steps-grid` / `.pstep` CSS family, 10 lines the chrome slice had been
  copying into all 17 pages. Neither class appears as markup anywhere on the site.

### Left alone, on purpose

- 660 em dashes live in code comments, CSS comments and script comments. **Zero reach
  visible copy or any attribute**, so nothing patient-facing breaks the house style. They do
  still ship inside comments, which is a mild agency tell of the same family as the
  `font-claude` and `notionvc` markers we grep for before launch. Cleaning them touches all
  17 files and is its own pass.
- `.credo-list` is now 5 items in a 3-column ruled grid, so the bottom rule runs one column
  short. Cosmetic, and better than padding the list with a fact we just deduplicated.
- The `.field` border override hard-coding `--ink-faint` is arguably redundant now that
  `--line` passes. Still correct at 4.4:1. Separate call.
- No-JS form delivery is **untested**, not working-as-far-as-we-know. The forms keep a real
  `action`, but a native POST sends urlencoded and the GHL webhook trigger is only known to
  parse JSON. Every form carries a `<noscript>` block pointing at the phone.

## data-speed is PIXELS PER SECOND, not per frame (2026-08-27)

Jules reported the credentials marquee "doesn't work". It was running. It was moving at
**15 pixels per second**, which is not motion any reader perceives: a cell took 13 seconds to
cross and a full loop ran about two minutes.

Two defects, both in the speed maths, and the second is the one worth remembering.

**It was too slow.** `pos += speed` added `data-speed` pixels on every animation frame, and
the credentials bar carried `data-speed="0.25"`.

**The speed was never a speed.** Because the increment was per frame, the same page ran at
15px/s on a 60Hz display, 30px/s on a 120Hz laptop and 36px/s on a 144Hz monitor. Any
per-frame increment is really a per-refresh-rate increment.

The loop is now time-based: it advances `speed * elapsedSeconds`, so `data-speed` is
**pixels per second** and identical on every display. `dt` is clamped to 50ms because
`requestAnimationFrame` stops in a background tab, and without the clamp the first frame back
carries seconds of delta and teleports the strip.

Current values, all three re-expressed in the new unit:

| Track | Was (px/frame) | Now (px/s) | Note |
|---|---|---|---|
| `.mq-creds`, homepage | 0.25 | **48** | raised to be visibly moving |
| `.mq-reviews`, homepage | 0.35 | **21** | 0.35 x 60, so unchanged on a 60Hz screen |
| `.mq-liners`, `/reviews` | 0.3 | **18** | 0.3 x 60, likewise unchanged at 60Hz |

The two reviews strips were deliberately converted at their existing 60Hz behaviour rather
than retuned, so nothing about those sections changed for most readers. They simply stopped
running at double speed on high-refresh displays.

**`.mq-liners` lives in `build/gen_reviews.py`, not in `index.html`.** It is not part of the
sliced chrome, so changing the unit in the homepage script alone left it declaring `0.3`,
which under the new unit is one pixel every three seconds. Caught by grepping
`data-speed` across `build/*.py` after the edit. Any future change to the marquee unit has to
touch that file too.

### The loop period is measured from the DOM

`half` used to be `track.scrollWidth` taken *before* the mirror was appended. That is the
width of the content, but the loop period is the distance from a cell to its mirrored copy,
which also includes the flex gap between the strip and the mirror. Wrapping at the content
width landed one gap short, so the strip jumped visibly once per loop.

It now comes from `children[period].offsetLeft - children[0].offsetLeft`, which is exact and
needs no knowledge of the gap. That matters because the gap is not constant: the credentials
bar drops from 56px to 34px below 720px.

### How this was verified, after two methods lied

Worth writing down, because the first two answers were both wrong:

- **The in-app Browser pane is useless for this.** It frequently does not lay out or
  composite, so `clientWidth` reads 0 and `scrollLeft` reads 0 even while the animation runs.
  It also reported the strip advancing at ~60px/s at one point, because with no vsync its
  `requestAnimationFrame` runs unthrottled, which flattered the old per-frame code.
- **`--virtual-time-budget` renders understate travel.** Virtual time advances in large steps
  and the 50ms `dt` clamp caps each step's contribution, so a 3-second budget showed 8px of
  travel against 144px of real travel.
- **What worked: real headless Chrome driven over CDP against a wall clock.** Launch with
  `--remote-debugging-port`, connect from Node (v24 has global `fetch` and `WebSocket`, no npm
  needed), and sample `scrollLeft` over several seconds. That measured 47.9px/s against a
  declared 48, and confirmed `wrapLandsOnSameContent` on both marquees. Scripts kept in the
  session scratchpad as `measure-marquee.mjs` and `verify-wrap.mjs`.

## Three mobile defects (2026-08-27)

### The footer logo was stretched

The img carries `width="700" height="250"` attributes, added by the kit's
`add_img_dims.py`, and it also carried an inline `style="height:42px"`. That inline height
beats both `img{height:auto}` and `.foot-brand img{height:26px}`, but nothing constrained the
WIDTH, so it resolved from the 700px attribute capped by `max-width:100%`. Measured at 390px:
342x42, a ratio of 8.14 against the logo's natural 2.8.

**Pinning only the height on an img that has width/height attributes will distort it.** Height
now lives in the stylesheet next to `width:auto`, and the inline style is gone. Now 118x42,
ratio 2.8.

### The locations card was sheared, which is why the map looked wrong

The map was a symptom. `.btn` is `white-space:nowrap`, uppercase, `.16em` tracking, 30px side
padding, so "Book a free consultation" has a min-content width of about 303px. Under 900px the
card collapses to a single `1fr` track, and **a bare `1fr` floors at min-content**, so that one
button forced the track to 303.4px inside a 284px content box. `.loc-card` is
`overflow:hidden`, so 19px was sheared off the right of everything in it: the copy, the hours,
and the map.

Two changes: the track is `minmax(0,1fr)` so it can match the container, and under 560px the
two CTAs stack full width with wrapping allowed so nothing in the card has a min-content width
wider than the card. Track and both children now measure 284px.

**Use `minmax(0,1fr)`, not `1fr`, for any single-column mobile collapse that contains a nowrap
button.**

### The marquee fought the finger on touch

Two separate bugs, and the second is the subtle one.

**Momentum was cancelled.** `touchend` set `paused = false` immediately, but the browser's fling
continues after touchend. The loop resumed on the next frame and assigned `scrollLeft` from its
own accumulator, killing the fling. Fixed with a settle window that holds the loop while
momentum plays out, extends while scroll events keep arriving, then adopts wherever the fling
ended. Our own wrap correction is excluded from extending it, or the window would never close.

**The loop overwrote the drag itself.** Neither pause flag survives a touch gesture: when the
browser takes a touch over for native panning it fires `pointercancel`, which cleared
`dragging`, and `pointerleave`, which cleared `paused`. Both went false with the finger still
down, so the loop resumed and overwrote the native pan every frame.

Measured at 390px with synthesized touch, this was stark: with the loop paused a flick dragged
the strip **129px**; with the loop running the identical flick moved it **13px**.

Fixed with an explicit `touchActive` flag driven only by touchstart/touchend/touchcancel, held
in the step guard, and `pointerleave` no longer clears the hold during a touch. After the fix
the same flick drags **130px** with the loop running, matching the paused case.

Verified over CDP with `Emulation.setDeviceMetricsOverride` at a true 390px (headless clamps
`--window-size` to about 500px, so device-metrics override is the only way) and real
`Input.dispatchTouchEvent` gestures. Note those coordinates are **viewport** relative: the first
attempt dispatched at document coordinates, landed off-screen, and measured the marquee's own
48px/s drift as though it were the drag. Scripts in the session scratchpad:
`mobile-diag.mjs`, `mobile-verify.mjs`, `touch-test.mjs`, `touch-regress.mjs`.

Regression checked after the hold was added: a vertical swipe over the bar still scrolls the
page (327px), and a tap still toggles the pause (aria-pressed true, label Play, zero movement).

