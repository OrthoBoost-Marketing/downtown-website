# CLIENT BRIEF: Downtown Orthodontics
Generated 2026-08-24 · status: DRAFT

> Written **extractively**, not from an interview. Sources: the Notion client record
> (`31232d95-51dd-81ae-b086-cd14a2d107ce`), its Locations and Scheduling records, the two
> Offers records, Dr. Ty's `Downtown Orthodontics - Positioning Brief (Jules).pdf` v2, and
> Maya's consolidated credential list of 2026-08-24. Anything not in one of those is marked
> `TBD` or `ASSUMED` at the bottom. Nothing here was inferred from general knowledge.

## Identity
practice: Downtown Orthodontics | founded: TBD (practice is 30+ years old; no founding year on file) | domain: downtownorthodontics.ca | tagline: "The specialist orthodontist for all of Van City."

## Avatar & voice
avatar: affordable-ortho
voice notes: Professional, expert, patient-first, but warm and inclusive. Use the local term "Van City". **Never** luxury, VIP, boutique or premium-tech language: Dr. Ty's v2 brief explicitly kills the "premium Invisalign boutique" identity because the real competitor is general dentists selling discount aligners, and sounding premium puts Dr. Daher on their shelf looking overpriced. Notion brand persona: "High-Expertise Clinical Ortho". Languages: English only, **no Spanish**. Medicaid: **No, never mention.**

**COPY RULE, added 2026-09-04 after Charlotte's review. This constrains how the line above may be expressed.**

The positioning above is still correct: the competitor *is* general dentists selling discount aligners, and that is why premium language is banned. **But the site may never say so.** Charlotte's 3 September review asked, in writing, that we stop wording it as "dentists selling aligners on the side" and instead "hone in on 'this is a specialist'". Her reason is regulatory as well as commercial: she does not want local dentists reading the site as undercutting them, and she does not want the College of Dental Surgeons of BC taking an interest.

So the competitor framing is **strategy, not copy**. In patient-facing text:

- **Do not** name, characterise, or describe general dentists, dental offices, or other practitioners, favourably or otherwise. Not in headings, body copy, card titles, comparison tables, FAQ answers, meta descriptions, nav labels, image alt text, or HTML comments. Comments matter: `chrome.py` slices `index.html` comments and all, so a comment ships in all 17 pages.
- **Do** make the same point by describing what a certified specialist does. "Orthodontics is a separate specialty after dental school" carries the whole argument without a target.
- Where a comparison is genuinely useful, compare **processes**, not people. The compare table's left column is headed "Aligners without a specialist" and its rows describe process gaps ("No orthodontic specialist involved"), which is the pattern to follow.
- Phrases that are now banned sitewide, and were removed on 2026-09-04: "aligners on the side", "sold on the side", "discount aligners", "between fillings", "general dental office", "general dentist", "not the shortcut", "complex cases other offices decline", "cases other offices declined".

**One deliberate exception:** verbatim patient reviews. Alex Bobylev's Google review says Dr. Daher is "repairing the work I had done at a regular dentist". That is the patient's own published words, attributed, which is a different risk class from the practice asserting it.

**SETTLED 2026-09-04 by Jules: the review stays, in full, in both places** (homepage and `/reviews`), untouched. Charlotte's review did not ask for anything about it, and the instruction was to do exactly what she asked and no more. A proposal to trim the longer `/reviews` version back to the homepage excerpt was raised and declined. Do not revisit this without a new instruction: it is the only place any dentist-directed wording remains, and that is intentional.

Open question for whoever briefs the attorney already reviewing the three legal pages: whether the BC college restricts patient testimonials as a category, independent of their content. Nobody here has established that, and it would bear on the whole `/reviews` page and all 28 reviews on it, not just this one quote. It has not been checked.

The reasoning behind the ban on premium language, which used to sit in an `index.html` comment, now lives in `BUILD-NOTES.md` under "Why premium language is banned", because that comment was being served on every page.

## Doctors
- Dr. Sam Daher, Certified Specialist in Orthodontics, sole doctor and founder, bio depth: **full**. 30+ years in practice; former associate professor, University of Montreal and University of the Pacific; McGill (Dr. James McCutcheon award)
doctor hub page: no  ← single doctor

## Locations
primary phone (sitewide default, used in header/mobile bar on non-location pages): +1 604 662 3290
- Vancouver: 840 W Hastings St, Vancouver, BC V6C 1C8 · (604) 662-3290 · Mon 10:00–18:00, Tue 08:00–15:00, Wed 08:00–16:30, Thu 08:00–15:00, Fri–Sun closed · landmarks: by Canada Place, across from Terminal City Club, down the street from Vancouver Club, across from Breitling
  areaServed: Downtown Vancouver, Burnaby, South Vancouver, Richmond, Surrey, North Vancouver
  geo: **omit**
location pages: none (single office)

> Hours are client-confirmed and verified line by line against the Notion Locations record; they may ship in `openingHoursSpecification`.
> `geo` is deliberately **omit**. The homepage previously carried derived coordinates and they were removed in the 2026-08-24 audit. Do not put them back without the pin from the client's Google Business Profile.
> The four landmarks above are the client's own and are now the ONLY ones used sitewide. The invented "two blocks from Waterfront Station" was removed on 2026-08-24; zero references remain.
> Do **not** publish (778) 763-1707 anywhere. That is the Google Ads call-tracking number.

## Nav (the agreed header tree)
Treatments ▾ {Braces · Kids & early care · Invisalign & Quick 6 Fix · Retainers & aftercare · Common questions} | How it works | Meet Dr. Daher | Pricing | Visit
financing in main nav: yes (as "Pricing")

> This mirrors the live homepage header exactly, which currently points at in-page anchors. The build re-points them at the real pages. **The header layout does not change.**

## Assets (real paths, relative to the site root)
| File path | What it is | Use on | Delivered? |
|---|---|---|---|
| assets/Logo_Full-Dark_Downtown Orthodontics.png | wordmark, dark | header | yes |
| assets/Logo_Full-Light_Downtown Orthodontics.png | wordmark, light | footer | yes |
| assets/downtown-orthodontics-icon.svg | smile mark | favicon source | yes |
| assets/downtown-orthodontics-favicon-48.png | favicon | all pages | yes |
| assets/downtown-orthodontics-apple-touch-icon-180.png | apple touch icon | all pages | yes |
| assets/downtown-orthodontics-icon-512.png | schema logo | JSON-LD | yes |
| assets/photos/dt-7.jpg | Dr. Daher, studio, holding aligner | homepage hero (LCP) | yes |
| assets/photos/dt-6.jpg | Dr. Daher, studio portrait | doctor bio, homepage doctor band | yes |
| assets/photos/practice.jpg | Dr. Daher seated, teal wall | why page, homepage bento | yes |
| assets/photos/used-3.jpg | Dr. Daher at desk explaining a plan | how-it-works, appointment page | yes |
| assets/photos/used-1.jpg | female team member, studio, holding a retainer | family-facing slots | yes |
| assets/photos/used-2.jpg | female clinician scanning a patient chairside | early-ortho, how-it-works | yes |
| assets/photos/img-3127.jpg | Dr. Daher with an adult patient | adult treatment slots | yes |
| assets/photos/office-inside.jpg | reception interior | contact, visit, why page | yes |
logo: assets/Logo_Full-Dark_Downtown Orthodontics.png · delivered: yes

> **PHOTO RULE, from the client's second reviewer:** Dr. Daher must not appear touching or hugging child patients. Three shots were pulled for this on 2026-08-24 (`img-0079`, `img-0081`, `img-4241`). A female provider reads better in family-facing slots. **Consequence: there is currently no photograph of a child anywhere on the site.** Do not solve this by reintroducing a pulled shot.

## Reviews (quotable: verbatim text, not just a count)
**RESOLVED 2026-08-24.** Pulled from the practice's live Google Business Profile with Jules present.
- **Rating: 4.4 out of 5, from 160 Google reviews.** Profile link: `https://www.google.com/maps?cid=9098292092356715373`
- Displayed as **text only**. Never marked up as `AggregateRating`. The kit bans it and so does Google's self-serving-review policy.
- Twelve quotes run verbatim in the homepage reviews marquee, each doing a different job:
  Kim Patara (retention: original Invisalign 2007, teeth have not shifted) · Iryna Ponomarenko (comprehensive method, facial and lip proportions) · S Ismail (walks you through the plan) · Dante Foreman (fast first scan) · Fiona Deng (both kids like him) · SassySips (same-day retainer replacement) · Skyla W (finished Invisalign) · Riaz Meghji (attention to detail, worth the investment) · Jayden Dinh (looked forward to appointments) · amber rold (Invisalign, staff) · Sonya Lee (returning patient) · Atlas Hanen (comfort)
- **Still to place:** service pages, the appointment page and the financing page each want a topic-matched quote beside the form. Those slots remain visible placeholders until the right quote is assigned per page.
- **Builders must not invent quotes.** Trim only with an ellipsis at a sentence boundary; never reconstruct.

## Appointment
type: free
name: "Free consultation"
exam fee: free
treatment pricing published on site: yes (from $220/mo, $1,000 down, 0% in-house)
template: offer-led  ← there is an active evergreen $-off offer

## Brand
logo: assets/Logo_Full-Dark_Downtown Orthodontics.png · colors: pale blue `#CCDBE7` (accent), charcoal `#313131`, near-black `#010101`, light grey `#EDEDED` · fonts: Nunito throughout
direction: carried from the live Concept B homepage. **The design system is tokenized in the homepage's `:root`** (spacing `--sp-*`, type `--fs-*`, weights `--fw-*`, `--tap`, `--border`, `--radius-*`, `--section-y`). Every new page reads those tokens and adds none.
**The display voice is LIGHT.** All display type is Nunito at weight 200–300, wide-tracked. Never set a heading heavier.
**There is one card language:** `background:var(--bg)` + `var(--border) solid var(--line)` + `var(--radius-lg)` + `var(--shadow-soft)`. No coloured edge bars on any card, ever.

## Services (homepage grid count: 3)
The homepage grid is the **audience** split, and it stays at three cards: Kids · Teens · Adults. The service *pages* below are a separate, longer list. Do not rebuild the homepage grid to match the page count.
1. Braces, metal and clear (money page: yes)
2. Invisalign and Invisalign Teen, incl. Invisalign Express "Quick 6 Fix" at $4,299 flat (money page: yes)
3. Early / interceptive orthodontics, expanders, corrective appliances, Invisalign First (money page: yes)
4. Retainers and retention, clear (money page: no)

Also offered, to fold into the pages above rather than give their own: complex bite correction, retreatment, aesthetic braces and aligners, digital scans and imaging, bite and jaw alignment assessment, growth and development evaluation, treatment planning.

## Proof
rating: 4.4 · reviews: 160 · patients: 900 (Notion "Patients Served") · years: 30+ · awards: see below
trust bar: credential

Dr. Daher's ten client-supplied credentials (Maya, 2026-08-24: treat as confirmed, run **Invisalign-first** per Jules's explicit call):
1. An early adopter of Invisalign; worked with **Align Technology**'s founder on the company's scientific advisory board
2. Still one of a select few orthodontists on Align's scientific advisory board
3. Invisalign Lifetime Achievement Award, 2014
4. Lectured in 46 countries, 142 cities, six continents
5. Founder of the Daher Aligner Institute
6. Founder of Stream Dental HR
7. Former associate professor, University of Montreal and University of the Pacific
8. McGill's Dr. James McCutcheon award
9. Opened the world's first Invisalign-only practice, 2009
10. Top 1% of Invisalign providers globally; top provider worldwide 2009–2011

> The company is **Align Technology**, singular. The source note wrote "Align Technologies".
> Items 5 and 6 have no description on file. The homepage subs assert only what the titles state. Do not embellish them.
> **No `AggregateRating` or `Review` objects in JSON-LD anywhere**, per the kit ban.

## Photography
available: 8 real client photographs, all with real paths above
missing: any child patient; a female provider with a child; real before/after cases; team headshots for Maya and Bita
shoot planned: 12 August 2026, **has not landed as of 2026-08-24**
constraints this creates: family-facing slots run without children; before/after slots run as on-brand placeholder panels, never stock models; no team page

## Team
tier: minimal · turnover risk: unknown, treat as high
→ **No team page.** Maya and Bita are known by name only, with no bios and no delivered headshots. Fold a short team sentence into the why page instead.

## Money story
fork: affordability
financial page: yes · financing in main nav: yes

Confirmed figures, identical everywhere they appear: **$1,000 down · from $220/mo · 0% in-house interest · direct insurance billing · free consultation · pay in full and save 5% · save $450 on a same-day start · Invisalign Express (Quick 6 Fix) $4,299 flat.**
Active offer (Notion, verified 2026-08-24): **"$1,000 Off Full Treatment Invisalign or Braces"**, Evergreen, Status=Active. The "$500 Off" record is Inactive. Keep the $-off in one swappable slot.
> Never write "0% down". The current live site says it and it is inaccurate.
> Keep "Save $1,000" (the promotion) distinct from "$1,000 down" (the financing).
> The Notion offer records have an **empty disclaimer field**, so no disclaimer ships. Confirm none is required before launch.

## Integrations
ghl webhook: **NOT SUPPLIED**, blocks form wiring · booking link: currently `https://downtownorthodontics.ca/appointment-request/` on the existing WordPress site · review link: TBD · call tracking: CallTrackingMetrics → GHL → office

## Launch
domain: downtownorthodontics.ca · dns controlled by: CloudFlare (registrar per Notion) · deadline: none current (the Notion "Expected Launch Date" of 2026-02-16 is stale) · rebuild: yes
> **UNRESOLVED STACK CONFLICT.** Dr. Ty's brief names WordPress + Elementor + RankMath Pro, and Notion records `Hosting = Client Hosted` with WP access already sent. This site is static on Vercel. Settle before any cutover; it could invalidate the build target.
> The Notion Sales Notes still read "NO NEW WEBSITE! Only a Transfer!": stale, from the 2026-01-28 signing, superseded by the v2 brief.

## Page inventory  ← the build skill executes this list
- [x] index.html: exists, live, audited
- [x] braces.html
- [x] invisalign.html
- [x] early-orthodontics.html
- [x] retainers.html
- [x] appointment-request.html
- [x] appointment-request-confirmation.html
- [x] why-choose-us.html
- [x] dr-sam-daher.html
- [x] financing.html
- [x] faq.html
- [x] contact.html
- [x] privacy-policy.html
- [x] terms.html
- [x] accessibility.html
- [x] 404.html
- [x] reviews.html

Flat filenames at the root, served extensionless: `vercel.json` sets `cleanUrls: true`, so `braces.html` resolves at `/braces`. **Every internal link must be written extensionless from the start.** Retrofitting clean URLs touched every file on Siouxland.

Derived from the skill's own rules: single doctor → no doctor hub · single office → no location pages · client supplies no team content → **no team page** · affordability-led money story → **financing page yes**.
> **REVISED 2026-08-26.** The original derivation read "review count unknown and no quotes → no reviews page". Both halves stopped being true on 2026-08-24: the profile is 4.4 from 160. `REVIEWS-PAGE-SPEC` sizes a high-volume practice at 24 to 30 reviews, so **reviews.html ships with 28**, all verified five-star and quoted verbatim.
One deliberate deviation: a **standalone FAQ page** ships even though the practice is not education-heavy, because eight client-voiced Q&As already exist and are already in the homepage `FAQPage` schema, and the client's own Notion sitemap asks for `/faq`.

## Open questions / assumptions
- ~~TBD: review quotes and the rating/count.~~ **RESOLVED 2026-08-24, extended 2026-08-26:** 4.4 from 160. Twenty-eight verified five-star reviews are now harvested verbatim into `build/reviews_data.py`, which also records the full non-five-star exclusion list and how it was established. Per-page quote assignment for the service, appointment and financing forms is still open, and `reviews_data.py` is the source to draw them from.
- **TBD: GHL webhook URL.** Blocks form wiring and the leads backup.
- **TBD: founding year.** Never write one; "30+ years" is the safe form.
- ~~TBD: treatment duration.~~ **RESOLVED 2026-08-24:** softened everywhere. No duration range is published; every answer now points at the consultation for a case-specific timeline.
- **TBD: social profile URLs** (Instagram, Facebook, Google reviews). The footer row was removed on 2026-08-24 rather than ship dead icons.
- **TBD: Neera Arora endorsement quote**, named as a proof element in brief §8 and still unsupplied.
- **ASSUMED: avatar `affordable-ortho`.** Derived from the v2 brief's "specialist for everyone: expert, full-service, affordable".
- **ASSUMED: the four service pages.** Built from the Notion service fields; the client's own sitemap is an unfilled generic template with Dallas/Plano placeholders, so there is no client-approved page list to follow.
- **AWAITING DR. TY:** three rulings from the 2026-08-24 audit: the "Van City" H1 versus the literal-city rule; the 5-card homepage bento that maps to no kit section type; whether the credentials marquee, before/after slider and sticky stepper count against "no carousels".
