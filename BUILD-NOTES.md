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

## Homepage sections now match Dr. Ty's called-for order (2026-08-25)

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
| **Iryna Ponomarenko** — facial and lip proportions, respected preferences | Specialist planning, not a discount aligner mill |
| **Riaz Meghji** — "well worth the investment" | Handles the price objection |
| **S Ismail** — walks you through the plan, answers thoroughly | Clear treatment plan |
| **SassySips** — retainers, appointment the same day she called | Service speed, and retainer replacement |
| **Fiona Deng** — "Both of my kids like him a lot!" | Kids and family |
| **Dante Foreman** — scan, in and out quickly, info sent over | The free first visit |
| **Skyla W** — finished Invisalign, process explained clearly | Completed treatment |

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
for g in gen_appointment gen_services gen_rest gen_support gen_utility; do python build/$g.py; done
python build/post_media.py
python "$KIT/plugin/skills/static-site-deploy/scripts/add_img_dims.py" .
```

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

## Still open at launch

- **Five of the fourteen kit-conformance findings** (F 06, 07, 09, 10, 12 above):
  two need a Dr. Ty ruling, two need Maya, one needs reviews harvested.
- Wire the forms (GHL + leads backup), then set the confirmation page as the conversion
  goal in Ads, GA4 and Meta.
- Drop `noindex` and the `robots.txt` Disallow **together**, and only at launch. Utility
  pages keep `noindex` permanently.
- Tailwind and anime.js still load from CDNs. Compile and self-host before PageSpeed.
- Attorney review of the three legal pages.
- **The stack conflict is still unresolved.** The brief names WordPress + Elementor +
  RankMath Pro; this is static on Vercel; registrar is CloudFlare. Settle before cutover.
- Three Dr. Ty rulings from the homepage audit, plus the trust-bar question (F 07).
