"""Shared page parts. Import-safe: no side effects, nothing is written on import.

HTML blocks use __TOKEN__ placeholders rather than %-formatting, because the copy is
full of literal percent signs (0%, 5%, 100%) and escaping them all is a bug farm.
"""
import json
import html as H

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


def cta_band(head, body, fine):
    return fill("""
  <section class="block closing">
    <div class="wrap">
      <div class="inner">
        <h2 class="h2 reveal">__HEAD__</h2>
        <p class="reveal">__BODY__</p>
        <div class="hero-actions reveal">
          <a class="btn btn-primary" href="/appointment-request">Book a free consultation <span class="arr">&rarr;</span></a>
        </div>
        <p class="fineprint reveal">__FINE__</p>
      </div>
    </div>
  </section>
""", head=head, body=body, fine=fine)


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
