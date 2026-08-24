## Downtown Orthodontics — website

[Notion client record](https://www.notion.so/31232d9551dd81aeb086cd14a2d107ce) · Dr. Sam Daher · Downtown Vancouver, BC · downtownorthodontics.ca

**Status (2026-08-24):** homepage only, deployed to Vercel as a client review build.
Concept B is the agreed direction, light mode only. This is a flattened copy of
`downtown-orthodontics/concept-b/` in
[Client-web-concepts](https://github.com/OrthoBoost-Marketing/Client-web-concepts);
that repo stays the design home, this one is what Vercel serves.

### What this build carries

- The warmer, family-first Concept B layout, **light mode only** — no dark
  variant and no toggle.
- Dr. Daher's full credential record (ten client-supplied items) in a
  "Credentials & recognition" section, plus above-the-fold marquee, doctor
  chips, bio, and `Person` JSON-LD.

### Deliberately absent — do not "fix"

- **`noindex` + `robots.txt` Disallow.** A review build must not compete with
  downtownorthodontics.ca in search. Both come off at launch, together.
- **Sibling pages.** The nav points at in-page anchors only. Service, doctor,
  location, financial, FAQ and legal pages are not built yet.

### Open items before this can launch

1. **Real photography.** The Aug 12 shoot has not landed. Every slot marked
   `PHOTO SWAP` in `index.html` is a placeholder. Per the client's second
   reviewer, Dr. Daher must not appear touching or hugging child patients — brief
   the shoot for a **female provider with a child patient**. Three existing shots
   of him posed with children were pulled for this reason, which means the Kids
   and Teens cards currently show **no children at all**.
2. **Two credential descriptions.** Maya to confirm one line each for the Daher
   Aligner Institute and Stream Dental HR. Flagged inline; the placeholders
   assert only what the titles already state.
3. **Reviews and the Neera Arora endorsement** are still placeholder copy
   matching real review themes. Flagged on the page itself.
4. **Before/after slider** runs on-brand placeholder panels, not real patient
   photos. Needs cases with signed consent (kids included).
5. **Forms are not wired.** No GoHighLevel webhook and no orthoboost-leads
   backup yet. See the `orthoboost-ghl-forms` and `orthoboost-leads-connect`
   skills.
6. **Tailwind and anime.js load from CDNs.** Fine for review, not for launch —
   compile Tailwind and self-host both, or PageSpeed will not clear.
7. **Legal pages, office hours, and attorney review** all still outstanding.

### Claims worth knowing about

Every credential on this page came from the client (Maya) on 2026-08-24 and is
treated as confirmed. Two notes:

- The company is **Align Technology** (singular). The source note wrote "Align
  Technologies"; corrected here.
- The credential list is heavily Invisalign-weighted, which sits in tension with
  Dr. Ty's v2 positioning brief ("kill the premium Invisalign boutique identity",
  braces and kids as the hero). Running the list Invisalign-first was an explicit
  call, not an oversight.
