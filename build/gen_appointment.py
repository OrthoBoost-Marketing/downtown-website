"""Appointment request + confirmation.

APPOINTMENT-PAGE-SPEC free-consult template: short page, form inside the hero above
the fold, three risk-reversal checkmarks, proof-count line, phone fallback, a 3-step
what-happens block, one first-visit quote strip, and NO mid-page or final CTA band
(the whole page is the CTA).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chrome as C
import common
from common import fill, attribution_inputs, wire_form, leads_script

TICK = ('<svg width="17" height="17" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
        '<path d="M5 13l4 4L19 7" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>')

# ------------------------------------------------------------------ the form
# REQUEST-FORM-SPEC: exactly four fields plus at most one select. Zero PHI.
# The endpoint comes from GHL_WEBHOOK_URL in build/common.py, the single place it is
# set. While that is unset, wire_form() disables every control and inserts a notice
# pointing at the practice phone, so no lead is accepted or faked. See build/GHL-WIRING.md.
FORM_TPL = """        <div class="formcard reveal d1">
          <h2>Request your free consultation</h2>
          <form method="post" action="" novalidate>
            <div class="fgrid">
              <div class="field">
                <label for="f-first">First name</label>
                <input id="f-first" name="first_name" type="text" autocomplete="given-name" required />
              </div>
              <div class="field">
                <label for="f-last">Last name</label>
                <input id="f-last" name="last_name" type="text" autocomplete="family-name" required />
              </div>
              <div class="field">
                <label for="f-phone">Phone</label>
                <input id="f-phone" name="phone" type="tel" autocomplete="tel" required />
              </div>
              <div class="field">
                <label for="f-email">Email</label>
                <input id="f-email" name="email" type="email" autocomplete="email" required />
              </div>
              <div class="field wide">
                <label for="f-interest">I&rsquo;m interested in</label>
                <select id="f-interest" name="interest">
                  <option>Not sure yet, help me choose</option>
                  <option>Braces, metal or clear</option>
                  <option>Invisalign or Quick 6 Fix</option>
                  <option>Kids&rsquo; first visit and early care</option>
                  <option>Retainers and aftercare</option>
                </select>
              </div>
            </div>
%(attribution)s
            <button class="btn btn-primary" type="submit">Request my free consultation <span class="arr">&rarr;</span></button>
          </form>
          <p class="microline">Your consultation is free and there is no obligation to start.
            We only ask for a name, a phone number and an email, never health details:
            Dr. Daher covers all of that with you in person.</p>
          <noscript>
            <p class="microline">This form needs JavaScript to send your request. Please call
              the practice on <a class="tlink" href="tel:+16046623290">(604) 662-3290</a>.</p>
          </noscript>
        </div>""" % {"attribution": attribution_inputs(
    "appointment-request", offer="$1,000 off full treatment")}

FORM = wire_form(FORM_TPL, "lead-appointment")

BODY = """
  <!-- HERO with the form, above the fold (free-consult template) -->
  <section class="phero" id="top">
    <div class="wrap">
      <div class="reqgrid">
        <div class="reqcopy reveal">
          <p class="crumb"><a href="/">Home</a><span>&middot;</span>Free consultation</p>
          <span class="eyebrow">Free consult &middot; Downtown Vancouver</span>
          <h1>Schedule your <em>free consultation.</em></h1>
          <p class="sub">One visit with Dr. Daher, a certified specialist in
            orthodontics. You will leave knowing exactly what your bite needs, what it costs,
            and whether to start now or wait.</p>
          <ul class="checks">
            <li>%(tick)s<span><b>The consultation is free</b>, including the digital scan and
              Dr. Daher&rsquo;s read on your bite. No referral needed.</span></li>
            <li>%(tick)s<span><b>Your exact price in writing</b> before you decide. Most plans
              start at $1,000 down and from $220 a month at 0%% in-house interest.</span></li>
            <li>%(tick)s<span><b>We reply the same business day.</b> If you would rather not wait,
              call and we will book you on the spot.</span></li>
          </ul>
          <div class="hero-cred" style="margin-top:var(--sp-7);">
            <span>%(tick)s 900 patients treated</span>
            <span>%(tick)s 30+ years, one specialist</span>
            <span>%(tick)s By Canada Place</span>
          </div>
          <p class="promise" style="margin-top:var(--sp-6);">Rather talk to someone now?</p>
          <a class="big-tel" href="tel:+16046623290"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 006.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 013 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.2.2 2.4.6 3.6.1.4 0 .7-.2 1l-2.3 2.2z" fill="currentColor"/></svg> (604) 662-3290</a>
        </div>
%(form)s
      </div>
    </div>
  </section>

  <!-- WHAT HAPPENS (3 numbered steps, ~110 words) -->
  <section class="block">
    <div class="wrap">
      <div class="sec-head reveal">
        <span class="eyebrow">(What happens)</span>
        <h2 class="h2">Your free consultation, <em>start to finish.</em></h2>
      </div>
      <ol class="steps reveal d1">
        <li>
          <h3>A scan, not a sales pitch</h3>
          <p>We capture your teeth in a few minutes with a digital scanner, no impression
            trays, then put the images on screen so you can see what Dr. Daher sees.</p>
        </li>
        <li>
          <h3>A specialist reads your bite</h3>
          <p>Dr. Daher explains what is actually happening in plain language, which options
            genuinely suit it, and where braces and Invisalign differ for your case. Both are
            planned by a specialist here, so the recommendation is about your bite.</p>
        </li>
        <li>
          <h3>Your plan and your price, in writing</h3>
          <p>Timeline, options and full cost before you leave, with your insurance checked
            during the visit. Start whenever you are ready, or not at all.</p>
        </li>
      </ol>
    </div>
  </section>

  <!-- ONE first-visit quote strip. SPEC wants a verbatim first-visit testimonial;
       none is on file, so the slot ships visibly empty rather than invented. -->
  <section class="block" style="background:var(--surface);">
    <div class="wrap">
      <div class="reveal" style="max-width:760px;">
        <h2 class="eyebrow">(In their words)</h2>
        <p class="slot">Placeholder: a first-visit review goes here, quoted verbatim from the
          practice&rsquo;s Google profile with attribution. No client-approved quotes are on file
          yet, and this build does not invent them.</p>
      </div>
    </div>
  </section>
""" % {"tick": TICK, "form": FORM} + leads_script()

SCHEMA = """{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": "Request a free orthodontic consultation",
  "url": "https://downtownorthodontics.ca/appointment-request",
  "isPartOf": { "@id": "https://downtownorthodontics.ca/#practice" },
  "about": { "@id": "https://downtownorthodontics.ca/#practice" },
  "primaryImageOfPage": "https://downtownorthodontics.ca/assets/photos/used-3.jpg"
}"""

C.write("appointment-request.html", C.page(
    title="Book a Free Consultation | Downtown Vancouver Orthodontist",
    desc="Book a free consultation with specialist orthodontist Dr. Sam Daher in downtown Vancouver. Digital scan, honest options, exact price in writing.",
    slug="appointment-request",
    body=BODY,
    schema=SCHEMA,
))

# ------------------------------------------------------------------ confirmation
CONF_BODY = fill("""
  <section class="phero" id="top">
    <div class="wrap">
      <div class="phero-narrow reveal">
        <span class="eyebrow">Request received</span>
        <h1>Thank you. <em>We have your request.</em></h1>
        <p class="sub">Someone from Dr. Daher&rsquo;s front desk will call you the same business
          day to find a time that works. If you sent this over a weekend, expect us Monday
          morning.</p>
        <div class="pactions">
          <a class="btn btn-outline" href="tel:+16046623290">Call (604) 662-3290</a>
        </div>
      </div>
    </div>
  </section>

  <section class="block">
    <div class="wrap">
      <div class="sec-head reveal">
        <span class="eyebrow">(What happens next)</span>
        <h2 class="h2">Three things, <em>in order.</em></h2>
      </div>
      <ol class="steps reveal d1">
        <li>
          <h3>We call to book you in</h3>
          <p>A short call to pick a time. Tell us then if you need an early slot before work,
            or an after-school one for a child.</p>
        </li>
        <li>
          <h3>We check your insurance first</h3>
          <p>Bring your plan details and we will confirm your orthodontic coverage before your
            visit, so the numbers you hear on the day are real ones.</p>
        </li>
        <li>
          <h3>You meet Dr. Daher</h3>
          <p>A digital scan, a specialist&rsquo;s read on your bite, and your full plan and price
            in writing before you leave. Free, with no obligation to start.</p>
        </li>
      </ol>
    </div>
  </section>

  <!-- "While you wait" cards route back into the site: this page's real job -->
  <section class="block" style="background:var(--surface);">
    <div class="wrap">
      <div class="sec-head reveal">
        <h2 class="h2">While you wait.</h2>
      </div>
      <div class="paths-grid">
        <a class="path reveal" href="/dr-sam-daher">
          <div class="body">
            <div class="lbl">The doctor</div>
            <h3>Who you will <em>actually see.</em></h3>
            <p>Thirty years, the world&rsquo;s first Invisalign-only practice, and a seat on Align
              Technology&rsquo;s scientific advisory board. The full record.</p>
            <span class="go">Meet Dr. Daher <span class="arr">&rarr;</span></span>
          </div>
        </a>
        <a class="path reveal d1" href="/financing">
          <div class="body">
            <div class="lbl">Pricing</div>
            <h3>What it <em>costs.</em></h3>
            <p>$1,000 down, from $220 a month at 0% in-house interest, insurance billed
              directly, and the two ways to pay less.</p>
            <span class="go">See pricing <span class="arr">&rarr;</span></span>
          </div>
        </a>
        <a class="path reveal d2" href="/faq">
          <div class="body">
            <div class="lbl">Questions</div>
            <h3>The things <em>families ask first.</em></h3>
            <p>Cost, timing, whether your child is too young, whether you are too old, and what
              happens if you move partway through.</p>
            <span class="go">Read the answers <span class="arr">&rarr;</span></span>
          </div>
        </a>
      </div>
    </div>
  </section>

  <!-- "NEED US SOONER?" band. UTILITY-PAGES-SPEC requires phone + hours here,
       before the footer. Same number and same hours as contact.html. -->
  <section class="block" style="border-top:var(--border) solid var(--line);">
    <div class="wrap">
      <div class="reqgrid">
        <div class="reveal">
          <span class="eyebrow">(Need us sooner?)</span>
          <h2 class="h2">Call the practice <em>directly.</em></h2>
          <p class="promise">If something has come up, or you would rather not wait for our call,
            the front desk can book you in over the phone.</p>
          <a class="big-tel" href="tel:+16046623290">__PHONE__ (604) 662-3290</a>
        </div>
        <div class="reveal d1">
          <ul class="checks" style="margin-top:0;">
            <li>__TICK__<span><b>Monday</b> 10:00 to 18:00</span></li>
            <li>__TICK__<span><b>Tuesday</b> 08:00 to 15:00</span></li>
            <li>__TICK__<span><b>Wednesday</b> 08:00 to 16:30</span></li>
            <li>__TICK__<span><b>Thursday</b> 08:00 to 15:00</span></li>
            <li>__TICK__<span style="color:var(--ink-faint);">Friday to Sunday, closed</span></li>
          </ul>
        </div>
      </div>
    </div>
  </section>
""") + leads_script()
# The confirmation page loads the same script so the ob_generate_lead event fires here,
# on the conversion URL. It is a one-shot flag set at submit time, so arriving at this
# page directly fires nothing.

# UTILITY-PAGES-SPEC mobile nuance: the visitor has already converted, so this
# page's sticky-bar centre segment becomes an explore action instead of "Book".
# Asserted single replacement on this page's own HTML: the shared bar that the
# other 16 pages get is untouched.
_MBAR_BOOK = """    <a class="primary" href="/appointment-request">
      <svg width="17" height="17" viewBox="0 0 24 24" fill="none" aria-hidden="true"><rect x="3" y="5" width="18" height="16" rx="3" stroke="currentColor" stroke-width="1.8"/><path d="M3 10h18M8 3v4M16 3v4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>
      Book free consult
    </a>"""
_MBAR_EXPLORE = """    <a class="primary" href="/dr-sam-daher">
      <svg width="17" height="17" viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="12" cy="8" r="3.4" stroke="currentColor" stroke-width="1.8"/><path d="M4.8 20a7.6 7.6 0 0114.4 0" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>
      Meet Dr. Daher
    </a>"""

_conf = C.page(
    noindex=True,   # a thank-you page has no business in search results
    title="Request Received | Downtown Orthodontics",
    desc="Your free consultation request has been received. Dr. Daher's front desk will call you the same business day.",
    slug="appointment-request-confirmation",
    body=CONF_BODY,
)
assert _conf.count(_MBAR_BOOK) == 1, "confirmation sticky-bar centre segment not found exactly once"
_conf = _conf.replace(_MBAR_BOOK, _MBAR_EXPLORE)
# NB: the HEADER CTA also carries a "Book free consult" short label; that one
# stays. Only the sticky bar's centre segment changes on this page.
assert _conf.count(_MBAR_EXPLORE) == 1
assert _MBAR_BOOK not in _conf

C.write("appointment-request-confirmation.html", _conf)
