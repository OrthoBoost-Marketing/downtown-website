# GoHighLevel lead wiring, Downtown Orthodontics

Status: **built, not connected.** Every lead form on the site is wired end to end except
for the endpoint itself, which is not on file yet (CLIENT-BRIEF.md, Integrations:
"ghl webhook: NOT SUPPLIED"). At cutover you set one string and re-run the build.

---

## 1. The one thing to set at cutover

**File:** `build/common.py`
**Line:** **26**

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
| `LEAD_CONFIRM_URL` | 32 | `/appointment-request-confirmation` | where a successful submit redirects |
| `LEAD_ATTR_DAYS` | 42 | `90` | first-touch attribution lifetime, in days |
| `LEAD_QUEUE_DAYS` | 47 | `30` | failed-lead backup lifetime, in days |

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
<script>window.OB_LEADS = {"attr_days": 90, "confirm": "/appointment-request-confirmation", "endpoint": "", "phone": "(604) 662-3290", "queue_days": 30, "tel": "+16046623290"};</script>
<script src="/assets/js/ob-leads.js" defer></script>
```

Better: move the call into `build/chrome.py`'s `page()` so every page gets it from the one
constant. That file is also owned separately.

Pages that currently load the script: the six form pages, the confirmation page,
`dr-sam-daher`, `why-choose-us`, `reviews`, `financing`, `faq`. Deliberately excluded:
`privacy-policy`, `terms`, `accessibility`, `404`, and `index.html`.

---

## 4. Fail-safe behaviour while the endpoint is unset

While `GHL_WEBHOOK_URL` is `""`, the generators render every lead form in a disabled
state:

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

Setting the constant reverses all of this on the next build: forms become interactive,
`data-ob-lead="1"`, the notice disappears and `action` points at the webhook.

**If the client needs to see a live-looking form during review before the webhook
exists,** there is no switch for that on purpose. Ask for the webhook, or accept the
notice.

---

## 5. Submit path when the endpoint is set

1. The form stays a real `<form method="post" action="<webhook>">`, so it is not a
   JS-only trap. `assets/js/ob-leads.js` intercepts submit and posts JSON instead.
2. Hidden attribution inputs are filled from the URL and stored first touch.
3. `form.checkValidity()` runs. The forms carry `novalidate` so one message can be shown
   in place, but the `required` attributes are real and still enforced here. The first
   invalid field is focused.
4. `fetch` POSTs `application/json` with `keepalive`. GHL's webhook trigger only parses
   JSON, and its CORS headers allow this request straight from the browser.
5. On a non-2xx response or a network error, the lead is queued locally (§6) and the
   visitor is shown the practice number.
6. On success the `ob_generate_lead` event fires and the browser redirects to
   `/appointment-request-confirmation`.

**No-JavaScript caveat.** With JS disabled the native POST would send
`application/x-www-form-urlencoded`, which GHL's webhook trigger is not known to parse
(`text/plain` is documented to fail; urlencoded is untested here). So the native action is
a real action but not a verified delivery path. Every form therefore also carries a
`<noscript>` block telling the visitor to call the practice. Do not claim the no-JS path
works until someone tests it against the real endpoint.

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

## 6. Local leads backup

Server-free, so a failed or unset submit never silently loses a lead.

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

The script also retries the queue quietly on the next page load once the endpoint is set,
removing entries that go through. A retry can create a duplicate contact if the original
POST actually landed but its response was unreadable; GHL's create/update contact action
collapses those by email and phone.

This queue lives only in the visitor's own browser. It is a last-resort safety net for
the person in front of the screen, not a lead database the practice can query. The real
backup is the OrthoBoost Leads platform (`orthoboost-leads-connect`), which is **not**
wired here: it needs a site registration and was out of scope.

### Other storage this site's forms use

| Key | Store | Expiry | Purpose |
|---|---|---|---|
| `ob_attr_first_touch_v1` | localStorage | **90 days** (`LEAD_ATTR_DAYS`), checked and dropped on read | first-touch attribution |
| `ob_attr_first_touch_v1` | sessionStorage | the browser session | mirror, for when localStorage is blocked but sessionStorage is not |
| `ob_lead_queue_v1` | localStorage | 30 days | failed-lead backup |
| `ob_lead_event_pending_v1` | sessionStorage | one-shot, deleted on read | fires `ob_generate_lead` on the confirmation page |

**No cookie is set anywhere by these forms.** A never-expiring attribution cookie is a
known defect in the OrthoBoost WordPress plugin, and it is avoided here by not using
cookies at all. Every stored record carries its own explicit expiry and is dropped when
past it. Every storage access is wrapped in `try/catch`, because private-browsing modes
throw on the storage property itself, not just on write.

---

## 7. Cutover checklist

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
4. **Set the constant:** `GHL_WEBHOOK_URL` in `build/common.py`, line 26.
5. **Re-run the generators** to regenerate the 16 pages.
6. **Confirm the forms came out live:**
   ```bash
   grep -c 'data-ob-lead="1"' appointment-request.html braces.html early-orthodontics.html \
     invisalign.html retainers.html contact.html   # expect 1 each
   grep -c 'not open yet' *.html                   # expect 0 everywhere
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
10. **Delete the test contacts** from GHL, including "Webhook Test (delete me)".
11. **Optional, recommended:** close the homepage attribution gap (§3) and register the
    site with the OrthoBoost Leads backup platform (§6).
12. **Remember the noindex.** Every page currently ships
    `<meta name="robots" content="noindex, nofollow" />` because `REVIEW_BUILD = True` in
    `build/chrome.py`. Flipping that is a separate launch step owned elsewhere, not part of
    form wiring. Note that the confirmation page is meant to stay noindex after launch,
    which is correct: a thank-you page has no business in search results.

---

## 8. Open items outside this wiring

- **Webhook URL not supplied.** CLIENT-BRIEF.md, Integrations. This is the blocker.
- **Unresolved stack conflict.** CLIENT-BRIEF.md, Launch: Dr. Ty's brief names WordPress
  plus Elementor and Notion records client hosting, while this build is static on Vercel.
  If the site ships on WordPress instead, none of this Python wiring transfers; only the
  field contract in §3 does.
- **Call tracking.** The brief records CallTrackingMetrics feeding GHL. Nothing here
  touches phone attribution, and the tracking number appears nowhere in these forms.
- **OrthoBoost Leads backup platform** not connected, see §6.
