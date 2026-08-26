"""Appointment request + confirmation.

APPOINTMENT-PAGE-SPEC free-consult template: short page, form inside the hero above
the fold, three risk-reversal checkmarks, proof-count line, phone fallback, a 3-step
what-happens block, one first-visit quote strip, and NO mid-page or final CTA band
(the whole page is the CTA).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chrome as C

TICK = ('<svg width="17" height="17" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
        '<path d="M5 13l4 4L19 7" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>')

# ------------------------------------------------------------------ the form
# REQUEST-FORM-SPEC: exactly four fields plus at most one select. Zero PHI.
# Hidden attribution set is present but unwired: the GHL webhook URL is not on file
# (CLIENT-BRIEF.md, Integrations). orthoboost-ghl-forms + orthoboost-leads-connect
# finish this at launch.
FORM = """        <div class="formcard reveal d1">
          <h2>Request your free consult</h2>
          <form id="request-form" method="post" action="" novalidate>
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
            <!-- Attribution. Populated from URL params and a first-touch cookie at launch. -->
            <input type="hidden" name="utm_source" value="" />
            <input type="hidden" name="utm_medium" value="" />
            <input type="hidden" name="utm_campaign" value="" />
            <input type="hidden" name="utm_term" value="" />
            <input type="hidden" name="utm_content" value="" />
            <input type="hidden" name="gclid" value="" />
            <input type="hidden" name="fbclid" value="" />
            <input type="hidden" name="offer" value="$1,000 off full treatment" />
            <input type="hidden" name="page" value="appointment-request" />
            <button class="btn btn-primary" type="submit">Request my free consult <span class="arr">&rarr;</span></button>
          </form>
          <p class="microline">Your consultation is free and there is no obligation to start.
            We only ask for a name, a phone number and an email, never health details:
            Dr. Daher covers all of that with you in person.</p>
          <!-- NOT WIRED YET: no GHL webhook URL on file. See CLIENT-BRIEF.md, Integrations. -->
        </div>"""

BODY = """
  <!-- HERO with the form, above the fold (free-consult template) -->
  <section class="phero" id="top">
    <div class="wrap">
      <div class="reqgrid">
        <div class="reqcopy reveal">
          <p class="crumb"><a href="/">Home</a><span>&middot;</span>Free consultation</p>
          <span class="eyebrow">Free consult &middot; Downtown Vancouver</span>
          <h1>Schedule your <em>free consult.</em></h1>
          <p class="sub">One visit with Dr. Daher, a certified specialist in
            orthodontics. You will leave knowing exactly what your bite needs, what it costs,
            and whether to start now or wait.</p>
          <ul class="checks">
            <li>%(tick)s<span><b>The consultation is free</b>, including the digital scan and
              Dr. Daher&rsquo;s read on your bite. No referral needed.</span></li>
            <li>%(tick)s<span><b>Your exact price in writing</b> before you decide. Most plans
              start at $1,000 down and about $220 a month at 0%% in-house interest.</span></li>
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
        <h2 class="h2">Your free consult, <em>start to finish.</em></h2>
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
        <span class="eyebrow">(In their words)</span>
        <p class="slot">Placeholder: a first-visit review goes here, quoted verbatim from the
          practice&rsquo;s Google profile with attribution. No client-approved quotes are on file
          yet, and this build does not invent them.</p>
      </div>
    </div>
  </section>
""" % {"tick": TICK, "form": FORM}

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
    title="Book a Free Orthodontic Consultation | Downtown Orthodontics Vancouver",
    desc="Book a free consultation with Dr. Sam Daher, a certified specialist in orthodontics in downtown Vancouver. Digital scan, honest options and your exact price in writing. No referral needed.",
    slug="appointment-request",
    body=BODY,
    schema=SCHEMA,
))

# ------------------------------------------------------------------ confirmation
CONF_BODY = """
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
"""

C.write("appointment-request-confirmation.html", C.page(
    title="Request Received | Downtown Orthodontics",
    desc="Your free consultation request has been received. Dr. Daher's front desk will call you the same business day.",
    slug="appointment-request-confirmation",
    body=CONF_BODY,
))
