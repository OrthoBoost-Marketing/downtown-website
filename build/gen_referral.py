"""Referring-dentist page and its confirmation page.

Requested by Maya on 2026-09-11: a form for doctors to refer a patient, laid out like
vancouverbraces.com/site/orthodontist-referrals. That layout is a short hero, ONE form
in two groups (Referring doctor, then Patient information) and a "Questions?" band.

Delivery runs on GHL_REFERRAL_WEBHOOK_URL (build/common.py), NOT the patient-form
webhook, and the form stays disabled until that URL is set. See the note there.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chrome as C
from common import TICK, PHONE, phero, fill
from common import attribution_inputs, wire_form, leads_script
from common import GHL_REFERRAL_WEBHOOK_URL, PRACTICE_PHONE, PRACTICE_TEL

CONFIRM = "/referral-confirmation"

# The patient's name, phone and email use the canonical names (first_name, last_name,
# phone, email), so the GHL contact and the leads backup row are the PATIENT, the person
# the office books. Everything else is data-extra: ob-leads.js sends each under its own
# key and writes a labelled summary into `message` for the notification. The data-extra
# value is the label used in that summary.
FIELD = """              <div class="field%(wide)s">
                <label for="%(id)s">%(label)s</label>
                <input id="%(id)s" name="%(name)s" type="%(type)s"%(auto)s data-extra="%(summary)s"%(req)s />
              </div>"""


def field(id_, name, label, summary, type_="text", auto="", req=True, wide=False):
    return FIELD % {"id": id_, "name": name, "label": label, "type": type_,
                    "summary": summary, "wide": " wide" if wide else "",
                    "auto": ' autocomplete="%s"' % auto if auto else "",
                    "req": " required" if req else ""}


DOCTOR = "\n".join([
    field("r-doc", "ref_doctor", "Doctor name", "Referring doctor", auto="off"),
    field("r-office", "ref_office", "Office", "Office", auto="organization"),
    field("r-docemail", "ref_email", "Email address", "Doctor email", type_="email", auto="off"),
    field("r-docphone", "ref_phone", "Phone", "Doctor phone", type_="tel", auto="off"),
])

PATIENT = "\n".join([
    field("r-first", "first_name", "Patient first name", "Patient first name", auto="off"),
    field("r-last", "last_name", "Patient last name", "Patient last name", auto="off"),
    field("r-dob", "patient_dob", "Patient date of birth", "Patient date of birth", type_="date"),
    field("r-guardian", "guardian_names", "Parent or guardian names (if applicable)",
          "Parent or guardian", req=False),
    field("r-phone", "phone", "Patient phone", "Patient phone", type_="tel", auto="off"),
    field("r-email", "email", "Patient email", "Patient email", type_="email", auto="off"),
])

NOTICE = ("<b>Online referrals are not open yet.</b> This form cannot send at the moment.\n"
          "              Please call the practice on\n"
          '              <a class="tlink" href="tel:%s">%s</a> and our team will take the\n'
          "              referral by phone." % (PRACTICE_TEL, PRACTICE_PHONE))

BODY = phero(
    "Refer a patient", "For dentists",
    "Refer a patient to <em>Dr. Daher.</em>",
    "Fill in the form below and a member of our team will contact your patient to book "
    "their consultation.",
    actions=False,
) + fill("""
  <section class="block">
    <div class="wrap">
      <div class="formcard reveal" style="max-width:760px;margin:0 auto;">
        <form method="post" action="" novalidate>
          <h2>Referring doctor</h2>
          <div class="fgrid">
__DOCTOR__
          </div>
          <h2 style="margin-top:var(--sp-7);">Patient information</h2>
          <div class="fgrid">
__PATIENT__
            <div class="field wide">
              <label for="r-reason">Reason for consultation or comments</label>
              <textarea id="r-reason" name="reason" rows="5" data-extra="Reason for consultation" required style="min-height:120px;min-width:0;width:100%;font-family:var(--font);font-size:16px;color:var(--ink);background:var(--bg);border:var(--border) solid var(--ink-faint);border-radius:var(--radius-btn);padding:var(--sp-3) var(--sp-4);"></textarea>
            </div>
          </div>
__ATTRIBUTION__
          <button class="btn btn-primary" type="submit">Send referral <span class="arr">&rarr;</span></button>
        </form>
        <p class="microline">Sending radiographs, photos or a referral letter? Mention them in
          the comments and our team will arrange a secure way to receive them. Please include
          only what we need to book the consultation.</p>
        <noscript>
          <p class="microline">This form needs JavaScript to send your referral. Please call
            the practice on <a class="tlink" href="tel:+16046623290">(604) 662-3290</a>.</p>
        </noscript>
        <!-- The reason box is the referral's clinical summary, which a referral cannot
             do without. It is the one deliberate exception to the no-PHI form rule. -->
      </div>
    </div>
  </section>

  <section class="block" style="background:var(--surface);">
    <div class="wrap">
      <div class="reqgrid">
        <div class="reveal">
          <h2 class="h2">Questions? <em>Get in touch.</em></h2>
          <p style="margin-top:var(--sp-5);">Our team is happy to talk through a case before you
            refer, or to help with anything after. Call the practice any time we&rsquo;re open.</p>
          <a class="big-tel" href="tel:+16046623290" style="margin-top:var(--sp-6);">__PHONE__ (604) 662-3290</a>
        </div>
        <div class="reveal d1">
          <ul class="checks">
            <li>__TICK__<span><b>840 W Hastings St</b><br />Vancouver, BC V6C 1C8<br />
              <a class="tlink" href="https://www.google.com/maps/search/?api=1&amp;query=840+W+Hastings+St+Vancouver+BC+V6C+1C8" target="_blank" rel="noopener">Open in Maps &rarr;</a></span></li>
            <li>__TICK__<span><b>Monday</b> 10:00 to 18:00<br /><b>Tuesday</b> 08:00 to 15:00<br />
              <b>Wednesday</b> 08:00 to 16:30<br /><b>Thursday</b> 08:00 to 15:00<br />
              <span style="color:var(--ink-faint);">Friday to Sunday, closed</span></span></li>
          </ul>
        </div>
      </div>
    </div>
  </section>
""", doctor=DOCTOR, patient=PATIENT, attribution=attribution_inputs("referring-dentists"))

BODY = (wire_form(BODY, "lead-referral", endpoint=GHL_REFERRAL_WEBHOOK_URL, notice=NOTICE)
        + leads_script(endpoint=GHL_REFERRAL_WEBHOOK_URL, confirm=CONFIRM))

SCHEMA = """{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": "Refer a patient to Downtown Orthodontics",
  "url": "https://downtownorthodontics.ca/referring-dentists",
  "isPartOf": { "@id": "https://downtownorthodontics.ca/#practice" },
  "about": { "@id": "https://downtownorthodontics.ca/#practice" }
}"""

C.write("referring-dentists.html", C.page(
    title="Refer a Patient | Downtown Orthodontics, Vancouver",
    desc="Dentists and specialists: refer a patient to Dr. Sam Daher at Downtown Orthodontics, 840 W Hastings St, Vancouver. Our team contacts your patient to book.",
    slug="referring-dentists", body=BODY, schema=SCHEMA))

# ==================================================================== CONFIRMATION
CONF_BODY = phero(
    "Referral sent", "Thank you",
    "Referral <em>received.</em>",
    "Thank you for the referral. A member of our team will contact your patient to book "
    "their consultation. If anything is urgent, please call us on (604) 662-3290.",
    actions=False,
) + fill("""
  <section class="block">
    <div class="wrap" style="text-align:center;">
      <a class="btn btn-primary" href="/">Back to the homepage <span class="arr">&rarr;</span></a>
    </div>
  </section>
""") + leads_script(endpoint=GHL_REFERRAL_WEBHOOK_URL, confirm=CONFIRM)

C.write("referral-confirmation.html", C.page(
    title="Referral Received | Downtown Orthodontics",
    desc="Your referral to Downtown Orthodontics has been received.",
    slug="referral-confirmation", body=CONF_BODY, noindex=True))
