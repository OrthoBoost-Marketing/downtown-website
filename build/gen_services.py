"""The four service pages.

SERVICE-HERO-SPEC + SERVICE-ZIGZAG-SPEC: keyword-in-H1, offer-stacking sub, dual CTA
(form anchor + phone), real photo of the service. Then a 3-row zigzag in the fixed
order empathy -> differentiator BULLETS -> experience, one contextual text link per
row, no buttons on rows. Then the doctor block, then the on-page request form.

One service per page. Rows never drift to sibling services.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chrome as C
from common import attribution_inputs, wire_form, leads_script, quote_card

TICK = ('<svg width="17" height="17" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
        '<path d="M5 13l4 4L19 7" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>')
PHONE = ('<svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
         '<path d="M6.6 10.8a15.1 15.1 0 006.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 013 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.2.2 2.4.6 3.6.1.4 0 .7-.2 1l-2.3 2.2z" fill="currentColor"/></svg>')


def form(slug, preselect, quote_note):
    """REQUEST-FORM-SPEC: 4 fields + the interest select PRE-FILLED with this page's
    service. Testimonial beside the form ships as a visible placeholder (none on file)."""
    opts = []
    for label in ["Braces, metal or clear", "Invisalign or Quick 6 Fix",
                  "Kids' first visit and early care", "Retainers and aftercare",
                  "Not sure yet, help me choose"]:
        sel = ' selected' if label == preselect else ''
        opts.append('                  <option%s>%s</option>' % (sel, label.replace("'", "&rsquo;")))
    tpl = """
  <!-- REQUEST FORM -->
  <section class="block" id="request">
    <div class="wrap">
      <div class="reqgrid">
        <div class="reqcopy reveal">
          <span class="eyebrow">(Talk to us)</span>
          <h2 class="h2">Prefer us to <em>call you?</em></h2>
          <p class="promise">Leave four details and Dr. Daher&rsquo;s front desk will call you the
            same business day to book your free consultation. No health questions here: we cover
            all of that on the call.</p>
          <p class="promise" style="margin-top:var(--sp-6);">Rather just call?</p>
          <a class="big-tel" href="tel:+16046623290">%(phone)s (604) 662-3290</a>
          <p class="promise">Monday 10&ndash;6, Tuesday and Thursday 8&ndash;3, Wednesday 8&ndash;4:30.</p>
          %(quote_note)s
        </div>
        <div class="formcard reveal d1">
          <h3>Request a call back</h3>
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
%(opts)s
                </select>
              </div>
            </div>
%(attribution)s
            <button class="btn btn-primary" type="submit">Request a call back <span class="arr">&rarr;</span></button>
          </form>
          <p class="microline">Your consultation is free. We ask for a name, a phone number and
            an email, never health details.</p>
          <noscript>
            <p class="microline">This form needs JavaScript to send your request. Please call
              the practice on <a class="tlink" href="tel:+16046623290">(604) 662-3290</a>.</p>
          </noscript>
        </div>
      </div>
    </div>
  </section>
"""
    # The form's endpoint and its fail-safe state both come from GHL_WEBHOOK_URL in
    # build/common.py. Same treatment on all four service pages.
    section = tpl % {"opts": "\n".join(opts), "phone": PHONE, "quote_note": quote_note,
                     "attribution": attribution_inputs(
                         slug, offer="$1,000 off full treatment")}
    return wire_form(section, "lead-%s" % slug) + leads_script()


DOCTOR_BAND = """
  <!-- MEET THE DOCTOR (same band as the homepage, one CTA) -->
  <section class="block doc">
    <div class="wrap doc-grid">
      <div class="doc-photo reveal">
        <div class="frame"><img src="assets/photos/w880/dt-6.jpg" alt="Dr. Daher, orthodontist at Downtown Orthodontics" /></div>
      </div>
      <div class="reveal d1">
        <h2 class="h2">One specialist, <em>start to finish.</em></h2>
        <p class="bio">Dr. Daher has planned orthodontic treatment for over 30 years and leads a
          specialist orthodontic practice in downtown Vancouver. He opened the world&rsquo;s
          first Invisalign-only practice in 2009, has taught in 142 cities across six continents,
          and still sits on Align Technology&rsquo;s scientific advisory board.</p>
        <div class="doc-creds">
          <span>%(tick)s Certified specialist in orthodontics</span>
          <span>%(tick)s 30+ years in practice</span>
          <span>%(tick)s Invisalign Lifetime Achievement Award</span>
          <span>%(tick)s Align scientific advisory board</span>
        </div>
        <div class="hero-actions">
          <a class="btn btn-ghost-light" href="/dr-sam-daher">Meet Dr. Daher <span class="arr">&rarr;</span></a>
        </div>
      </div>
    </div>
  </section>
""" % {"tick": TICK}


def hero(eyebrow, h1, sub, chips, photo, alt):
    chip_html = "".join("<span>%s %s</span>" % (TICK, c) for c in chips)
    return """
  <!-- SERVICE HERO: keyword in the H1, offer stacked in the sub, dual CTA -->
  <section class="hero lux" id="top">
    <div class="wrap">
      <div class="hero-copy">
        <p class="crumb"><a href="/">Home</a><span>&middot;</span>%(eyebrow_plain)s</p>
        <div class="hero-mask m-eyebrow"><span class="hero-eyebrow">%(eyebrow)s</span></div>
        <h1 class="hero-title"><span class="hero-mask m-title"><span>%(h1)s</span></span></h1>
        <div class="hero-mask m-sub"><p class="hero-sub">%(sub)s</p></div>
        <div class="hero-actions">
          <a class="btn btn-primary" href="#request">Request a call back <span class="arr">&rarr;</span></a>
          <a class="btn btn-outline" href="tel:+16046623290">%(phone)s (604) 662-3290</a>
        </div>
        <div class="hero-cred">%(chips)s</div>
      </div>
      <div class="hero-figure">
        <div class="hero-frame">
          <img class="hshot" src="%(photo_disp)s" alt="%(alt)s" />
        </div>
      </div>
    </div>
  </section>
""" % {"eyebrow": eyebrow, "eyebrow_plain": eyebrow.split("&middot;")[0].strip(),
       "h1": h1, "sub": sub, "chips": chip_html, "photo_disp": C.disp(photo),
       "alt": alt, "phone": PHONE}


def zigzag(rows):
    """3 rows, fixed order: empathy -> bullets -> experience. Alternating bands.
    One contextual text link per row, never a button."""
    out = []
    for i, r in enumerate(rows):
        bg = ' style="background:var(--surface);"' if i % 2 else ''
        if r.get("bullets"):
            content = '<ul class="checks">%s</ul>' % "".join(
                "<li>%s<span>%s</span></li>" % (TICK, b) for b in r["bullets"])
        else:
            content = "".join("<p style=\"color:var(--ink-soft);font-size:var(--fs-lg);margin-top:var(--sp-4);\">%s</p>" % p
                              for p in r["paras"])
        if r.get("photo"):
            # mirror -> the photo column moves to the left column on desktop via
            # .reqgrid .flip { order: -1 }, while the DOM stays text-first for mobile.
            figure = ('      <div class="photo-side%s reveal d1"><div class="hero-frame">'
                      '<img src="%s" alt="%s" /></div></div>'
                      % (" flip" if r.get("mirror") else "", C.disp(r["photo"]), r["alt"]))
            grid = '<div class="reqgrid">'
        else:
            figure = ""
            grid = '<div style="max-width:760px;">'
        out.append("""
  <section class="block"%(bg)s>
    <div class="wrap">
      %(grid)s
        <div class="reveal">
          <span class="eyebrow">%(eyebrow)s</span>
          <h2 class="h2">%(h2)s</h2>
          %(content)s
          <p style="margin-top:var(--sp-6);"><a class="tlink" href="%(link)s">%(link_text)s <span class="arr">&rarr;</span></a></p>
        </div>
%(figure)s
      </div>
    </div>
  </section>""" % {"bg": bg, "grid": grid, "eyebrow": r["eyebrow"], "h2": r["h2"],
                   "content": content, "link": r["link"], "link_text": r["link_text"],
                   "figure": figure})
    return "\n".join(out)


def faq_block(items):
    rows = "".join("""
        <details class="f">
          <summary>%s<span class="pm"><svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M12 5v14M5 12h14" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg></span></summary>
          <div class="ans"><p>%s</p></div>
        </details>""" % (q, a) for q, a in items)
    schema_items = ",\n".join("""    {
      "@type": "Question",
      "name": %s,
      "acceptedAnswer": { "@type": "Answer", "text": %s }
    }""" % (jstr(q), jstr(a)) for q, a in items)
    return ("""
  <section class="block faq">
    <div class="wrap">
      <div class="sec-head center reveal">
        <span class="eyebrow">(Common questions)</span>
        <h2 class="h2">What people <em>ask us about this.</em></h2>
      </div>
      <div class="faq-list reveal d1">%s
      </div>
    </div>
  </section>
""" % rows, schema_items)


def jstr(s):
    import json
    import html as H
    return json.dumps(H.unescape(s.replace("&rsquo;", "’").replace("&ndash;", "–")))


def build(slug, title, desc, h, rows, faqs, form_preselect, quote_note, service_name, photo):
    faq_html, faq_schema = faq_block(faqs)
    schema = """{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Service",
      "name": %s,
      "serviceType": %s,
      "url": "https://downtownorthodontics.ca/%s",
      "provider": { "@id": "https://downtownorthodontics.ca/#practice" },
      "areaServed": ["Downtown Vancouver", "Burnaby", "South Vancouver", "Richmond", "Surrey", "North Vancouver"]
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
%s
      ]
    }
  ]
}""" % (jstr(service_name), jstr(service_name), slug, faq_schema)
    body = h + zigzag(rows) + DOCTOR_BAND + form(slug, form_preselect, quote_note) + faq_html
    C.write(slug + ".html", C.page(title=title, desc=desc, slug=slug, body=body,
                                   schema=schema, preload=C.disp(photo),
                                   og_image="/" + photo))


# ============================================================ BRACES
build(
    slug="braces",
    title="Braces in Downtown Vancouver | Metal &amp; Clear Braces",
    desc="Metal and clear braces in downtown Vancouver, planned by specialist orthodontist Dr. Sam Daher. $1,000 down, from $220/mo at 0% in-house.",
    h=hero(
        eyebrow="Braces &middot; Downtown Vancouver",
        h1="Braces in downtown Vancouver.",
        sub="Metal and clear braces planned and adjusted by a certified specialist, not fitted in "
            "between fillings. $1,000 down, from $220 a month at 0% in-house interest.",
        chips=["Clear and metal options", "Adjusted by Dr. Daher himself", "Free consultation"],
        photo="assets/photos/used-2.jpg",
        alt="A Downtown Orthodontics clinician scanning a patient chairside before braces treatment"),
    rows=[
        {"eyebrow": "(Why you're here)",
         "h2": "Braces are still the right answer <em>more often than people expect.</em>",
         "paras": [
             "Most people arrive assuming aligners are the modern choice and braces are what they "
             "had to put up with as a teenager. For a lot of bites that is backwards. Braces move "
             "teeth the orthodontist controls directly, which makes them faster and more predictable "
             "on rotations, deep bites and anything that needs real mechanics.",
             "So the honest answer depends on your bite, not on fashion. Dr. Daher plans and "
             "adjusts both braces and Invisalign himself, so the option you are offered is "
             "the one that suits your bite."],
         "link": "/#how", "link_text": "See how a first visit works",
         "photo": "assets/photos/office-inside.jpg",
         "alt": "The open treatment area at Downtown Orthodontics, with chairs and chairside screens",
         "mirror": True},
        {"eyebrow": "(What you get)",
         "h2": "What is actually included.",
         "bullets": [
             "<b>Clear or metal.</b> Ceramic brackets if you would rather they were discreet, "
             "traditional metal if you would rather they were quick and sturdy.",
             "<b>Planned by a specialist, not a salesperson.</b> Dr. Daher adjusts them himself, "
             "so the option you are offered is the one that suits your bite.",
             "<b>Digital scans, no impression trays.</b> Your records are captured in a few minutes.",
             "<b>Dr. Daher at every adjustment.</b> A certified specialist, not a rotating cast.",
             "<b>Refinement covered.</b> If the finish needs extra work to be right, we see it through.",
             "<b>Clear retainers to hold it.</b> Every plan finishes with a retention plan."],
         "link": "/financing", "link_text": "See the full pricing and financing",
         "photo": "assets/photos/used-3.jpg",
         "alt": "Dr. Daher explaining a braces treatment plan at his consultation desk"},
        {"eyebrow": "(What to expect)",
         "h2": "Appointments that <em>fit around a working day.</em>",
         "paras": [
             "The practice is by Canada Place, so adjustments fit into a lunch break "
             "or a school run rather than costing you an afternoon. You see the same small team "
             "each time, so nobody has to re-read your history back to you.",
             "And you will know what is happening. Dr. Daher explains what he is doing and why, in "
             "plain language, at every visit."],
         "link": "#request", "link_text": "Request a call back",
         "photo": None},
    ],
    faqs=[
        ("Who decides whether braces or Invisalign is right for me?",
         "Dr. Daher does, at your free consultation, and he plans and adjusts both himself. That matters more than it sounds: a general dental office selling aligners on the side can only recommend the one thing it offers. You leave with the option that suits your bite, and your exact figure for it in writing."),
        ("How much do braces cost in Vancouver?",
         "Every bite is different, so you get your exact price in writing at your free consultation rather than a range that may not apply to you. Most plans here start at $1,000 down and from $220 a month at 0% in-house interest, with your insurance billed directly."),
        ("Clear braces or metal braces?",
         "Ceramic clear brackets are far less visible and suit adults who would rather not advertise the treatment. Metal is stronger and often a little faster, which matters on complex mechanics. Dr. Daher will tell you honestly whether your case has a real preference or whether it is genuinely your choice."),
        ("Will braces hurt?",
         "There is usually some tenderness for a few days after placement and after an adjustment, the kind that responds to soft food and ordinary painkillers. It is not the constant discomfort people remember from decades ago. Tell us if anything is rubbing and we will fix it rather than asking you to put up with it."),
        ("Can adults get braces?",
         "Yes, and a good share of our patients are downtown professionals. Bone responds to the same forces at forty as at fourteen; treatment can simply take a little longer. If visibility is the concern, clear brackets or Invisalign are both worth discussing at your consultation."),
        ("What happens when the braces come off?",
         "Every plan finishes with clear retainers and a retention plan, because teeth drift if you let them. Dr. Daher checks your retention himself. If an old retainer has stopped fitting, we can help with that too."),
    ],
    form_preselect="Braces, metal or clear",
    # JJ, "Braces off": a finished braces case AND the retention handoff, the pair this
    # page has to prove. Not on the homepage marquee.
    quote_note=quote_card(22, "Braces off, and retained"),
    service_name="Braces for kids, teens and adults",
    photo="assets/photos/used-2.jpg",
)

# ============================================================ INVISALIGN
build(
    slug="invisalign",
    title="Invisalign in Downtown Vancouver | Quick 6 Fix $4,299",
    desc="Invisalign planned by a specialist in downtown Vancouver, not a general dentist. Invisalign Express (Quick 6 Fix) at $4,299 flat, free consultation.",
    h=hero(
        eyebrow="Invisalign &middot; Downtown Vancouver",
        h1="Invisalign in downtown Vancouver.",
        sub="Planned by the orthodontist who opened the world&rsquo;s first Invisalign-only practice "
            "and still sits on Align Technology&rsquo;s scientific advisory board. Simple crowding "
            "and relapse cases fit the Quick 6 Fix at $4,299 flat.",
        chips=["Top 1% of providers globally", "Quick 6 Fix &middot; $4,299 flat", "Free consultation"],
        photo="assets/photos/used-3.jpg",
        alt="Dr. Daher going through an Invisalign plan at his consultation desk"),
    rows=[
        {"eyebrow": "(Why you're here)",
         "h2": "Invisalign is a tool. The result comes from <em>the doctor holding it.</em>",
         "paras": [
             "Plenty of dental offices now sell aligners between fillings and cleanings. The trays "
             "come from the same company either way. What differs is who decides how the teeth "
             "should move, how far, in what order, and what to do when a tooth does not track.",
             "That is the whole job of an orthodontic specialist, and it is the difference between "
             "a finished bite and one that looks straighter from the front. Dr. Daher has been "
             "doing it since Invisalign existed, and taught other clinicians how in 142 cities."],
         "link": "/dr-sam-daher", "link_text": "Read Dr. Daher's record",
         "photo": "assets/photos/practice.jpg",
         "alt": "Dr. Daher at the Downtown Orthodontics practice in downtown Vancouver",
         "mirror": True},
        {"eyebrow": "(What you get)",
         "h2": "What is actually included.",
         "bullets": [
             "<b>A specialist plan.</b> Every stage designed and supervised by a certified "
             "orthodontist, not sent away to a lab technician.",
             "<b>Quick 6 Fix at $4,299 flat.</b> For mild crowding, small gaps and teeth that "
             "shifted after earlier treatment, with candidacy confirmed free.",
             "<b>Planned by a specialist.</b> So the recommendation is about your bite.",
             "<b>Digital scans, no impression trays.</b> A few minutes, and you see the plan on screen.",
             "<b>Refinement covered.</b> Extra aligners to finish it properly are part of the plan.",
             "<b>Clear retainers at the end.</b> With a retention plan Dr. Daher checks himself."],
         "link": "/financing", "link_text": "See the full pricing and financing",
         "photo": "assets/photos/dt-7.jpg",
         "alt": "Dr. Daher holding an Invisalign aligner at Downtown Orthodontics"},
        {"eyebrow": "(What to expect)",
         "h2": "Discreet enough that <em>most people never notice.</em>",
         "paras": [
             "Aligners come out to eat and to brush, and go back in for the other twenty-two hours. "
             "Most of our adult patients tell colleagues nothing and nobody asks. Appointments are "
             "short and the practice sits by Canada Place, so they fit before work or over lunch.",
             "The part people underestimate is wear time. Dr. Daher will be straight with you about "
             "it at the consultation, because aligners only work as well as they are worn."],
         "link": "#request", "link_text": "Request a call back",
         "photo": None},
    ],
    faqs=[
        ("How much does Invisalign cost in Vancouver?",
         "Simple cases that suit Invisalign Express, what we call the Quick 6 Fix, are $4,299 flat. Full treatment starts at $1,000 down and from $220 a month at 0% in-house interest. Your exact figure comes from your free consultation, in writing, before you commit."),
        ("What is the Quick 6 Fix?",
         "It is Invisalign Express for mild crowding, small gaps, and teeth that have shifted after earlier treatment. It is a shorter course of aligners at a $4,299 flat rate. Not every case qualifies, and we confirm your candidacy free rather than selling you into it."),
        ("Why see an orthodontist instead of my dentist for Invisalign?",
         "Because the aligners are the same and the planning is not. Deciding how teeth should move, in what order, and what to do when one does not track is the specialty. Dr. Daher opened the world's first Invisalign-only practice in 2009 and sits on Align Technology's scientific advisory board."),
        ("Invisalign or braces: how do we choose?",
         "At your consultation we will walk through both honestly for your specific bite. Some cases do beautifully with Invisalign; others are better and faster with braces. Dr. Daher plans and adjusts both himself, so the recommendation is about your teeth rather than our margin."),
        ("How long does Invisalign take?",
         "Treatment length depends on what your bite needs, so you will get a realistic timeline for your own case at your consultation rather than a range that may not apply to you. Express cases finish considerably sooner. With aligners, wear time is the biggest single factor."),
        ("Can teenagers use Invisalign?",
         "Yes. Invisalign Teen is built for it, with wear indicators and replacement allowances for the aligners that inevitably get lost. Whether it suits your teenager depends on the bite and honestly on how reliably they will wear them, which we will talk through together."),
    ],
    form_preselect="Invisalign or Quick 6 Fix",
    # Chloe McCarron, "Invisalign": no waiting to start, and confidence in the
    # specialist. Not on the homepage marquee.
    quote_note=quote_card(18, "Invisalign"),
    service_name="Invisalign and Invisalign Teen",
    photo="assets/photos/used-3.jpg",
)

# ============================================================ EARLY ORTHODONTICS
build(
    slug="early-orthodontics",
    title="Kids&rsquo; Orthodontist Downtown Vancouver | Early Treatment",
    desc="Free first orthodontic check from age seven in downtown Vancouver. Expanders, early treatment and Invisalign First with specialist Dr. Sam Daher.",
    h=hero(
        eyebrow="Kids &amp; early care &middot; Downtown Vancouver",
        h1="Kids&rsquo; orthodontics in downtown Vancouver.",
        sub="A first check around age seven, watched by a specialist rather than guessed at. Most "
            "children need nothing done yet, and that first visit is always free.",
        chips=["Free growth assessment", "First check from age seven", "Treatment only when it helps"],
        photo="assets/photos/used-1.jpg",
        alt="A member of the Downtown Orthodontics team holding a clear retainer"),
    rows=[
        {"eyebrow": "(Why you're here)",
         "h2": "Most seven-year-olds <em>do not need braces.</em>",
         "paras": [
             "That is the most useful thing an orthodontist can tell a parent, and it is the reason "
             "the first visit exists. An early check is not the start of treatment. It is a "
             "specialist looking at how the jaw is growing, whether the adult teeth have room, and "
             "whether anything is worth watching.",
             "Usually the answer is come back in a year. Occasionally it is that a small "
             "intervention now avoids a much larger one later. Either way you leave knowing, "
             "instead of wondering."],
         "link": "/#how", "link_text": "See how a first visit works",
         "photo": "assets/photos/used-3.jpg",
         "alt": "Dr. Daher pointing out a growth pattern on a digital scan at his consultation desk",
         "mirror": True},
        {"eyebrow": "(What you get)",
         "h2": "What the first visit covers.",
         "bullets": [
             "<b>Free, always.</b> The first growth check costs nothing and carries no obligation.",
             "<b>Jaw growth and spacing assessed</b> by a certified specialist, with digital images "
             "you can see rather than a verdict you have to take on trust.",
             "<b>Expanders and early appliances</b> when the timing genuinely helps, sized to a "
             "growing jaw rather than fitted early for the sake of it.",
             "<b>Invisalign First</b> where aligners suit a child's case better than brackets.",
             "<b>Monitoring, at no cost</b> if the answer is wait. We will tell you when to come back.",
             "<b>No treatment we cannot justify.</b> Thirty years in, the rule has not changed."],
         "link": "/financing", "link_text": "See the full pricing and financing",
         "photo": "assets/photos/used-2.jpg",
         "alt": "A Downtown Orthodontics clinician working chairside with a patient"},
        {"eyebrow": "(What to expect)",
         "h2": "A first appointment <em>nobody has to be brave for.</em>",
         "paras": [
             "The scan is a camera, not a mouthful of putty, and it takes a few minutes. Nothing "
             "sharp, nothing that needs explaining away. Children generally find it more "
             "interesting than alarming, because they can watch their own teeth appear on screen.",
             "Parents sit in on everything. You will hear the same explanation your child does, and "
             "you will leave with it written down."],
         "link": "#request", "link_text": "Request a call back",
         "photo": None},
    ],
    faqs=[
        ("When should our child first see an orthodontist?",
         "Around age seven. Most children will not need anything done yet, but an early check lets Dr. Daher see how the jaw is growing and catch anything worth watching while it is still easy to influence. That first visit is always free."),
        ("How much does children's orthodontic treatment cost in Vancouver?",
         "The first growth check is free. If treatment is genuinely needed, most plans start at $1,000 down and from $220 a month at 0% in-house interest, with your insurance billed directly. You get the exact figure in writing before anything begins."),
        ("Is it too early for braces at seven?",
         "Usually, yes, and we will say so. The point of an age-seven check is not to start treatment but to know whether anything needs watching. If early treatment would genuinely help, an expander or partial braces timed to the growing jaw can prevent a bigger problem later."),
        ("What is an expander and does my child need one?",
         "It is an appliance that widens the upper jaw while it is still growing, creating room for adult teeth that would otherwise crowd. Whether your child needs one depends on the width of the palate and the space available, which is exactly what the free check measures."),
        ("Will you recommend treatment my child does not need?",
         "No, and the practice has been built around not doing that. Dr. Daher's rule for thirty years has been the least treatment that gets the right result, with no unnecessary extractions. If the honest answer is wait a year, that is the answer you will get."),
        ("Can my teenager have Invisalign instead of braces?",
         "Often, yes. Invisalign Teen is designed for it. Whether it suits depends on the bite and on how reliably the aligners will actually be worn, and we would rather have that conversation honestly up front than six months in."),
    ],
    form_preselect="Kids' first visit and early care",
    # Elizabeth May, "Kids": explains the treatment to the CHILD as well as the adult,
    # which is this page's whole promise. Not on the homepage marquee.
    # "Family of", not "Parent of": she brought her NIECE. The caption must not imply a
    # relationship the review does not state.
    quote_note=quote_card(11, "Family of a young patient"),
    service_name="Early and interceptive orthodontics for children",
    photo="assets/photos/used-1.jpg",
)

# ============================================================ RETAINERS
build(
    slug="retainers",
    title="Retainers in Downtown Vancouver | Retention &amp; Replacements",
    desc="Clear retainers and retention planning in downtown Vancouver, checked by specialist Dr. Sam Daher. Old retainers can be replaced.",
    h=hero(
        eyebrow="Retainers &amp; aftercare &middot; Downtown Vancouver",
        h1="Retainers in downtown Vancouver.",
        sub="Teeth drift if you let them, so every plan here finishes with clear retainers and a "
            "retention plan Dr. Daher checks himself. If an old retainer has stopped fitting, we "
            "can help with that too.",
        chips=["Included in every plan", "Retention checked by a specialist", "Replacements available"],
        photo="assets/photos/img-3127.jpg",
        alt="Dr. Daher with an adult patient at Downtown Orthodontics"),
    rows=[
        {"eyebrow": "(Why you're here)",
         "h2": "The result is not finished <em>when the braces come off.</em>",
         "paras": [
             "Teeth are held in bone by fibres that remember where they used to be, and for the "
             "first year or so after treatment they pull. That is not a failure of the treatment. "
             "It is simply what teeth do, and it is why retention is part of the plan rather than "
             "an upsell at the end.",
             "Most relapse cases we see are not people whose treatment went wrong. They are people "
             "who stopped wearing a retainer in their twenties and came back a decade later."],
         "link": "/#how", "link_text": "See how a first visit works",
         "photo": "assets/photos/used-1.jpg",
         "alt": "A member of the Downtown Orthodontics team holding a clear retainer",
         "mirror": True},
        {"eyebrow": "(What you get)",
         "h2": "What retention actually involves.",
         "bullets": [
             "<b>Clear retainers with every plan.</b> Included, not charged separately at the end.",
             "<b>A retention schedule you can follow.</b> Full-time at first, then nights, with the "
             "steps written down rather than left vague.",
             "<b>Dr. Daher checks the retention himself</b> at your review appointments.",
             "<b>Replacements when life happens.</b> Lost, cracked or outgrown retainers can be "
             "remade from a fresh scan.",
             "<b>Old retainers that no longer fit</b> are worth bringing in. We can often help even "
             "if the original treatment was somewhere else.",
             "<b>Relapse cases welcome.</b> Teeth that shifted after earlier treatment often suit "
             "the Quick 6 Fix at $4,299 flat."],
         "link": "/invisalign", "link_text": "Read about the Quick 6 Fix",
         "photo": "assets/photos/used-3.jpg",
         "alt": "Dr. Daher reviewing a retention plan at his consultation desk"},
        {"eyebrow": "(What to expect)",
         "h2": "Short visits, <em>by Canada Place.</em>",
         "paras": [
             "Retainer checks are quick, and the practice sits close enough to the office towers "
             "that they fit into a lunch break. Bring the retainer you have, even if it has not "
             "been worn in years and you are slightly embarrassed about it. We have seen worse.",
             "If a scan shows things have moved, you will get honest options rather than a lecture."],
         "link": "#request", "link_text": "Request a call back",
         "photo": None},
    ],
    faqs=[
        ("How long do I need to wear a retainer?",
         "Full-time at first, then nights, and then indefinitely a few nights a week if you want the result to hold. That last part surprises people. Teeth keep their memory for life, so retention is less a phase than a habit, and it is a small one."),
        ("What if I lost my retainer?",
         "Call us. We can take a fresh scan and remake it, and the sooner you do that the less likely anything has moved. Going without one for a few weeks is usually recoverable; going without for a few years often is not."),
        ("My teeth shifted after braces years ago. Can that be fixed?",
         "Usually, yes, and often quickly. Mild relapse is exactly what Invisalign Express, our Quick 6 Fix, is for, at a $4,299 flat rate. We confirm your candidacy free before you commit to anything."),
        ("Can you replace a retainer if I had treatment elsewhere?",
         "Often. Bring in what you have and we will take a look. If your teeth are still where the old retainer expects them to be, remaking it is straightforward. If not, we will show you the scan and talk through the options."),
        ("Are retainers included in the treatment price?",
         "Yes. Every plan here finishes with clear retainers and a retention plan as part of the treatment, not as a separate charge at the end. Replacements later on are priced separately, and we will tell you what they cost before we make one."),
        ("How much does a replacement retainer cost?",
         "It depends on the type and whether we need a new scan, so we quote it before making anything rather than publishing a figure that may not match your case. Call the practice and we will tell you what your situation involves."),
    ],
    form_preselect="Retainers and aftercare",
    # Roger Singh, "Retention": thirteen years on and still a patient, the retention
    # claim proved by duration. Not on the homepage marquee.
    quote_note=quote_card(15, "Retention, thirteen years"),
    service_name="Clear retainers and retention",
    photo="assets/photos/img-3127.jpg",
)
