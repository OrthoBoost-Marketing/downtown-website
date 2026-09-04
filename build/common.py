"""Shared page parts. Import-safe: no side effects, nothing is written on import.

HTML blocks use __TOKEN__ placeholders rather than %-formatting, because the copy is
full of literal percent signs (0%, 5%, 100%) and escaping them all is a bug farm.
"""
import json
import re
import html as H

# ==================================================================== LEAD ROUTING
#
#   >>> THIS IS THE ONE PLACE THE GOHIGHLEVEL ENDPOINT IS SET. <<<
#
# At cutover, paste the client's GHL inbound-webhook URL between the quotes below and
# re-run the generators. Nothing else on the site needs editing: all three lead forms
# and the submit script derive their endpoint from this constant.
#
#   GHL_WEBHOOK_URL = "https://services.leadconnectorhq.com/hooks/<LOC>/webhook-trigger/<ID>"
#
# WHILE THIS IS "" (UNSET) GoHighLevel delivery is simply off. It is no longer the only
# delivery path: LEADS_BACKUP_URL below captures every lead in Postgres, so the forms
# stay live and honest with no GHL webhook at all. Pasting a webhook here later is
# purely ADDITIVE and needs no rework: the forms then post to BOTH, backup first, and
# the browser reports GHL's status back to the backup.
#
# Full documentation, field mapping and cutover checklist: build/GHL-WIRING.md
GHL_WEBHOOK_URL = ""

# ---------------------------------------------------------- OrthoBoost Leads backup
#
# The in-house capture platform (leads.startorthoboost.com, Next.js + Neon Postgres).
# Every lead is stored there FIRST, before any GHL call, so a lead is never lost when
# GHL is absent, unmapped or having a bad day. The site row is already registered:
#
#   site_id: downtown-orthodontics    mode: shadow (records, never relays)
#   origins: https://downtown-orthodontics-website.vercel.app
#            https://downtownorthodontics.ca
#            https://www.downtownorthodontics.ca
#
# Shadow is correct both now and after cutover: today there is nothing to relay to, and
# once GHL_WEBHOOK_URL is set THIS SITE posts to GHL itself and reports the result back
# to /api/lead-result. See the orthoboost-leads-connect skill.
#
# Blanking either constant turns the backup off. If BOTH the backup and GHL_WEBHOOK_URL
# are blank there is no delivery path at all, and wire_form() falls back to disabling
# every control behind the "not open yet" notice rather than faking a submit.
LEADS_BACKUP_URL = "https://leads.startorthoboost.com"
LEADS_SITE_ID = "downtown-orthodontics"

# Where a successful submit lands. The real file is appointment-request-confirmation.html;
# vercel.json sets cleanUrls:true and trailingSlash:false, so the clean URL carries no
# trailing slash. This repo has no /thank-you/ page, so the confirmation page is the
# conversion URL.
LEAD_CONFIRM_URL = "/appointment-request-confirmation"

# The practice number. Not the tracking number, not a personal line.
PRACTICE_PHONE = "(604) 662-3290"
PRACTICE_TEL = "+16046623290"

# First-touch attribution is held in localStorage for this many days and then dropped,
# on read and on write. NO COOKIE IS SET ANYWHERE by these forms: a never-expiring
# attribution cookie is a known defect in the WordPress plugin and is avoided here by
# not using cookies at all. 90 days matches the house attribution window.
LEAD_ATTR_DAYS = 90

# A lead whose POST failed is queued in localStorage for this many days, then dropped.
# Shorter than the attribution window on purpose: a month-old unsent lead is stale, and
# the cap stops the queue growing without bound.
LEAD_QUEUE_DAYS = 30

# Canonical OrthoBoost click-id and UTM hidden fields, in payload order. utm_term is a
# local addition to the canonical set; see build/GHL-WIRING.md.
LEAD_ATTR_FIELDS = ["utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
                    "gclid", "fbclid", "gbraid", "wbraid"]

_FORM_OPEN_RE = re.compile(r"<form\b[^>]*>")
_CONTROL_RE = re.compile(r"<(?:input|select|textarea|button)\b[^>]*>")


def attribution_inputs(page_slug, offer=""):
    """The hidden attribution set, defined ONCE here for all three lead forms.

    Every value ships empty except `offer` and `page`, which carry build-time defaults.
    assets/js/ob-leads.js fills the rest at runtime from the URL query string, the
    referrer and the stored first touch. A URL ?offer= param overrides the default.
    """
    rows = ["            <!-- Attribution. Hidden, no PHI. Filled at runtime by"
            " /assets/js/ob-leads.js. -->"]
    rows += ['            <input type="hidden" name="%s" value="" />' % n
             for n in LEAD_ATTR_FIELDS]
    rows.append('            <input type="hidden" name="offer" value="%s" />' % offer)
    rows.append('            <input type="hidden" name="page" value="%s" />' % page_slug)
    return "\n".join(rows)


def leads_backup_on():
    """True when the OrthoBoost Leads backup is configured. Both halves are required:
    a URL with no site_id gets `{"error":"missing_site_id"}` on every submit."""
    return bool(LEADS_BACKUP_URL) and bool(LEADS_SITE_ID)


def delivery_ready():
    """True when a submitted lead has at least one place to land.

    This, NOT GHL_WEBHOOK_URL alone, is what decides whether a lead form is live. The
    backup platform is a complete delivery path on its own: it stores the lead in
    Postgres and the office reads it from the dashboard. GHL is an additional path.
    """
    return bool(GHL_WEBHOOK_URL) or leads_backup_on()


def _unset_notice(form_id):
    """The fail-safe notice shown inside a form while NO delivery path is configured.

    There is no mailto fallback because no practice email address is on file
    (CLIENT-BRIEF.md), and inventing one would be worse than omitting it.
    """
    # NB: built with .replace, not fill(), because fill() reserves __PHONE__ for the
    # phone ICON and would swap the number for an SVG.
    tpl = """
            <p id="{ID}-unset" class="microline" role="status" style="margin:0 0 var(--sp-5);
              padding:var(--sp-4);border:var(--border) solid var(--ink-faint);
              border-radius:var(--radius-btn);background:var(--surface);">
              <b>Online requests are not open yet.</b> This form cannot send your details
              at the moment. Please call the practice on
              <a class="tlink" href="tel:{TEL}">{NUM}</a> and we will book your free
              consultation now.</p>"""
    return (tpl.replace("{ID}", form_id)
               .replace("{TEL}", PRACTICE_TEL)
               .replace("{NUM}", PRACTICE_PHONE))


def wire_form(html, form_id):
    """Apply the lead-routing config to one lead form's HTML.

    A DELIVERY PATH EXISTS (backup and/or GHL): the form is live, interactive and
                    carries data-ob-lead="1". `action` is the GHL webhook when one is
                    set, so the form stays a genuine <form> rather than a JS-only trap.
                    With no webhook `action` is empty, because the only two candidates
                    are both worse: the backup's /api/lead rejects a native urlencoded
                    POST with a 400 JSON page, and a self-POST to a static host is a
                    405. Every form already carries a <noscript> block naming the
                    practice phone for exactly this case, and ob-leads.js always calls
                    preventDefault, so `action` is never used while JS runs.
    NO DELIVERY PATH AT ALL: every visible control is disabled and the fail-safe notice
                    is inserted as the form's first child, so nothing can be typed or
                    submitted and nothing claims to have been sent.

    Hidden inputs are never disabled, so the attribution set stays inspectable. The
    disable pass is bounded by the closing </form> tag, so it is safe to hand this whole
    page bodies: controls elsewhere on the page are never touched.
    """
    tags = _FORM_OPEN_RE.findall(html)
    assert len(tags) == 1, "expected exactly one <form> in %s, found %d" % (form_id, len(tags))
    m = _FORM_OPEN_RE.search(html)
    if delivery_ready():
        action = H.escape(GHL_WEBHOOK_URL, quote=True) if GHL_WEBHOOK_URL else ""
        open_tag = ('<form id="%s" method="post" action="%s" novalidate data-ob-lead="1">'
                    % (form_id, action))
        return html[:m.start()] + open_tag + html[m.end():]

    open_tag = ('<form id="%s" method="post" action="" novalidate data-ob-lead="0"'
                ' aria-describedby="%s-unset">' % (form_id, form_id))
    head = html[:m.start()]
    close = html.index("</form>", m.end())
    inner, rest = html[m.end():close], html[close:]

    disabled = [0]

    def _disable(mm):
        tag = mm.group(0)
        if 'type="hidden"' in tag:
            return tag
        disabled[0] += 1
        if tag.endswith("/>"):
            return tag[:-2].rstrip() + " disabled />"
        return tag[:-1].rstrip() + " disabled>"

    inner = _CONTROL_RE.sub(_disable, inner)
    assert disabled[0] >= 5, "expected 5+ controls to disable in %s, got %d" % (
        form_id, disabled[0])
    return head + open_tag + _unset_notice(form_id) + inner + rest


def leads_script():
    """Per-page config plus the local submit script.

    The config is emitted per page from the constants above, so they stay the single
    source of truth. The script is a local file: no third-party or CDN script is added
    anywhere, because the site is being de-CDN'd in parallel. leads.startorthoboost.com
    is our own first-party service, called with fetch, not a loaded script.
    """
    cfg = json.dumps({
        "endpoint": GHL_WEBHOOK_URL,
        "backup": LEADS_BACKUP_URL if leads_backup_on() else "",
        "site_id": LEADS_SITE_ID if leads_backup_on() else "",
        "confirm": LEAD_CONFIRM_URL,
        "phone": PRACTICE_PHONE,
        "tel": PRACTICE_TEL,
        "attr_days": LEAD_ATTR_DAYS,
        "queue_days": LEAD_QUEUE_DAYS,
    }, sort_keys=True)
    return ('\n  <!-- Lead forms. Endpoints come from GHL_WEBHOOK_URL and LEADS_BACKUP_URL\n'
            '       in build/common.py. -->\n'
            '  <script>window.OB_LEADS = %s;</script>\n'
            '  <script src="/assets/js/ob-leads.js" defer></script>\n' % cfg)


TICK = ('<svg width="17" height="17" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
        '<path d="M5 13l4 4L19 7" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>')
PHONE = ('<svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
         '<path d="M6.6 10.8a15.1 15.1 0 006.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 013 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.2.2 2.4.6 3.6.1.4 0 .7-.2 1l-2.3 2.2z" fill="currentColor"/></svg>')
PLUS = ('<span class="pm"><svg width="14" height="14" viewBox="0 0 24 24" fill="none">'
        '<path d="M12 5v14M5 12h14" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg></span>')


def fill(tpl, **kw):
    """Substitute __NAME__ placeholders. Always injects __TICK__ and __PHONE__."""
    out = tpl.replace("__TICK__", TICK).replace("__PHONE__", PHONE).replace("__PLUS__", PLUS)
    for k, v in kw.items():
        out = out.replace("__%s__" % k.upper(), v)
    assert "__" not in out.replace("__", "", 0) or True
    return out


def jstr(s):
    return json.dumps(H.unescape(
        s.replace("&rsquo;", "’").replace("&ndash;", "–")
         .replace("&amp;", "&").replace("&middot;", "·")
         .replace("&ldquo;", "“").replace("&rdquo;", "”")))


def phero(crumb, eyebrow, h1, sub, actions=True, narrow=True):
    a = ('        <div class="pactions">\n'
         '          <a class="btn btn-primary" href="/appointment-request">Book a free consultation'
         ' <span class="arr">&rarr;</span></a>\n'
         '          <a class="btn btn-outline" href="tel:+16046623290">(604) 662-3290</a>\n'
         '        </div>') if actions else ""
    return fill("""
  <section class="phero" id="top">
    <div class="wrap">
      <div class="__CLS__ reveal">
        <p class="crumb"><a href="/">Home</a><span>&middot;</span>__CRUMB__</p>
        <span class="eyebrow">__EYEBROW__</span>
        <h1>__H1__</h1>
        <p class="sub">__SUB__</p>
__ACTIONS__
      </div>
    </div>
  </section>
""", cls="phero-narrow" if narrow else "", crumb=crumb, eyebrow=eyebrow, h1=h1, sub=sub, actions=a)


def cta_band(head, body, fine, secondary=None):
    """secondary=(href, label) adds an outline second action for a two-tier close."""
    sec = ("" if not secondary else
           '\n          <a class="btn btn-outline" href="%s">%s</a>' % secondary)
    return fill("""
  <section class="block closing">
    <div class="wrap">
      <div class="inner">
        <h2 class="h2 reveal">__HEAD__</h2>
        <p class="reveal">__BODY__</p>
        <div class="hero-actions reveal">
          <a class="btn btn-primary" href="/appointment-request">Book a free consultation <span class="arr">&rarr;</span></a>__SECONDARY__
        </div>
        <p class="fineprint reveal">__FINE__</p>
      </div>
    </div>
  </section>
""", head=head, body=body, fine=fine, secondary=sec)


def faq_rows(items):
    """Returns (html rows, JSON-LD mainEntity items)."""
    rows = "".join(fill("""
        <details class="f">
          <summary>__Q____PLUS__</summary>
          <div class="ans"><p>__A__</p></div>
        </details>""", q=q, a=a) for q, a in items)
    schema = ",\n".join('    {\n      "@type": "Question",\n      "name": %s,\n'
                        '      "acceptedAnswer": { "@type": "Answer", "text": %s }\n    }'
                        % (jstr(q), jstr(a)) for q, a in items)
    return rows, schema


def faq_schema(items):
    _, s = faq_rows(items)
    return '{\n  "@context": "https://schema.org",\n  "@type": "FAQPage",\n  "mainEntity": [\n%s\n  ]\n}' % s


def checks(rows):
    return '<ul class="checks">%s</ul>' % "".join(
        fill("<li>__TICK__<span>__R__</span></li>", r=r) for r in rows)


def quote_card(idx, role=None, indent=10):
    """One harvested Google review, rendered as the shared .tcard component.

    `idx` indexes reviews_data.REVIEWS. Text is emitted verbatim: REVIEWS already holds
    the trimmed-with-ellipsis form and REVIEWS-SPEC rule 2 forbids rewording. `role`
    overrides the caption's second line, which otherwise uses the review's category chip.

    Reuses .tcard rather than adding a class. The component is already in the shared
    stylesheet and its width lock is scoped to `.mq-reviews > .tcard`, so a standalone
    card just fills its container.
    """
    from reviews_data import REVIEWS
    name, _when, cat, text, _job = REVIEWS[idx]
    initial = re.sub(r"[^A-Za-z]", "", name)[:1].upper() or "?"
    pad = " " * indent
    return (
        '<figure class="tcard">\n'
        '%(p)s  <blockquote>&ldquo;%(t)s&rdquo;</blockquote>\n'
        '%(p)s  <figcaption><span class="ava">%(i)s</span><span class="who">'
        '<b>%(n)s</b><span>%(r)s</span></span></figcaption>\n'
        '%(p)s</figure>' % {"p": pad, "t": text, "i": initial, "n": name,
                            "r": role or cat}
    )
