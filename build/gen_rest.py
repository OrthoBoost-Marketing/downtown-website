"""Doctor bio, why-choose-us, financing, FAQ, contact, and the utility pages."""
import sys, os, json, html as H
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chrome as C

from common import TICK, PHONE, phero, cta_band, faq_rows, jstr as j, fill
from common import leads_script

# ==================================================================== DOCTOR BIO
# DOCTOR-PAGE-SPEC wants story before credentials: origin spark, the personal wound
# that explains the practice style, training as journey, a philosophy metaphor, why
# this practice, life outside. NONE of that narrative is on file. The credentials are
# client-confirmed; the story is not. So the story beats ship as visible placeholders
# rather than invented biography. Flagged in BUILD-NOTES.md.
CREDS = [
    ("An early adopter of Invisalign", "Dr. Daher worked with Align Technology&rsquo;s founder on the company&rsquo;s scientific advisory board."),
    ("Still on Align&rsquo;s scientific advisory board", "One of a select few orthodontists serving on it today."),
    ("Invisalign Lifetime Achievement Award", "Awarded in 2014."),
    ("Lectured in 46 countries", "142 cities, across six continents."),
    ("Founder of the Daher Aligner Institute", "Founded and led by Dr. Daher."),
    ("Founder of Stream Dental HR", "A venture he founded alongside the practice."),
    ("Former associate professor", "University of Montreal and University of the Pacific."),
    ("McGill&rsquo;s Dr. James McCutcheon award", "Recognised by his alma mater."),
    ("The world&rsquo;s first Invisalign-only practice", "Opened in 2009."),
    ("Top 1% of Invisalign providers globally", "And the top provider worldwide from 2009 to 2011."),
]
cred_rows = "\n".join(
    '        <div class="ci reveal%s">%s<div><b>%s</b><span>%s</span></div></div>'
    % ((" d1" if i % 2 else ""), TICK, t, d) for i, (t, d) in enumerate(CREDS))

DOC_BODY = phero(
    "Meet Dr. Daher", "Meet the doctor",
    "Dr. Sam Daher, <em>orthodontist.</em>",
    "Thirty years of moving teeth, a seat on Align Technology&rsquo;s scientific advisory board, "
    "and a rule that has never changed: the least treatment that gets the right result.",
) + """
  <!-- STAT BAR. DOCTOR-PAGE-SPEC wants four chips under the hero for the
       credential-scanners, ahead of the story. Every figure here is already
       stated further down this page and in the Physician schema. -->
  <section class="block" style="padding-block:var(--sp-7);background:var(--surface);border-block:var(--border) solid var(--line);">
    <div class="wrap">
      <h2 class="sr-only">Dr. Daher in four numbers</h2>
      <ul class="statbar reveal">
        <li><span class="sb-k">30+ years</span><span class="sb-v">planning orthodontic treatment</span></li>
        <li><span class="sb-k">Certified</span><span class="sb-v">specialist in orthodontics</span></li>
        <li><span class="sb-k">Align board</span><span class="sb-v">scientific advisory board member</span></li>
        <li><span class="sb-k">46 countries</span><span class="sb-v">142 cities where he has taught</span></li>
      </ul>
    </div>
  </section>

  <!-- WHO HE IS, in the practice's own documented terms -->
  <section class="block">
    <div class="wrap doc-grid" style="align-items:start;">
      <div class="doc-photo reveal">
        <div class="frame"><img src="assets/photos/w880/dt-6.jpg" alt="Dr. Sam Daher, orthodontist at Downtown Orthodontics" /></div>
      </div>
      <div class="reveal d1">
        <span class="eyebrow">(In practice)</span>
        <h2 class="h2">Orthodontics is <em>the only thing he does.</em></h2>
        <p style="color:var(--ink-soft);font-size:var(--fs-xl);margin-top:var(--sp-5);">
          Dr. Daher is a certified specialist in orthodontics and has planned treatment for over
          thirty years. Downtown Orthodontics is a specialist orthodontic practice in
          downtown Vancouver, which means moving teeth is the whole job here.</p>
        <p style="color:var(--ink-soft);font-size:var(--fs-md);margin-top:var(--sp-4);">
          His patients range from seven-year-olds at a first growth check to adults referred for
          complex cases. The approach has not changed in three decades: careful diagnosis,
          honest recommendations, no unnecessary extractions, and no surgery a patient does not
          need. If a result needs extra refinement to be right, he sees it through.</p>
        <p style="color:var(--ink-soft);font-size:var(--fs-md);margin-top:var(--sp-4);">
          He has also spent much of his career teaching it. Dr. Daher opened the world&rsquo;s first
          Invisalign-only practice in 2009, has lectured in 46 countries and 142 cities across six
          continents, founded the Daher Aligner Institute, and served as an associate professor at
          the University of Montreal and the University of the Pacific.</p>
        <div class="hero-actions" style="margin-top:var(--sp-7);">
          <a class="btn btn-primary" href="/appointment-request">Book with Dr. Daher <span class="arr">&rarr;</span></a>
        </div>
      </div>
    </div>
  </section>

  <!-- NO "in his own words" section. The kit's doctor-page spec asks for story before
       credentials: why he chose orthodontics, what shaped the conservative approach, and a
       short "away from the office" note. None of that is on file and this build does not
       invent biography, so the section shipped as a visible placeholder until 2026-08-27,
       when Jules cut it rather than launch with an empty promise on the page. The
       credentials, the record and the treatment philosophy carry the page on their own.
       Roughly 200 words from Dr. Daher plus 60 on life outside restores it. -->

  <!-- CREDENTIALS, identical treatment to the homepage section -->
  <section class="block credo" id="credentials">
    <div class="wrap">
      <div class="sec-head reveal">
        <span class="eyebrow">(Credentials &amp; recognition)</span>
        <h2 class="h2">The record, <em>in full.</em></h2>
        <p>Every item here was supplied by the practice.</p>
      </div>
      <div class="credo-lead">
        <div class="reveal"><span class="cl-k">2014</span><p class="cl-v">Invisalign Lifetime Achievement Award.</p></div>
        <div class="reveal d1"><span class="cl-k">46 countries</span><p class="cl-v">142 cities, six continents, teaching other clinicians.</p></div>
        <div class="reveal d2"><span class="cl-k">2009</span><p class="cl-v">Opened the world&rsquo;s first Invisalign-only practice.</p></div>
      </div>
      <div class="credo-list">
%s
      </div>
    </div>
  </section>
""" % cred_rows + cta_band(
    "See what a specialist <em>actually finds.</em>",
    "A free consultation with Dr. Daher gets you a digital scan, an honest read on your bite, "
    "and your exact price in writing. What you do next is up to you.",
    "Free consultation. No referral needed. $1,000 down, from $220/mo at 0% in-house financing.")

DOC_SCHEMA = """{
  "@context": "https://schema.org",
  "@type": "AboutPage",
  "url": "https://downtownorthodontics.ca/dr-sam-daher",
  "mainEntity": {
    "@type": "Physician",
    "name": "Dr. Sam Daher",
    "jobTitle": "Certified Specialist in Orthodontics",
    "worksFor": { "@id": "https://downtownorthodontics.ca/#practice" },
    "award": [
      "Invisalign Lifetime Achievement Award (2014)",
      "Dr. James McCutcheon award, McGill University"
    ],
    "memberOf": { "@type": "Organization", "name": "Align Technology Scientific Advisory Board" },
    "alumniOf": { "@type": "CollegeOrUniversity", "name": "McGill University" },
    "affiliation": [
      { "@type": "CollegeOrUniversity", "name": "University of Montreal" },
      { "@type": "CollegeOrUniversity", "name": "University of the Pacific" }
    ]
  }
}"""

C.write("dr-sam-daher.html", C.page(
    title="Dr. Sam Daher, Orthodontist | Downtown Vancouver",
    desc="Downtown Vancouver orthodontist Dr. Sam Daher, a certified specialist with 30+ years. Align Technology advisory board, 2014 Invisalign Lifetime Award.",
    slug="dr-sam-daher", body=DOC_BODY + leads_script(), schema=DOC_SCHEMA,
    preload="assets/photos/w880/dt-6.jpg", og_image="/assets/photos/dt-6.jpg"))

# ==================================================================== WHY CHOOSE US
# WHY-PAGE-SPEC: no form. Six USPs as a grid, then deep-dives on the top three.
# CTA cadence hero -> one mid-page -> closing band.
USPS = [
    ("A certified specialist downtown",
     "Orthodontics is a separate specialty after dental school, and Downtown Orthodontics is a "
     "specialist orthodontic practice in the downtown core. Everything here is planned by one."),
    ("On Align Technology&rsquo;s scientific advisory board",
     "Dr. Daher was among the first to use Invisalign and still sits on Align Technology&rsquo;s "
     "scientific advisory board, one of a select few worldwide. Align gave him its Lifetime "
     "Achievement Award in 2014."),
    ("Conservative by conviction",
     "Thirty years in, the rule has not changed: no unnecessary extractions, no surgery a patient "
     "does not need, and the least treatment that gets the right result."),
    ("Referrals and retreatment, routinely",
     "Referred cases and retreatment are a normal part of the week here, which is what a specialist "
     "practice is for. Thirty years of it, in one pair of hands."),
    ("From $220/mo at 0% in-house",
     "$1,000 down, financing arranged in-house at no interest, insurance billed directly, and your "
     "full cost in writing before you commit."),
    ("By Canada Place",
     "Close enough to the office towers that adjustments fit into a lunch break, and close enough "
     "to transit that a school run works."),
]
usp_cards = "\n".join("""        <div class="reveal%s rounded-brand border border-line bg-white p-7 shadow-soft">
          <h3 style="font-size:var(--fs-xl);font-weight:var(--fw-semibold);color:var(--ink);margin:0 0 var(--sp-3);letter-spacing:-.01em;">%s</h3>
          <p style="margin:0;color:var(--ink-soft);font-size:var(--fs-md);">%s</p>
        </div>""" % ((" d%d" % (i % 3) if i % 3 else ""), t, b) for i, (t, b) in enumerate(USPS))

WHY_BODY = phero(
    "Why choose us", "Why a specialist",
    "Why a specialist, <em>for every bite.</em>",
    "Orthodontics is a separate specialty after dental school. Here it is the only thing done, "
    "by a certified specialist with thirty years in it.",
) + ("""
  <section class="block">
    <div class="wrap">
      <div class="sec-head reveal">
        <span class="eyebrow">(Six reasons)</span>
        <h2 class="h2">What actually <em>sets this practice apart.</em></h2>
      </div>
      <div class="tw-block grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
%(usps)s
      </div>
    </div>
  </section>

  <section class="block compare-wrap">
    <div class="wrap">
      <div class="sec-head center reveal">
        <span class="eyebrow">(The difference)</span>
        <h2 class="h2">Specialist care, <em>side by side.</em></h2>
        <p>What changes when a certified orthodontic specialist plans the case from the start.</p>
      </div>
      <div class="compare reveal">
        <div class="ch old">Aligners without a specialist</div>
        <div class="ch new">A certified specialist downtown</div>
        <div class="cc old">No orthodontic specialist involved</div>
        <div class="cc new">%(tick)s A certified specialist at every visit</div>
        <div class="cc old">One appliance, whatever the bite</div>
        <div class="cc new">%(tick)s Braces, Invisalign and early care, matched to the bite</div>
        <div class="cc old">Finished when the trays run out</div>
        <div class="cc new">%(tick)s Refinement covered until the finish is right</div>
        <div class="cc old">Costs that land later</div>
        <div class="cc new">%(tick)s Your full cost, in writing, up front</div>
      </div>
      <p class="compare-note reveal">Done right by a certified specialist downtown. It is still
        affordable here.</p>
      <div class="hero-actions reveal" style="justify-content:center;margin-top:var(--sp-8);">
        <a class="btn btn-primary" href="/appointment-request">Book a free consultation <span class="arr">&rarr;</span></a>
      </div>
    </div>
  </section>

  <section class="block" style="background:var(--surface);">
    <div class="wrap">
      <div class="sec-head reveal">
        <span class="eyebrow">(In more detail)</span>
        <h2 class="h2">The three that <em>matter most.</em></h2>
      </div>
      <div class="reqgrid reveal">
        <div>
          <h3 style="font-size:var(--fs-3xl);font-weight:var(--fw-semibold);color:var(--ink);margin:0 0 var(--sp-4);letter-spacing:-.02em;">A specialist plans it</h3>
          <p style="color:var(--ink-soft);font-size:var(--fs-md);">Orthodontics is a separate
            specialty for a reason. Deciding how teeth should move, in what order, how far, and what
            to do when one does not track is the entire discipline. Dr. Daher has been doing it for
            thirty years and has taught it to other clinicians in 142 cities.</p>
          <p style="color:var(--ink-soft);font-size:var(--fs-md);margin-top:var(--sp-4);">The
            aligners themselves come from the same company wherever you go. The planning does not.</p>
        </div>
        <div class="hero-frame"><img src="assets/photos/w880/practice.jpg" alt="Dr. Daher at Downtown Orthodontics" /></div>
      </div>
    </div>
  </section>

  <section class="block">
    <div class="wrap">
      <div class="reqgrid reveal">
        <div class="hero-frame" style="order:-1;"><img src="assets/photos/w880/used-3.jpg" alt="Dr. Daher explaining a treatment plan at his consultation desk" /></div>
        <div>
          <h2 style="font-family:var(--font);font-size:var(--fs-3xl);font-weight:var(--fw-semibold);color:var(--ink);margin:0 0 var(--sp-4);letter-spacing:-.02em;">A specialist plans it either way</h2>
          <p style="color:var(--ink-soft);font-size:var(--fs-md);">Braces and Invisalign are
            different tools, and only one of them may suit your bite. Dr. Daher plans and adjusts
            both himself, so the option you are offered is the one your case calls for, and you get
            your exact figure in writing before you commit.</p>
          <p style="color:var(--ink-soft);font-size:var(--fs-md);margin-top:var(--sp-4);">
            <a class="tlink" href="/financing">See the pricing in full <span class="arr">&rarr;</span></a></p>
        </div>
      </div>
    </div>
  </section>

  <section class="block" style="background:var(--surface);">
    <div class="wrap">
      <div class="reqgrid reveal">
        <div>
          <h2 style="font-family:var(--font);font-size:var(--fs-3xl);font-weight:var(--fw-semibold);color:var(--ink);margin:0 0 var(--sp-4);letter-spacing:-.02em;">The least treatment that works</h2>
          <p style="color:var(--ink-soft);font-size:var(--fs-md);">No unnecessary extractions. No
            surgery a patient does not need. A finished case means a healthy bite, and if getting
            there needs extra refinement, that is included rather than invoiced.</p>
          <p style="color:var(--ink-soft);font-size:var(--fs-md);margin-top:var(--sp-4);">It is also
            why a seven-year-old often leaves with instructions to come back in a year. Watching is
            a legitimate treatment plan, and the check for it is free.</p>
          <p style="color:var(--ink-soft);font-size:var(--fs-md);margin-top:var(--sp-4);">
            <a class="tlink" href="/early-orthodontics">Read about kids&rsquo; early care <span class="arr">&rarr;</span></a></p>
        </div>
        <div class="hero-frame"><img src="assets/photos/w880/office-inside.jpg" alt="The Downtown Orthodontics treatment area" /></div>
      </div>
    </div>
  </section>

  <section class="block">
    <div class="wrap" style="max-width:760px;">
      <div class="reveal">
        <span class="eyebrow">(The team)</span>
        <h2 class="h2">A small team you will <em>actually recognise.</em></h2>
        <p style="color:var(--ink-soft);font-size:var(--fs-lg);margin-top:var(--sp-5);">The practice
          is deliberately small. You see Dr. Daher at every visit and the same handful of people at
          the front desk and chairside, which means nobody has to read your history back to you.</p>
        <!-- No named introductions. Maya and Bita are known to us by first name only, with
             no roles, bios or headshots on file. This shipped as a visible placeholder until
             2026-08-27, when Jules cut it: the heading and the paragraph above already make
             the small-practice point without naming anyone, and there is no separate team
             page for the same reason. Full names plus job titles are enough to restore it,
             and it can run type-only if headshots never arrive. -->
      </div>
    </div>
  </section>
""" % {"usps": usp_cards, "tick": TICK}) + cta_band(
    "One free visit tells you <em>everything.</em>",
    "A digital scan, a specialist&rsquo;s read on your bite, honest options and your exact price in "
    "writing. Then you decide.",
    "Free consultation. No referral needed. Clear and metal braces, and Invisalign.")

# (11) This page carried no JSON-LD. A minimal WebPage that points at the shared
# #practice entity: no new address, hours or geo facts to keep in sync.
WHY_SCHEMA = """{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": "Why a specialist orthodontist",
  "url": "https://downtownorthodontics.ca/why-choose-us",
  "isPartOf": { "@id": "https://downtownorthodontics.ca/#practice" },
  "about": { "@id": "https://downtownorthodontics.ca/#practice" }
}"""

C.write("why-choose-us.html", C.page(
    title="Why a Specialist Orthodontist | Downtown Vancouver",
    desc="Why see a certified specialist orthodontist in downtown Vancouver. Conservative care, 30+ years, complex and referred cases welcome.",
    slug="why-choose-us", body=WHY_BODY + leads_script(), schema=WHY_SCHEMA))
