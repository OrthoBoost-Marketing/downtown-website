"""Legal and utility pages.

UTILITY-PAGES-SPEC. Legal copy ships as clearly-marked SAMPLE text requiring the
practice's own counsel: this build does not supply legal advice, and the brief lists
attorney review as outstanding. These pages stay noindex permanently.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chrome as C
from common import phero, fill

COUNSEL = ('<p class="legal-note"><b>Sample text, not legal advice.</b> This page is a starting '
           'template prepared for Downtown Orthodontics and has <b>not</b> been reviewed by a '
           'lawyer. It must be checked against British Columbia&rsquo;s Personal Information '
           'Protection Act, PIPEDA, and the College of Oral Health Professionals of British '
           'Columbia&rsquo;s requirements before the site goes live. Bracketed items need the '
           'practice&rsquo;s own answers.</p>')

# ==================================================================== PRIVACY
PRIVACY = phero(
    "Privacy policy", "Legal",
    "Privacy policy.",
    "How Downtown Orthodontics collects, uses and protects personal information.",
    actions=False,
) + fill("""
  <section class="block">
    <div class="wrap">
      <div class="prose reveal">
        __COUNSEL__
        <p><b>Last updated:</b> [DATE TO CONFIRM]</p>

        <h2>Who we are</h2>
        <p>Downtown Orthodontics is an orthodontic practice at 840 W Hastings St, Vancouver,
          British Columbia V6C 1C8. You can reach us on
          <a href="tel:+16046623290">(604) 662-3290</a> with any question about this policy or
          about the information we hold on you.</p>

        <h2>What we collect through this website</h2>
        <p>When you complete a form on this site we collect only your first name, last name,
          phone number, email address, and the treatment you told us you were interested in. We
          deliberately do not ask for health information through this website. Anything clinical is
          discussed with you directly, in person or by phone.</p>
        <p>We also collect standard technical information that your browser sends to any website,
          such as your approximate location, the pages you viewed, and the site or advertisement
          that referred you.</p>

        <h2>Why we collect it</h2>
        <ul>
          <li>To contact you about the consultation or question you submitted.</li>
          <li>To arrange, provide and administer orthodontic care if you become a patient.</li>
          <li>To understand which pages and advertisements bring people to the practice.</li>
        </ul>
        <p>We do not sell your personal information, and we do not share it with anyone except the
          service providers described below.</p>

        <h2>Who else handles your information</h2>
        <p>We use third-party services to run the website and manage enquiries, and those providers
          process information on our behalf under contract. [LIST TO CONFIRM: the practice&rsquo;s
          website host, customer relationship system, call-tracking provider, and analytics and
          advertising platforms.] Some of these providers store information outside Canada, which
          means it may be subject to the laws of the country where it is held.</p>

        <h2>Cookies and advertising</h2>
        <p>This site uses cookies and similar technologies to remember how you arrived, so we can
          tell which advertising is working. [TO CONFIRM: the exact analytics and advertising
          tools in use, and whether a consent banner is required for this practice.] You can clear
          or block cookies through your browser settings at any time.</p>

        <h2>How long we keep it</h2>
        <p>Enquiry information is kept for as long as we need it to answer you and to keep proper
          business records. Patient records are kept for the period required by the regulator for
          health records in British Columbia. [RETENTION PERIODS TO CONFIRM.]</p>

        <h2>Your rights</h2>
        <p>You can ask us what personal information we hold about you, ask us to correct it, or ask
          us to delete information we are not required to keep. Call
          <a href="tel:+16046623290">(604) 662-3290</a> or write to us at the address above and we
          will respond within the timeframe the law allows. If you are not satisfied with our
          response you may contact the Office of the Information and Privacy Commissioner for
          British Columbia.</p>

        <h2>Children</h2>
        <p>We treat children, and a parent or guardian provides and controls their information.
          We do not knowingly collect information directly from a child through this website.</p>

        <h2>Changes to this policy</h2>
        <p>If we change this policy we will update the date at the top of this page.</p>
      </div>
    </div>
  </section>
""", counsel=COUNSEL)

C.write("privacy-policy.html", C.page(
    title="Privacy Policy | Downtown Orthodontics",
    desc="How Downtown Orthodontics collects, uses and protects personal information.",
    slug="privacy-policy", body=PRIVACY))

# ==================================================================== TERMS
TERMS = phero(
    "Terms &amp; conditions", "Legal",
    "Terms &amp; conditions.",
    "The terms on which this website is provided.",
    actions=False,
) + fill("""
  <section class="block">
    <div class="wrap">
      <div class="prose reveal">
        __COUNSEL__
        <p><b>Last updated:</b> [DATE TO CONFIRM]</p>

        <h2>About this website</h2>
        <p>This website is operated by Downtown Orthodontics, 840 W Hastings St, Vancouver, British
          Columbia V6C 1C8. By using it you accept these terms.</p>

        <h2>This site is not medical advice</h2>
        <p>Everything on this website is general information about orthodontic treatment. It is not
          a diagnosis, and it is not a treatment recommendation for you. Orthodontic treatment
          depends on your own bite, and the only way to know what yours needs is an examination.
          Never delay seeking care because of something you read here.</p>

        <h2>No doctor and patient relationship</h2>
        <p>Reading this site or submitting a form does not create a doctor and patient relationship.
          That begins when you attend the practice and we agree to provide care.</p>

        <h2>Prices and offers</h2>
        <p>Figures shown on this site, including down payments, monthly amounts, flat rates and
          promotional discounts, are starting points and current at the time of publication. Your
          own price depends on your treatment plan and is confirmed in writing at your consultation.
          Promotional offers may change or end. Nothing on this site is a binding quotation.</p>

        <h2>Appointments</h2>
        <p>Submitting a form is a request, not a confirmed appointment. We will contact you to
          arrange a time. [TO CONFIRM: the practice&rsquo;s cancellation and missed-appointment
          policy, if it is to appear here.]</p>

        <h2>Intellectual property</h2>
        <p>The text, photographs, logos and design on this site belong to Downtown Orthodontics or
          are used with permission. Please do not reproduce them without asking us first.</p>

        <h2>Links to other sites</h2>
        <p>Where we link to another website we do so for convenience. We do not control those sites
          and are not responsible for their content or their privacy practices.</p>

        <h2>Limitation of liability</h2>
        <p>[CLAUSE TO BE DRAFTED BY THE PRACTICE&rsquo;S COUNSEL. The wording that is enforceable
          here depends on British Columbia law and should not be copied from a template.]</p>

        <h2>Governing law</h2>
        <p>These terms are governed by the laws of the Province of British Columbia and the laws of
          Canada that apply there.</p>

        <h2>Contact</h2>
        <p>Questions about these terms: <a href="tel:+16046623290">(604) 662-3290</a>.</p>
      </div>
    </div>
  </section>
""", counsel=COUNSEL)

C.write("terms.html", C.page(
    title="Terms &amp; Conditions | Downtown Orthodontics",
    desc="The terms on which the Downtown Orthodontics website is provided.",
    slug="terms", body=TERMS))

# ==================================================================== ACCESSIBILITY
ACCESS = phero(
    "Accessibility statement", "Legal",
    "Web accessibility statement.",
    "What we have done to make this site usable for everyone, and how to tell us when it falls "
    "short.",
    actions=False,
) + fill("""
  <section class="block">
    <div class="wrap">
      <div class="prose reveal">
        __COUNSEL__
        <p><b>Last updated:</b> [DATE TO CONFIRM]</p>

        <h2>Our commitment</h2>
        <p>Downtown Orthodontics wants this website to be usable by as many people as possible,
          including people using a screen reader, a keyboard on its own, voice control, or a browser
          set to larger text. We treat accessibility as part of building the site rather than as a
          later addition.</p>

        <h2>What standard we are working to</h2>
        <p>We are working toward the Web Content Accessibility Guidelines version 2.1 at level AA.
          That standard is the reference point used across Canada for public-facing websites.</p>

        <h2>What we have done so far</h2>
        <ul>
          <li>Every interactive control can be reached and operated with a keyboard, and keyboard
            focus is visible.</li>
          <li>Buttons, links and menu items are at least 44 pixels tall so they can be tapped
            reliably.</li>
          <li>Text colours were checked against their backgrounds for contrast, and adjusted where
            they fell short.</li>
          <li>Images that carry meaning have text descriptions, and decorative images are hidden
            from screen readers rather than described pointlessly.</li>
          <li>Form fields have real labels, and are large enough that mobile browsers do not zoom.</li>
          <li>Animation is switched off for anyone whose device asks for reduced motion.</li>
          <li>Expandable sections use the browser&rsquo;s own controls, so assistive technology
            announces them correctly.</li>
        </ul>

        <h2>Where we know we fall short</h2>
        <p>[TO CONFIRM after a formal audit. This site has been checked by the people who built it
          but has not yet been tested by a third party or by people using assistive technology.
          Known gaps will be listed here honestly rather than omitted.]</p>

        <h2>Tell us when something does not work</h2>
        <p>If any part of this site is difficult to use, please call
          <a href="tel:+16046623290">(604) 662-3290</a> and tell us what happened and what you were
          trying to do. We will fix what we can, and in the meantime we will give you the
          information you were after over the phone.</p>

        <h2>Getting care is never conditional on the website</h2>
        <p>If the site is not working for you, the practice still is. Call us and we will book your
          free consultation and answer anything you need answered.</p>
      </div>
    </div>
  </section>
""", counsel=COUNSEL)

C.write("accessibility.html", C.page(
    title="Web Accessibility Statement | Downtown Orthodontics",
    desc="What Downtown Orthodontics has done to make this website usable for everyone, and how to report a problem.",
    slug="accessibility", body=ACCESS))

# ==================================================================== 404
NOTFOUND = phero(
    "Page not found", "404",
    "That page has <em>moved or never existed.</em>",
    "Nothing is broken on your end. Here is where most people are heading.",
    actions=False,
) + fill("""
  <section class="block">
    <div class="wrap">
      <div class="sec-head reveal">
        <h2 class="h2">Where most people <em>are heading.</em></h2>
      </div>
      <div class="paths-grid">
        <a class="path reveal" href="/appointment-request">
          <div class="body">
            <div class="lbl">Book</div>
            <h3>A free <em>consultation.</em></h3>
            <p>A digital scan, a specialist&rsquo;s read on your bite, and your exact price in
              writing. No referral needed.</p>
            <span class="go">Request a consult <span class="arr">&rarr;</span></span>
          </div>
        </a>
        <a class="path reveal d1" href="/financing">
          <div class="body">
            <div class="lbl">Pricing</div>
            <h3>What treatment <em>costs.</em></h3>
            <p>$1,000 down, from $220 a month at 0% in-house interest, with insurance billed
              directly.</p>
            <span class="go">See pricing <span class="arr">&rarr;</span></span>
          </div>
        </a>
        <a class="path reveal d2" href="/">
          <div class="body">
            <div class="lbl">Start over</div>
            <h3>Back to the <em>beginning.</em></h3>
            <p>Braces, Invisalign and kids&rsquo; early care, and the specialist who plans all
              three.</p>
            <span class="go">Go to the homepage <span class="arr">&rarr;</span></span>
          </div>
        </a>
      </div>
    </div>
  </section>
""")

C.write("404.html", C.page(
    title="Page Not Found | Downtown Orthodontics",
    desc="That page has moved or never existed. Here is where most people are heading.",
    slug="404", body=NOTFOUND))
