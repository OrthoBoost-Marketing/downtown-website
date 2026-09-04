# Lead wiring, Downtown Orthodontics

Status: **capturing leads; GoHighLevel still disconnected.**

Two delivery paths, set independently in `build/common.py`:

| Path | Constant | State | What it does |
|---|---|---|---|
| OrthoBoost Leads backup | `LEADS_BACKUP_URL` + `LEADS_SITE_ID` | **live** | stores every lead in Postgres, read at `leads.startorthoboost.com/dashboard/downtown-orthodontics` |
| GoHighLevel webhook | `GHL_WEBHOOK_URL` | **empty** | nothing; no URL is on file (CLIENT-BRIEF.md, Integrations: "ghl webhook: NOT SUPPLIED") |

The backup is a complete delivery path on its own, so **the forms are live now**. They
were previously shipped disabled behind a call-us notice, because GHL was the only path
and it was unset. That fail-safe still exists, but it now triggers only when *both*
paths are blank (§4).

Setting `GHL_WEBHOOK_URL` later is **additive and needs no rework**: the forms then post
to both, backup first, and the browser reports GHL's verdict back to the backup so the
dashboard can flag anything GHL drops. See §9 for the backup and §7 for the GHL cutover.

---

## 1. The one thing to set at GHL cutover

**File:** `build/common.py`
**Line:** **27**

```python
GHL_WEBHOOK_URL = ""
```

Paste the client's GHL inbound-webhook URL between the quotes and re-run the generators.
Nothing else on the site needs editing: all three lead forms, all six form instances and
the client-side submit script derive their endpoint from this constant.

```python
GHL_WEBHOOK_URL = "https://services.leadconnectorhq.com/hooks/<LOC>/webhook-trigger/<ID>"
```

Related constants in the same block, change only if you mean to:

| Constant | Line | Value | Meaning |
|---|---|---|---|
| `LEADS_BACKUP_URL` | 47 | `https://leads.startorthoboost.com` | the backup platform; blank turns it off |
| `LEADS_SITE_ID` | 48 | `downtown-orthodontics` | the registered site row. Stable forever, never rename it |
| `LEAD_CONFIRM_URL` | 54 | `/appointment-request-confirmation` | where a successful submit redirects |
| `LEAD_ATTR_DAYS` | 64 | `90` | first-touch attribution lifetime, in days |
| `LEAD_QUEUE_DAYS` | 69 | `30` | in-browser failed-lead queue lifetime, in days |

---

## 2. The forms

Three form templates, six instances. No form carries more than five visible fields and
none asks for health information.

| Page | Generator | Form `id` | Visible fields |
|---|---|---|---|
| `/appointment-request` | `build/gen_appointment.py` | `lead-appointment` | first name, last name, phone, email, interest (select) |
| `/braces` | `build/gen_services.py` | `lead-braces` | first name, last name, phone, email, interest (select) |
| `/early-orthodontics` | `build/gen_services.py` | `lead-early-orthodontics` | as above |
| `/invisalign` | `build/gen_services.py` | `lead-invisalign` | as above |
| `/retainers` | `build/gen_services.py` | `lead-retainers` | as above |
| `/contact` | `build/gen_support.py` | `lead-contact` | first name, last name, phone, email, **message (textarea)** |

The contact form is the odd one out: its fifth visible field is a free-text
"How can we help?" box, not the interest select. It is the one permitted textarea on the
site and its own microline tells visitors not to send health information there. Treat
`message` as free text that a human reads, and do not build automation that assumes it
is clinical intake.

The interest select's options are plain text with no `value` attributes, so the payload
carries the visible label, for example `Braces, metal or clear`. On the four service
pages the option matching that page's service is pre-selected.

---

## 3. Field mapping for whoever configures the GHL inbound webhook

The form POSTs a **JSON** body. GHL reads each key as
`{{inboundWebhookRequest.<key>}}`. **Keys are case- and space-sensitive**, including the
space in `Full Name`. Do not rename them.

### Canonical OrthoBoost fields, map all of these

These are the standard set used on every OrthoBoost client, so the usual workflow
mapping applies unchanged.

| Payload key | Where it comes from | Suggested GHL contact field |
|---|---|---|
| `Full Name` | visible first name + " " + last name | Full name |
| `Email` | visible email field | Email |
| `Phone` | visible phone field | Phone |
| `utm_source` | URL `?utm_source=`, else stored first touch, else inferred | OB_Source |
| `utm_medium` | URL `?utm_medium=`, else stored first touch, else inferred | OB_Medium |
| `utm_campaign` | URL `?utm_campaign=`, else stored first touch | OB_Campaign |
| `utm_content` | URL `?utm_content=`, else stored first touch | OB_Content |
| `gclid` | URL `?gclid=`, else stored first touch | param_gclid |
| `fbclid` | URL `?fbclid=`, else stored first touch | param_fbclid |
| `gbraid` | URL `?gbraid=`, else stored first touch | param_gbraid |
| `wbraid` | URL `?wbraid=`, else stored first touch | param_wbraid |
| `Offer` | URL `?offer=` if present, else the form's build-time default | OB_Offer |

Build-time `Offer` defaults: `$1,000 off full treatment` on the appointment page and the
four service pages, empty on the contact form. A URL `?offer=` parameter overrides it; an
absent one does not blank it.

### Site extras, optional to map

Present in every payload. Map what is useful and ignore the rest.

| Payload key | Meaning |
|---|---|
| `first_name` | visible first name, unsplit, for a first-name-only merge field |
| `last_name` | visible last name |
| `utm_term` | URL `?utm_term=`, else stored first touch. Local addition, not in the canonical set |
| `interest` | the interest select's label. Empty on the contact form |
| `message` | the contact form's free-text box. Empty on the other five forms |
| `page` | which page the lead came from, for example `appointment-request`, `braces`, `contact` |
| `form_id` | which form instance, for example `lead-braces` |
| `page_url` | the full URL at submit time, query string included |
| `referrer` | `document.referrer` at submit time. Empty on a direct arrival |
| `first_touch_at` | ISO timestamp of the visitor's first recorded touch |
| `submitted_at` | ISO timestamp of the submit |

### Attribution resolution, in order

1. A parameter present in the current URL wins.
2. Otherwise the stored first touch for that parameter.
3. Otherwise, for `utm_source` and `utm_medium` only, an inferred value so the contact is
   never blank on attribution:

| Arrival | `utm_source` | `utm_medium` |
|---|---|---|
| `gclid`, `gbraid` or `wbraid` present | `google` | `cpc` |
| `fbclid` present | `facebook` | `paid-social` |
| external referrer, no UTMs | the referrer's hostname | `referral` |
| no referrer or an internal one, no UTMs | `direct` | `none` |

First touch is recorded on **every page that loads the script**, not only the pages with
a form, so an ad landing on `/financing` still attributes a lead submitted later from
`/appointment-request`.

**Known gap:** the homepage `index.html` does not load the script, so a visitor who lands
on `/` from an ad and never touches another page before converting will attribute from the
form page instead. `index.html` is owned separately and was deliberately not edited. To
close it, add these two lines to the homepage body, matching what
`common.leads_script()` emits:

```html
<script>window.OB_LEADS = {"attr_days": 90, "backup": "https://leads.startorthoboost.com", "confirm": "/appointment-request-confirmation", "endpoint": "", "phone": "(604) 662-3290", "queue_days": 30, "site_id": "downtown-orthodontics", "tel": "+16046623290"};</script>
<script src="/assets/js/ob-leads.js" defer></script>
```

Better: move the call into `build/chrome.py`'s `page()` so every page gets it from the one
constant. That file is also owned separately.

Pages that currently load the script: the six form pages, the confirmation page,
`dr-sam-daher`, `why-choose-us`, `reviews`, `financing`, `faq`. Deliberately excluded:
`privacy-policy`, `terms`, `accessibility`, `404`, and `index.html`.

---

## 4. Fail-safe behaviour when there is NO delivery path

This state **is not the current one.** The backup is live, so the forms are live. It
triggers only when `common.delivery_ready()` is false, meaning `GHL_WEBHOOK_URL` is
empty *and* the backup is off (`LEADS_BACKUP_URL` or `LEADS_SITE_ID` blanked). In that
case the generators render every lead form in a disabled state:

- every visible control gets `disabled`, so nothing can be typed or submitted;
- a notice is inserted as the form's first child, linked by `aria-describedby`, reading
  "Online requests are not open yet" and giving the practice number **(604) 662-3290** as
  a `tel:` link;
- the `<form>` carries `data-ob-lead="0"` and the submit script ignores it;
- hidden inputs are left enabled so the attribution set stays inspectable in devtools.

Nothing is posted, no confirmation page is shown and nothing reports a lead as sent. This
is deliberate: a static site with no endpoint cannot deliver a lead, so the only honest
options are to refuse the submission or to hand the visitor a channel that works. A form
that appeared to submit would lose the lead silently, which is worse than a form that
says it is closed.

There is **no mailto fallback** because no practice email address is on file anywhere in
this repo or in CLIENT-BRIEF.md. Inventing one would be a defect. If an address is
supplied, add it to the notice in `common._unset_notice()`.

Configuring either path reverses all of this on the next build: forms become
interactive, `data-ob-lead="1"` and the notice disappears.

---

## 5. Submit path

1. The form is a real `<form method="post">`. `action` is the GHL webhook when one is
   set; with no webhook it is empty, because both alternatives are worse: the backup's
   `/api/lead` rejects a native urlencoded POST with a 400 JSON page, and a self-POST to
   a static host is a 405. Every form already carries a `<noscript>` block naming the
   practice phone for exactly that case, and `ob-leads.js` always calls
   `preventDefault`, so `action` is never used while JS runs.
2. Hidden attribution inputs are filled from the URL and stored first touch.
3. `form.checkValidity()` runs. The forms carry `novalidate` so one message can be shown
   in place, but the `required` attributes are real and still enforced here. The first
   invalid field is focused.
4. **The backup fires first.** `fetch` POSTs `application/json` with `keepalive` to
   `https://leads.startorthoboost.com/api/lead`, with `site_id` prepended to the
   payload. `site_id` is prepended rather than merged over, so no form field could
   overwrite it. Every part of this call is wrapped so it can never block, delay or
   alter what follows.
5. **Then GHL, if a webhook is set.** Same JSON body, minus `site_id`. GHL's webhook
   trigger only parses JSON, and its CORS headers allow the request straight from the
   browser. Its verdict is reported to the backup's `/api/lead-result` either way, so
   the dashboard can flag a lead GHL dropped.
6. **Which response decides the visitor's outcome:**
   - webhook set: GHL decides, exactly as before. A non-2xx or a network error queues
     the lead locally (§6) and shows the practice number; a 2xx redirects.
   - **no webhook (today): the backup decides.** `{"ok":true}` redirects;
     anything else, including the platform's honest 503 when Postgres is down, queues
     the lead locally and shows the practice number. `/api/lead-result` is **not**
     called, because there is no GHL result to report.
7. On success the `ob_generate_lead` event fires and the browser redirects to
   `/appointment-request-confirmation`.

A lead is never thanked for unless something durable accepted it. That is the whole
reason the backup goes first.

**No-JavaScript caveat.** With JS disabled nothing is delivered: `action` is empty while
no webhook exists, and even with one the native POST would send
`application/x-www-form-urlencoded`, which GHL's webhook trigger is not known to parse
(`text/plain` is documented to fail; urlencoded is untested here). Every form therefore
carries a `<noscript>` block telling the visitor to call the practice. Do not claim the
no-JS path works until someone tests it against a real endpoint.

### The `ob_generate_lead` event

**There is no existing analytics or event convention in this repository.** A search for
`ob_generate_lead`, `dataLayer`, `gtag` and `generate_lead` across all HTML, Python,
JS, Markdown and JSON returns nothing, and no `/thank-you/` page exists. The house name
`ob_generate_lead` and the existing `appointment-request-confirmation.html` page were used
on that basis.

No analytics vendor, pixel or third-party script was added, because the site is being
de-CDN'd in parallel. The event only:

- pushes onto `window.dataLayer` (creating the array if absent, which loads nothing), and
- dispatches a DOM `CustomEvent` named `ob_generate_lead` on `document`.

Event detail: `event`, `form_id`, `page`, `interest`, `utm_source`, `utm_medium`,
`utm_campaign`, `offer`. **No name, email or phone is put in the event.**

It fires twice by design: once on the form page at the moment of success, and once on the
confirmation page, which is the conversion URL. The second firing uses a one-shot
`sessionStorage` flag set at submit time, so navigating to the confirmation URL directly
fires nothing. A tag installed later will catch the confirmation-page firing even though
the redirect can cut the first one short.

---

## 6. In-browser queue (last resort, not the backup)

Server-free, so even a submit that fails everywhere never silently loses a lead. This is
**not** the OrthoBoost Leads backup; that is §9.

| | |
|---|---|
| **Store** | `localStorage`, never a cookie |
| **Key** | `ob_lead_queue_v1` |
| **Expiry** | **30 days** per entry (`LEAD_QUEUE_DAYS`), pruned on every read and write |
| **Cap** | 20 entries, oldest dropped first |
| **Shape** | `[{ queued_at: ISO, exp: epoch_ms, payload: {…the full JSON payload…} }]` |

Written whenever a POST fails. The visitor is then shown the practice number
**(604) 662-3290** as a `tel:` link, so they still have a route to the office.

**Retrieving queued leads.** In the visitor's browser console on any page of the site:

```js
obLeadQueue()        // array of queued entries, expired ones already filtered out
```

The script retries the queue quietly on the next page load, down the same primary path a
fresh submit would take: the backup while there is no webhook, GHL once there is one.
Entries that go through are removed. A retry can create a duplicate if the original POST
actually landed but its response was unreadable; GHL's create/update contact action
collapses those by email and phone, and a duplicate row on the backup dashboard is
visible and deletable rather than a lost lead.

This queue lives only in the visitor's own browser. It is a last-resort safety net for
the person in front of the screen, not a lead database the practice can query. The lead
database the practice can query is the OrthoBoost Leads platform, §9.

### Other storage this site's forms use

| Key | Store | Expiry | Purpose |
|---|---|---|---|
| `ob_attr_first_touch_v1` | localStorage | **90 days** (`LEAD_ATTR_DAYS`), checked and dropped on read | first-touch attribution |
| `ob_attr_first_touch_v1` | sessionStorage | the browser session | mirror, for when localStorage is blocked but sessionStorage is not |
| `ob_lead_queue_v1` | localStorage | 30 days | in-browser queue for a lead nothing accepted |
| `ob_lead_event_pending_v1` | sessionStorage | one-shot, deleted on read | fires `ob_generate_lead` on the confirmation page |

**No cookie is set anywhere by these forms.** A never-expiring attribution cookie is a
known defect in the OrthoBoost WordPress plugin, and it is avoided here by not using
cookies at all. Every stored record carries its own explicit expiry and is dropped when
past it. Every storage access is wrapped in `try/catch`, because private-browsing modes
throw on the storage property itself, not just on write.

---

## 7. GHL cutover checklist

This is the checklist for ADDING GoHighLevel later. None of it is required for the
site to capture leads today: the backup already does that (§9). Steps 1-3 are the
client's GHL side, 4-6 this repo, 7-11 verification.

1. **Get the webhook URL.** In the client's GHL workflow, add an Inbound Webhook trigger
   and copy its URL.
2. **Test the endpoint directly**, with the full field set so GHL captures a sample. GHL
   only exposes `inboundWebhookRequest.<field>` for fields present in a sample.
   ```bash
   curl -s -X POST "<WEBHOOK URL>" -H "Content-Type: application/json" \
     --data '{"Full Name":"Webhook Test (delete me)","Email":"test@example.com","Phone":"6045550123","utm_source":"test","utm_medium":"cpc","utm_campaign":"check","utm_content":"a","gclid":"g1","fbclid":"f1","gbraid":"gb1","wbraid":"wb1","Offer":"$1,000 off full treatment","first_name":"Webhook","last_name":"Test","utm_term":"t","interest":"Braces, metal or clear","message":"","page":"appointment-request","form_id":"lead-appointment","page_url":"https://downtownorthodontics.ca/appointment-request","referrer":"","first_touch_at":"","submitted_at":""}'
   # expect: HTTP 200 {"status":"Success: test request received"}
   ```
3. **Map the fields in GHL** per §3 and **publish the workflow.** An unpublished workflow
   only captures samples. The endpoint returns 200 either way, so 200 alone does not prove
   a contact was created. Verify in GHL.
4. **Set the constant:** `GHL_WEBHOOK_URL` in `build/common.py`, line 27. Leave
   `LEADS_BACKUP_URL` and `LEADS_SITE_ID` exactly as they are: the backup stays on and
   stays in shadow mode, because from then on the site posts to both and reports GHL's
   result back itself.
5. **Re-run the full build**, all eight steps in the order given at the bottom of
   BUILD-NOTES.md. The last two steps are not optional: skipping them strips the image
   `width`/`height`/`loading`/`decoding` attributes and regresses CLS.
6. **Confirm the forms came out live and now carry the webhook:**
   ```bash
   grep -c 'data-ob-lead="1"' appointment-request.html braces.html early-orthodontics.html \
     invisalign.html retainers.html contact.html   # expect 1 each
   grep -l 'not open yet' *.html                   # expect no output
   grep -c 'services.leadconnectorhq.com' appointment-request.html  # expect 2: action + config
   ```
7. **Check the confirmation page has no redirect hijacking it.** `vercel.json` currently
   has no `redirects` block, so there is nothing to remove. Re-check if one is added.
8. **Live test with parameters:**
   `/appointment-request?utm_source=google&utm_medium=cpc&utm_campaign=test&offer=test-offer&gclid=abc123`
   Submit, and confirm the browser lands on `/appointment-request-confirmation` and the GHL
   contact shows OB_Source=google, OB_Offer=test-offer, param_gclid=abc123.
9. **Cross-page attribution test:** load `/financing?utm_source=google&gclid=abc123`,
   navigate to `/appointment-request` with no parameters, submit, and confirm the contact
   still carries `google` and `abc123` from the stored first touch.
10. **Confirm the backup now sees GHL's verdict.** After the live test the lead on
    `leads.startorthoboost.com/dashboard/downtown-orthodontics` should move from
    `pending` to `delivered`, reported by `browser`. If it stays `pending` the
    `/api/lead-result` call is not landing, and the dashboard can no longer tell you
    what GHL dropped.
11. **Delete the test contacts** from GHL, including "Webhook Test (delete me)", and
    archive the test rows on the backup dashboard.
12. **Optional, recommended:** close the homepage attribution gap (§3).
13. **Remember the noindex.** Every page currently ships
    `<meta name="robots" content="noindex, nofollow" />` because `REVIEW_BUILD = True` in
    `build/chrome.py`. Flipping that is a separate launch step owned elsewhere, not part of
    form wiring. Note that the confirmation page is meant to stay noindex after launch,
    which is correct: a thank-you page has no business in search results.

---

## 8. Open items outside this wiring

- **Webhook URL not supplied.** CLIENT-BRIEF.md, Integrations. This blocks GHL
  delivery only. It no longer blocks lead capture: see §9.
- **Unresolved stack conflict.** CLIENT-BRIEF.md, Launch: Dr. Ty's brief names WordPress
  plus Elementor and Notion records client hosting, while this build is static on Vercel.
  If the site ships on WordPress instead, none of this Python wiring transfers; only the
  field contract in §3 does.
- **Call tracking.** The brief records CallTrackingMetrics feeding GHL. Nothing here
  touches phone attribution, and the tracking number appears nowhere in these forms.
- **No office notification email.** The backup platform can email the front desk on
  every lead (`scripts/set-notify.js` in the orthoboost-leads repo), but no practice
  email address is on file anywhere in this repo or in CLIENT-BRIEF.md. Until one is
  supplied, someone has to open the dashboard to see a lead. Get an address and this
  becomes a one-command fix.
- **No honeypot or fill-timer field.** The backup accepts optional `hp` and `elapsed`
  fields for spam scoring, and neither form sends them, so no submission is scored on
  those two signals. The platform's IP rate limit (5 per hour) still applies. Adding a
  honeypot means adding a hidden input to all three form templates, which was outside
  this change.

---

## 9. OrthoBoost Leads backup platform

**The delivery path that works today.** `leads.startorthoboost.com`, Next.js on Vercel
plus Neon Postgres; repo `OrthoBoost-Marketing/orthoboost-leads`. Every lead is stored
in Postgres *before* any GHL call, so a lead survives GHL being absent, unmapped or down.

| | |
|---|---|
| **site_id** | `downtown-orthodontics`, stable forever. Never rename it |
| **Mode** | **shadow** (`forward_to_ghl = false`): the platform records and never relays |
| **Registered webhook** | empty string, because none is on file. Honest, and nothing reads it in shadow mode |
| **Allowed origins** | `https://downtown-orthodontics-website.vercel.app`, `https://downtownorthodontics.ca`, `https://www.downtownorthodontics.ca` |
| **Dashboard** | `leads.startorthoboost.com/dashboard/downtown-orthodontics` (session login) |
| **Office email alerts** | off, no address on file |

All three origins were registered up front, so the DNS cutover to the real domain needs
no change here.

### Why shadow, not live

`forward_to_ghl = true` makes the *platform* relay to GHL server-side with retries. That
is only right for a site that posts **only** to `/api/lead`. This site posts to GHL
itself the moment a webhook exists, and reports the result back, so shadow is correct
both now and after cutover. Live mode today would also be actively harmful: the stored
webhook is empty, so every lead would be marked `failed` and retried eight times over
three days for nothing.

### What a lead looks like on the dashboard

`status` stays **`pending`** while no GHL webhook exists. That is the truth, not a
defect: the lead is captured and durable, and it has not reached GHL because there is no
GHL to reach. Nothing marks it `delivered` until either the browser reports a real GHL
2xx (§7 step 10) or someone works it by hand.

**Consequence, worth knowing:** the platform's 5-minute cron alerts on any non-archived
lead left undelivered for over 30 minutes, so every real lead captured here will raise
that alert until GHL exists. The alert is telling the truth. Archiving a row silences it
for that row (`archived_at`); the row stays visible on the dashboard.

### Payload contract

These keys are shared with every OrthoBoost client and must not be renamed: `Full Name`
(with the space), `Email`, `Phone`, `Offer` (capital O), and lowercase `utm_source`,
`utm_medium`, `utm_campaign`, `utm_content`, `gclid`, `fbclid`, `gbraid`, `wbraid`. This
site sends the whole §3 payload, and the platform additionally stores:

| Key | Source | Stored as |
|---|---|---|
| `site_id` | `LEADS_SITE_ID`, prepended by the script so no form field can overwrite it | the site row |
| `source_page` | `location.pathname`, path only, no query string | `source_page`; also what per-form routing rules match on |
| `form_name` | the form's `id`, e.g. `lead-braces` | `form_name` |
| `message` | the contact form's free-text box | `message` |

Everything else in the payload is passed through and ignored by the platform, by design:
the same body goes to GHL unchanged.

### Reading leads from a shell

```bash
# API_TOKEN comes from the orthoboost-leads project env (vercel env pull)
curl -H "Authorization: Bearer $API_TOKEN" \
  "https://leads.startorthoboost.com/api/leads?site=downtown-orthodontics&range=30d"
```

### Verifying the endpoint

```bash
curl -s -X POST "https://leads.startorthoboost.com/api/lead" \
  -H "Content-Type: application/json" \
  -H "Origin: https://downtown-orthodontics-website.vercel.app" \
  -d '{"site_id":"downtown-orthodontics","Full Name":"Test OrthoBoost Wiring","Email":"test@startorthoboost.com","Phone":"(604) 555-0100","utm_source":"wiring-test","source_page":"/appointment-request","form_name":"lead-appointment"}'
# expect: {"ok":true,"id":"N","mode":"shadow","token":"..."}
```

`{"error":"unknown_site"}` means the site row is gone. `{"error":"origin_not_allowed"}`
means the `Origin` header is not on the allowlist above, which is also why **a form on
`localhost` cannot reach the backup**: a JSON POST triggers a CORS preflight and
localhost is deliberately not allowlisted. Test forms from the Vercel URL, or stub
`window.fetch` locally. Vercel's per-deployment preview URLs
(`...-<hash>-ortho-boost.vercel.app`) are not allowlisted either; only the production
alias is.

Name any test lead "Test ..." so it is obviously deletable, and archive it when done.
