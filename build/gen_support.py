"""Financing, FAQ and contact pages."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chrome as C
from common import TICK, PHONE, phero, cta_band, faq_rows, fill, faq_schema
from common import attribution_inputs, wire_form, leads_script, quote_card

# ==================================================================== FINANCING
# FINANCIAL-AND-FAQ-PAGE-SPEC: commercial-query H1, the monthly anchor repeated and
# always tethered to "your exact figure comes from the free consultation", the
# four-paragraph insurance explainer, and a payment-specific testimonial.
FIN_FAQS = [
    ("How much do braces cost in downtown Vancouver?",
     "Most treatment here starts at $1,000 down and from $220 a month with 0% in-house financing. Simple Invisalign Express cases run a $4,299 flat rate. Every bite is different, so your exact figure comes from your free consultation, in writing, before you commit to anything."),
    ("Who decides whether I need braces or Invisalign?",
     "Dr. Daher does, at your consultation, and he plans and adjusts both himself. That matters more than it sounds: recommending between braces and Invisalign takes a specialist who plans both. You get your exact figure for whichever option suits your bite, in writing, before you commit to anything."),
    ("Is the financing really 0% interest?",
     "Yes. It is arranged in-house rather than through a third-party lender, so there is no interest and no credit application to a finance company. $1,000 down, then a monthly amount agreed before treatment starts."),
    ("Do you bill my insurance directly?",
     "Yes, we bill your plan directly rather than handing you paperwork to chase. Bring your plan details to the consultation and we will confirm your orthodontic coverage during the visit, so the numbers you hear on the day are real ones."),
    ("What if I do not have insurance?",
     "Most of our patients pay through the in-house plan and a good share have no orthodontic coverage at all. $1,000 down and from $220 a month at 0% interest is the same offer either way. Insurance reduces what you pay; it is not what makes treatment possible."),
    ("Are there ways to pay less?",
     "Two. Pay in full and save 5%, or save $450 by starting the same day as your consultation. There is also $1,000 off full treatment for braces or Invisalign. We apply whatever you qualify for and show it on the written plan."),
]
fin_rows, fin_schema = faq_rows(FIN_FAQS)

FIN_BODY = phero(
    "Pricing &amp; financing", "Pricing",
    "Braces payment plans in <em>downtown Vancouver.</em>",
    "$1,000 down, from $220 a month at 0% in-house interest, insurance billed directly, and "
    "your full cost in writing before you decide. No asterisks.",
) + fill("""
  <section class="bg-petrol-deep text-white tw-block">
    <div class="wrap" style="padding-top:var(--section-y);">
      <div class="sec-head reveal" style="margin-bottom:clamp(30px,4vw,44px);">
        <h2 class="h2" style="color:#fff;">The whole arrangement, <em style="color:var(--teal);">in four numbers.</em></h2>
        <p style="color:rgba(255,255,255,.72);">Your exact figure comes from your free consultation.
          These are the terms it gets built on.</p>
      </div>
    </div>
    <div class="wrap grid grid-cols-2 gap-x-6 gap-y-10 md:grid-cols-4 md:gap-x-10">
      <div class="reveal text-center md:text-left">
        <div class="count leading-none tracking-tight text-teal" style="font-size:var(--fs-figure)" data-count="1000" data-prefix="$">0</div>
        <div class="mt-2.5 text-sm font-medium text-white/65">down, and that&rsquo;s all to start</div>
      </div>
      <div class="reveal d1 text-center md:text-left">
        <div class="count leading-none tracking-tight text-teal" style="font-size:var(--fs-figure)" data-count="220" data-prefix="$" data-suffix="/mo">0</div>
        <div class="mt-2.5 text-sm font-medium text-white/65">braces from, on a monthly plan</div>
      </div>
      <div class="reveal d2 text-center md:text-left">
        <div class="count leading-none tracking-tight text-teal" style="font-size:var(--fs-figure)" data-count="0" data-suffix="%">0</div>
        <div class="mt-2.5 text-sm font-medium text-white/65">interest, financed in-house</div>
      </div>
      <div class="reveal d3 text-center md:text-left">
        <div class="count leading-none tracking-tight text-teal" style="font-size:var(--fs-figure)" data-count="100" data-suffix="%">0</div>
        <div class="mt-2.5 text-sm font-medium text-white/65">of your insurance billed directly</div>
      </div>
    </div>
    <div class="wrap reveal" style="padding-bottom:var(--section-y);">
      <div class="hero-actions" style="margin-top:clamp(34px,5vw,52px);align-items:center;">
        <a class="btn btn-primary" href="/appointment-request">Get your exact price, free <span class="arr">&rarr;</span></a>
        <span class="text-sm font-medium text-white/55">Pay in full and save 5%, or save $450 when you start the same day.</span>
      </div>
    </div>
  </section>

  <section class="block">
    <div class="wrap">
      <div class="sec-head reveal">
        <span class="eyebrow">(What is included)</span>
        <h2 class="h2">What the monthly figure <em>actually covers.</em></h2>
        <p>Your exact figure comes from your free consultation. Whatever it turns out to be, this is
          what sits inside it.</p>
      </div>
      <ul class="checks reveal d1" style="max-width:760px;">
        <li>__TICK__<span><b>Every appointment with Dr. Daher.</b> A certified specialist at each
          adjustment, not a rotating cast.</span></li>
        <li>__TICK__<span><b>Digital scans and records.</b> No impression trays, and no separate
          imaging invoice.</span></li>
        <li>__TICK__<span><b>Your exact figure in writing.</b> Before you commit to anything, for
          whichever option suits your bite.</span></li>
        <li>__TICK__<span><b>Refinement to finish it properly.</b> If the result needs extra work to
          be right, that is part of the plan.</span></li>
        <li>__TICK__<span><b>Clear retainers and a retention plan</b> at the end, checked by
          Dr. Daher himself.</span></li>
        <li>__TICK__<span><b>Your full cost in writing</b> before anything begins. No surprise fees
          at the end.</span></li>
      </ul>
    </div>
  </section>

  <section class="block" style="background:var(--surface);">
    <div class="wrap">
      <div class="sec-head reveal">
        <span class="eyebrow">(Insurance)</span>
        <h2 class="h2">How dental insurance <em>actually works here.</em></h2>
      </div>
      <div class="prose reveal d1">
        <h3>A benefit is not a payment plan</h3>
        <p>Orthodontic coverage is usually a lifetime maximum: a fixed pot your plan will put toward
          treatment across your whole life, not a percentage of every visit. It is worth knowing
          that number before you start, because it changes what the monthly figure looks like rather
          than whether treatment is possible at all.</p>
        <h3>We file it for you</h3>
        <p>We bill your plan directly instead of handing you forms to submit and chase. Bring your
          plan details to the free consultation and we will confirm your orthodontic coverage during
          the visit, so the figures on your written plan already account for it.</p>
        <h3>In network, out of network</h3>
        <p>Most plans that include orthodontics will contribute here. What differs between plans is
          how much and how quickly, not whether you can be treated. We will tell you what your
          specific plan does before you commit, including if the honest answer is that it contributes
          very little.</p>
        <h3>And if you have no coverage at all</h3>
        <p>A good share of our patients have none. The in-house plan is the same either way:
          $1,000 down, from $220/mo, 0% interest. Insurance lowers what you pay. It is not the
          thing that makes treatment affordable.</p>
      </div>
    </div>
  </section>

  <!-- NUMBERED PROCESS STEPPER. Spec anatomy puts this between the insurance
       explainer and the payment testimonial. Same .steps <ol> as the appointment
       page. Every figure is already published above. -->
  <section class="block">
    <div class="wrap">
      <div class="sec-head reveal">
        <span class="eyebrow">(How paying for it works)</span>
        <h2 class="h2">Four steps, <em>and you know the number.</em></h2>
      </div>
      <ol class="steps steps-4 reveal d1">
        <li>
          <h3>Book the free consultation</h3>
          <p>No referral, no fee, and no commitment. Bring your insurance details and we will
            check your orthodontic coverage during the visit.</p>
        </li>
        <li>
          <h3>Get your plan and your exact figure</h3>
          <p>A digital scan, a specialist&rsquo;s read on your bite, and your full cost in writing
            before you leave. Not a range: your number.</p>
        </li>
        <li>
          <h3>$1,000 down when you start</h3>
          <p>That is all treatment takes to begin. Pay in full instead and save 5%, or save $450
            by starting the same day as your consultation.</p>
        </li>
        <li>
          <h3>Monthly at 0% in-house</h3>
          <p>From $220 a month, financed in-house rather than through a lender, so there is
            no interest and no finance application. We bill your insurance directly.</p>
        </li>
      </ol>
    </div>
  </section>

  <section class="block">
    <div class="wrap" style="max-width:760px;">
      <div class="reveal">
        <h2 class="eyebrow">(In their words)</h2>
        __QUOTE__
      </div>
    </div>
  </section>

  <section class="block faq" style="background:var(--surface);">
    <div class="wrap">
      <div class="sec-head center reveal">
        <span class="eyebrow">(Money questions)</span>
        <h2 class="h2">What people ask <em>about paying for it.</em></h2>
      </div>
      <div class="faq-list reveal d1">__ROWS__
      </div>
    </div>
  </section>
""", rows=fin_rows,
         # Riaz Meghji, "Worth it": the only review on the profile that speaks to
         # price, so it belongs here even though the homepage marquee also uses it.
         quote=quote_card(4, "Adult treatment", indent=8)) + cta_band(
    "Get your exact price, <em>free.</em>",
    "One visit, a digital scan, and a written plan with the full cost on it. No obligation to start.",
    "$1,000 down, from $220/mo at 0% in-house financing. Insurance billed directly.")

C.write("financing.html", C.page(
    title="Braces Payment Plans, Downtown Vancouver | 0% Financing",
    desc="Braces and Invisalign payment plans in downtown Vancouver: $1,000 down, from $220/mo at 0% in-house interest, insurance billed directly.",
    slug="financing", body=FIN_BODY + leads_script(),
    schema='{\n  "@context": "https://schema.org",\n  "@type": "FAQPage",\n  "isPartOf": { "@id": "https://downtownorthodontics.ca/#practice" },\n  "about": { "@id": "https://downtownorthodontics.ca/#practice" },\n  "mainEntity": [\n%s\n  ]\n}' % fin_schema))

# ==================================================================== FAQ
FAQS = [
    ("How much does orthodontic treatment cost in downtown Vancouver?",
     "Most treatment starts at $1,000 down and from $220 a month with 0% in-house financing, and we bill your insurance directly. Simple Invisalign Express cases run a $4,299 flat rate. Every bite is different, so you get your exact price in writing at your free consultation."),
    ("When should our child first see an orthodontist?",
     "Around age seven. Most children will not need anything done yet, but an early check lets Dr. Daher see how the jaw is growing and catch anything worth watching while it is still easy to influence. That first visit is always free."),
    ("I am 40. Is it too late for me?",
     "Not at all. A good share of our patients are downtown professionals, and bone responds to the same forces at forty as at fourteen. Invisalign keeps it discreet enough that most people will not notice a thing, until they see the result."),
    ("Who will actually be treating us?",
     "Dr. Daher, from your first visit to your last. He is a certified specialist in orthodontics with over 30 years in practice, and you will see the same doctor and the same small team throughout, with no rotating faces and no handoffs."),
    ("Braces or Invisalign: how do we choose?",
     "At your consultation we will walk through both honestly for your specific smile. Some cases do beautifully with Invisalign; others are better and faster with braces. Dr. Daher plans and adjusts both himself, so the recommendation you get is about your bite, not our margin."),
    ("How long does treatment usually take?",
     "Treatment length depends on what your bite actually needs, so you will get a realistic timeline for your own case at your consultation rather than a range that may not apply to you. Simple express cases finish considerably sooner, which is the point of the Quick 6 Fix, and we will keep you updated as you progress."),
    ("What about retainers when we are done?",
     "Every plan finishes with clear retainers and a retention plan, because teeth drift if you let them. Dr. Daher checks your retention himself, and if an old retainer has stopped fitting, we can help with that too."),
    ("What if we move partway through treatment?",
     "It happens, and we make it painless. We will prepare your records and help transfer your care to a trusted orthodontist near your new home, with your treatment plan fully documented so nothing has to be worked out twice."),
    ("Do we need a referral from our dentist?",
     "No. You can book a free consultation directly and most of our patients do. If your dentist has referred you, bring anything they sent and Dr. Daher will factor it in, but it is not a requirement."),
    ("Do you treat complex cases other offices have declined?",
     "Regularly. Referred cases and bites that have already been turned down elsewhere are a normal part of the week here. Dr. Daher's rule is the least treatment that gets the right result, which often means finding an approach somebody else did not."),
]
# (id, eyebrow, visible h2, short jump label, indices into FAQS)
FAQ_GROUPS = [
    ("cost-and-getting-started", "(Money and first steps)",
     "Cost and <em>getting started.</em>", "Cost &amp; getting started", [0, 8, 3]),
    ("is-it-right-for-us", "(Who it is for)",
     "Is orthodontics <em>right for us?</em>", "Is it right for us?", [1, 2, 4, 9]),
    ("treatment-and-afterwards", "(During and after)",
     "Treatment, timing <em>and afterwards.</em>", "Treatment &amp; afterwards", [5, 6, 7]),
]
# every question used exactly once, none invented, none dropped
assert sorted(i for g in FAQ_GROUPS for i in g[4]) == list(range(len(FAQS))), "FAQ grouping lost a question"
assert FAQ_GROUPS[0][4][0] == 0, "the cost+city question must stay first in its group"

# Visible order and schema order are the same list, so they cannot drift.
# TIER 3 (4): five of these ten questions are ALREADY marked up as FAQPage on another
# URL - four on index.html and one on early-orthodontics.html. Google disqualifies FAQ
# markup duplicated across URLs, so both copies lose. Each question is therefore marked
# up on exactly one page. All ten stay VISIBLE here, in their groups: only the JSON-LD
# is trimmed. Indices are into FAQS.
FAQ_SCHEMA_SKIP = {
    1,  # "When should our child first see an orthodontist?" -> early-orthodontics.html
    3,  # "Who will actually be treating us?"                -> index.html
    4,  # "Braces or Invisalign: how do we choose?"          -> index.html
    5,  # "How long does treatment usually take?"            -> index.html
    7,  # "What if we move partway through treatment?"       -> index.html
    6,  # "What about retainers when we are done?"         -> index.html (near-duplicate wording)
}
# Schema order follows visible order, so the two cannot drift.
FAQ_SCHEMA_ITEMS = [FAQS[i] for g in FAQ_GROUPS for i in g[4] if i not in FAQ_SCHEMA_SKIP]
# 4, not 5: "What about retainers when we are done?" was added to the skip list on
# 2026-08-26 because index.html marks up the same question with "we're done", which is
# a cross-URL duplicate in substance even though the bytes differ.
assert len(FAQ_SCHEMA_ITEMS) == len(FAQS) - len(FAQ_SCHEMA_SKIP) == 4, "FAQ schema subset drifted"
_, faq_schema = faq_rows(FAQ_SCHEMA_ITEMS)

faq_jump = '<nav class="faq-jump reveal" aria-label="Question categories">%s</nav>' % "".join(
    '<a href="#%s">%s</a>' % (g[0], g[3]) for g in FAQ_GROUPS)

faq_groups_html = "".join(
    fill("""
  <section class="block faq" id="__ID__"__BG__>
    <div class="wrap">
      <div class="sec-head center reveal">
        <span class="eyebrow">__EYEBROW__</span>
        <h2 class="h2">__H2__</h2>
      </div>
      <div class="faq-list reveal d1">__ROWS__
      </div>
    </div>
  </section>
""", id=g[0], eyebrow=g[1], h2=g[2],
        bg=' style="background:var(--surface);"' if i % 2 else "",
        rows=faq_rows([FAQS[j] for j in g[4]])[0])
    for i, g in enumerate(FAQ_GROUPS))

FAQ_BODY = phero(
    "Questions", "Common questions",
    "The things families <em>ask us first.</em>",
    "Cost, timing, whether your child is too young, whether you are too old, and what happens if "
    "life moves you partway through treatment.",
) + fill("""
  <section class="block" style="padding-block:var(--sp-7) 0;">
    <div class="wrap">
      <h2 class="sr-only">Jump to a category</h2>
      __JUMP__
    </div>
  </section>
""", jump=faq_jump) + faq_groups_html + cta_band(
    "Still have a question? <em>Ask it in person.</em>",
    "The free consultation exists for exactly this: a specialist&rsquo;s answer on your own bite, with "
    "no obligation attached.",
    "Free consultation. No referral needed.",
    secondary=("/contact", "Or send us a message"))

C.write("faq.html", C.page(
    title="Orthodontic FAQ Downtown Vancouver | Braces &amp; Invisalign",
    desc="Answers on braces and Invisalign cost in downtown Vancouver, when children should first be seen, treatment length, retainers and referrals.",
    slug="faq", body=FAQ_BODY + leads_script(),
    schema='{\n  "@context": "https://schema.org",\n  "@type": "FAQPage",\n  "isPartOf": { "@id": "https://downtownorthodontics.ca/#practice" },\n  "about": { "@id": "https://downtownorthodontics.ca/#practice" },\n  "mainEntity": [\n%s\n  ]\n}' % faq_schema))

# ==================================================================== CONTACT
CONTACT_BODY = phero(
    "Visit us", "Visit",
    "In the heart of <em>downtown Vancouver.</em>",
    "840 W Hastings St, by Canada Place and a short walk from the office towers. Free "
    "consultations, and no referral needed.",
) + fill("""
  <section class="block">
    <div class="wrap">
      <div class="reqgrid">
        <div class="reveal">
          <span class="eyebrow">(Where and when)</span>
          <h2 class="h2">Downtown Orthodontics.</h2>
          <ul class="checks" style="margin-top:var(--sp-6);">
            <li>__TICK__<span><b>840 W Hastings St</b><br />Vancouver, BC V6C 1C8<br />
              <a class="tlink" href="https://www.google.com/maps/search/?api=1&amp;query=840+W+Hastings+St+Vancouver+BC+V6C+1C8" target="_blank" rel="noopener">Open in Maps &rarr;</a></span></li>
            <li>__TICK__<span><b>Monday</b> 10:00 to 18:00<br /><b>Tuesday</b> 08:00 to 15:00<br />
              <b>Wednesday</b> 08:00 to 16:30<br /><b>Thursday</b> 08:00 to 15:00<br />
              <span style="color:var(--ink-faint);">Friday to Sunday, closed</span></span></li>
            <li>__TICK__<span><b>By Canada Place</b>, across from the Terminal City Club and down
              the street from the Vancouver Club.</span></li>
          </ul>
          <p class="promise" style="margin-top:var(--sp-7);">Call the practice</p>
          <a class="big-tel" href="tel:+16046623290">__PHONE__ (604) 662-3290</a>
        </div>
        <div class="formcard reveal d1">
          <h3>Send us a message</h3>
          <form method="post" action="" novalidate>
            <div class="fgrid">
              <div class="field">
                <label for="c-first">First name</label>
                <input id="c-first" name="first_name" type="text" autocomplete="given-name" required />
              </div>
              <div class="field">
                <label for="c-last">Last name</label>
                <input id="c-last" name="last_name" type="text" autocomplete="family-name" required />
              </div>
              <div class="field">
                <label for="c-phone">Phone</label>
                <input id="c-phone" name="phone" type="tel" autocomplete="tel" required />
              </div>
              <div class="field">
                <label for="c-email">Email</label>
                <input id="c-email" name="email" type="email" autocomplete="email" required />
              </div>
              <div class="field wide">
                <label for="c-msg">How can we help?</label>
                <textarea id="c-msg" name="message" rows="4" style="min-height:96px;min-width:0;width:100%;font-family:var(--font);font-size:16px;color:var(--ink);background:var(--bg);border:var(--border) solid var(--ink-faint);border-radius:var(--radius-btn);padding:var(--sp-3) var(--sp-4);"></textarea>
              </div>
            </div>
__ATTRIBUTION__
            <button class="btn btn-primary" type="submit">Send message <span class="arr">&rarr;</span></button>
          </form>
          <p class="microline">General enquiries only. Please do not send health information here:
            Dr. Daher covers anything clinical with you in person. To book, use the
            <a class="tlink" href="/appointment-request">free consultation request</a>.</p>
          <noscript>
            <p class="microline">This form needs JavaScript to send your message. Please call
              the practice on <a class="tlink" href="tel:+16046623290">(604) 662-3290</a>.</p>
          </noscript>
          <!-- The general-inquiry message box is the ONE permitted textarea (build-site rules). -->
        </div>
      </div>
    </div>
  </section>

  <!-- MAP BAND. Same lazy-loaded embed, address and title as the homepage
       locations section, so there is one map implementation on the site. -->
  <section class="block" style="background:var(--surface);">
    <div class="wrap">
      <div class="sec-head reveal">
        <span class="eyebrow">(On the map)</span>
        <h2 class="h2">840 W Hastings St, <em>by Canada Place.</em></h2>
        <p>Street level on West Hastings, across from the Terminal City Club. Pay parking is in
          the building and the Waterfront SkyTrain and SeaBus terminals are a few minutes&rsquo; walk.</p>
      </div>
      <div class="loc-map reveal d1" style="aspect-ratio:16/7;">
        <iframe
          src="https://maps.google.com/maps?q=Downtown%20Orthodontics%2C%20840%20W%20Hastings%20St%2C%20Vancouver%2C%20BC%20V6C%201C8&amp;z=14&amp;output=embed"
          title="Map showing Downtown Orthodontics at 840 W Hastings St, Vancouver, BC V6C 1C8"
          referrerpolicy="no-referrer-when-downgrade"
          style="position:absolute;inset:0;width:100%;height:100%;border:0" loading="lazy"></iframe>
      </div>
    </div>
  </section>
""", attribution=attribution_inputs("contact")) + cta_band(
    "Ready to <em>book?</em>",
    "The consultation is free, no referral is needed, and you leave with a digital scan, an honest "
    "read on your bite and your exact price in writing.",
    "Monday 10:00 to 18:00 &middot; Tuesday and Thursday 08:00 to 15:00 &middot; Wednesday 08:00 to 16:30.")

# The contact form's endpoints and its fail-safe state come from LEADS_BACKUP_URL and
# GHL_WEBHOOK_URL in build/common.py. wire_form bounds its disable pass to this page's
# one <form>.
CONTACT_BODY = wire_form(CONTACT_BODY, "lead-contact") + leads_script()

# (11) A minimal ContactPage pointing at the shared #practice entity. No address,
# hours or geo facts are restated here, so there is nothing extra to keep in sync.
CONTACT_SCHEMA = """{
  "@context": "https://schema.org",
  "@type": "ContactPage",
  "name": "Contact Downtown Orthodontics",
  "url": "https://downtownorthodontics.ca/contact",
  "isPartOf": { "@id": "https://downtownorthodontics.ca/#practice" },
  "about": { "@id": "https://downtownorthodontics.ca/#practice" }
}"""

C.write("contact.html", C.page(
    title="Contact Downtown Orthodontics | 840 W Hastings St, Vancouver",
    desc="Downtown Orthodontics, 840 W Hastings St, Vancouver, BC. Call (604) 662-3290. Free consultations with specialist orthodontist Dr. Sam Daher.",
    slug="contact", body=CONTACT_BODY, schema=CONTACT_SCHEMA))
