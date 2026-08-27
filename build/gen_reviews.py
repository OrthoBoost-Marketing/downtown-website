# -*- coding: utf-8 -*-
"""The reviews page. REVIEWS-PAGE-SPEC.

Why this page now exists: CLIENT-BRIEF.md derived "no reviews page" from *review count
unknown and no quotes*. Both halves stopped being true on 2026-08-24. The page spec sizes
a high-volume practice at 24 to 30 reviews, all rendered, with load-more above ~18.

Anatomy, in the spec's order: hero -> aggregate rating band -> skim layer (one-liner
marquee + Google's own topic chips) -> spotlight -> masonry wall -> bridge -> CTA band.

Schema: a `Dentist` node ONLY. No AggregateRating, no Review objects. Marking up
third-party reviews on your own site is self-serving, ineligible for rich results, and a
manual-action risk. The rating is displayed, never marked up.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chrome as C
from common import cta_band, fill, phero
from reviews_data import (COUNT, GOOGLE_TOPICS, GOOGLE_URL, HARVESTED, RATING,
                          REVIEWS, SPOTLIGHT)

STAR = ('<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
        '<path d="M12 2l2.9 6.3 6.9.8-5 4.8 1.3 6.8L12 17.4 5.9 20.7 7.2 13.9l-5-4.8 6.9-.8z"/></svg>')
GMARK = ('<svg class="gmark" width="15" height="15" viewBox="0 0 24 24" aria-hidden="true">'
         '<path fill="#4285F4" d="M23 12.2c0-.8-.1-1.6-.2-2.3H12v4.4h6.2a5.3 5.3 0 01-2.3 3.5v2.9h3.7c2.2-2 3.4-5 3.4-8.5z"/>'
         '<path fill="#34A853" d="M12 23.5c3 0 5.5-1 7.3-2.7l-3.6-2.8a6.9 6.9 0 01-10.3-3.6H1.6v3a11.5 11.5 0 0010.4 6.1z"/>'
         '<path fill="#FBBC05" d="M5.4 14.4a6.9 6.9 0 010-4.4v-3H1.6a11.5 11.5 0 000 10.4z"/>'
         '<path fill="#EA4335" d="M12 5.1c1.6 0 3.1.6 4.3 1.7l3.2-3.2A11.5 11.5 0 001.6 7l3.8 3a6.9 6.9 0 016.6-4.9z"/></svg>')

# Ratings are all five, verified by sorting the profile lowest-first and reading the
# transition point. See the header of reviews_data.py for the method and the full
# non-5-star exclusion list.
STARS5 = '<span class="stars" role="img" aria-label="Rated 5 out of 5">%s</span>' % (STAR * 5)

FIRST_RENDERED = 9  # the rest ship in the HTML with `hidden`, never JS-injected


def initial(name):
    for ch in name:
        if ch.isalpha():
            return ch.upper()
    return "?"


def card(name, when, chip, text, hidden):
    return fill("""
        <figure class="rc reveal"__HID__>
          <div class="rc-top">__STARS__ __GMARK__</div>
          <blockquote>&ldquo;__TEXT__&rdquo;</blockquote>
          <figcaption><span class="ava">__INI__</span><span class="who"><b>__NAME__</b><span>__WHEN__ &middot; Google review</span></span></figcaption>
          <span class="chip">__CHIP__</span>
        </figure>""",
                hid=" hidden" if hidden else "", stars=STARS5, gmark=GMARK,
                text=text, ini=initial(name), name=name, when=when, chip=chip)


# ------------------------------------------------------------------ skim one-liners
# Eight short verbatim fragments, each already present in a full card below, so nothing
# here is a claim the wall does not also carry.
LINERS = [
    ("Dr. Daher gave me hope when I really needed it&hellip;", "Lomish Bhangu"),
    ("He did my original Invisalign in 2007 and teeth have not shifted.", "Kim Patara"),
    ("&hellip;my biggest regret is that I didn&rsquo;t come across his excellent clinic sooner.", "Alex Bobylev"),
    ("&hellip;an outstanding result that was well worth the investment.", "Riaz Meghji"),
    ("&hellip;I&rsquo;ve never felt rushed or pressured to finish my treatment quicker.", "Vee L"),
    ("&hellip;got an appointment the same day I called.", "SassySips"),
    ("Both of my kids like him a lot!", "Fiona Deng"),
    ("I always looked forward to going to my ortho appointments (which is crazy!)", "Jayden Dinh"),
]

liners = "\n".join(
    '          <span class="liner">&ldquo;%s&rdquo; <cite>%s</cite></span>' % (q, who)
    for q, who in LINERS)

topics = "".join(
    '<span><span>%s</span><b>%d</b></span>' % (label, n) for label, n in GOOGLE_TOPICS)

wall = "".join(
    card(name, when, chip, text, hidden=(i >= FIRST_RENDERED))
    for i, (name, when, chip, text, _job) in enumerate(REVIEWS))

hidden_count = max(0, len(REVIEWS) - FIRST_RENDERED)

sp_name, sp_when, sp_chip, sp_text, _sp_job = SPOTLIGHT

BODY = fill("""
__HERO__

  <!-- AGGREGATE BAND. Displayed, never marked up: no AggregateRating anywhere on this
       page. The link out to the profile is the canonical cid URL, the same one the
       homepage rating line uses. -->
  <section class="block rv-agg" style="padding-block: var(--sp-9);">
    <div class="wrap">
      <h2 class="h2 reveal" style="text-align:center;margin-bottom:var(--sp-6);">The verdict, <em>in one number.</em></h2>
      <div class="inner reveal">
        <span class="score">__RATING__</span>
        <span class="meta">out of 5, from
          <a href="__GURL__" target="_blank" rel="noopener">__COUNT__ Google reviews</a>.
          Every review on this page is a verified five-star review, quoted verbatim.</span>
      </div>
      <div class="rv-topics reveal">
        <span class="lbl">What patients mention most, by Google&rsquo;s own count</span>
        __TOPICS__
      </div>
    </div>
  </section>

  <!-- SKIM LAYER. The spec's strongest steal: a skimmer gets the verdict in about four
       seconds before the long wall. It is a MARQUEE, permitted on this site under the
       three house conditions, and it uses the homepage's own .mq component and shared
       controller, so it pauses on tap, hover, focus and the keyboard, drags on desktop
       and on mobile, and every line sits in the static HTML for crawlers. Each fragment
       is also present in full in a card below. -->
  <section class="block" style="padding-block: var(--sp-9) var(--sp-8);">
    <div class="wrap">
      <h2 class="sr-only">Patient reviews at a glance</h2>
      <div class="mq-wrap reveal">
        <div class="mq mq-liners" data-marquee data-speed="0.3" tabindex="0" role="region"
             aria-label="Short quotes from patient reviews, scrollable. Drag or use the arrow keys.">
__LINERS__
        </div>
        <div class="mq-bar">
          <button class="mq-ctl" type="button" data-marquee-toggle aria-pressed="false">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><rect x="6" y="5" width="4" height="14" rx="1"/><rect x="14" y="5" width="4" height="14" rx="1"/></svg>
            <span data-marquee-label>Pause</span>
          </button>
          <span class="mq-hint">Drag to browse, or tap to pause.</span>
        </div>
      </div>
    </div>
  </section>

  <!-- SPOTLIGHT: the single most narrative review, promoted out of the wall into its own
       band. It is the strongest proof on the profile for the conservative-treatment claim
       the rest of the site makes, and it is this patient's account of her own case, not a
       clinical promise. -->
  <section class="block rv-spot">
    <div class="wrap">
      <figure class="inner reveal">
        <h2 class="eyebrow">(One patient&rsquo;s account)</h2>
        <blockquote>&ldquo;__SPTEXT__&rdquo;</blockquote>
        <figcaption><span class="ava">__SPINI__</span><span class="who"><b>__SPNAME__</b><span>__SPWHEN__ &middot; Google review &middot; __SPCHIP__</span></span></figcaption>
      </figure>
    </div>
  </section>

  <!-- THE WALL. Masonry via column-count, not an equal-height grid. The first nine are
       rendered and the remaining __HIDDEN__ ship in the HTML with `hidden`, revealed by
       the load-more below. Never JS-injected: that keeps every review crawlable and the
       page CLS-safe. -->
  <section class="block" id="all-reviews">
    <div class="wrap">
      <div class="sec-head center reveal">
        <span class="eyebrow">(All of them)</span>
        <h2 class="h2">Twenty-eight reviews, <em>in full.</em></h2>
        <p>Harvested from the practice&rsquo;s Google profile on __HARVESTED__ and quoted word for
          word. Trimmed only for length, never reworded.</p>
      </div>
      <div class="rv-wall">__WALL__
      </div>
      <div class="rv-more reveal">
        <button class="btn btn-outline" type="button" id="rv-more-btn"
                aria-controls="all-reviews" aria-expanded="false">Show all __TOTAL__ reviews</button>
      </div>
    </div>
  </section>

  <!-- BRIDGE. Catches the reader at peak trust and feeds the money pages. -->
  <section class="block" style="background:var(--surface); padding-block: var(--sp-9);">
    <div class="wrap">
      <h2 class="sr-only">Where to go next</h2>
      <p class="rv-bridge reveal">Most of these patients arrived with the same questions you have.
        See <a href="/financing">exactly what treatment costs</a>, read
        <a href="/why-choose-us">why a specialist and not a shortcut</a>, or
        <a href="/dr-sam-daher">meet Dr. Daher</a> before you book anything.</p>
    </div>
  </section>

__CTA__

  <!-- Load-more: ~30 lines of vanilla JS, no dependency, and it only reveals nodes that
       are already in the document. The button removes itself once everything is shown. -->
  <script>
  (function () {
    var btn = document.getElementById('rv-more-btn');
    if (!btn) return;
    btn.addEventListener('click', function () {
      var hidden = document.querySelectorAll('.rv-wall .rc[hidden]');
      for (var i = 0; i < hidden.length; i++) {
        hidden[i].removeAttribute('hidden');
        hidden[i].classList.add('in');           // the reveal observer has already run
      }
      btn.setAttribute('aria-expanded', 'true');
      btn.parentNode.removeChild(btn);
      var first = hidden[0];
      if (first) { first.setAttribute('tabindex', '-1'); first.focus({ preventScroll: true }); }
    });
  })();
  </script>
""",
            hero=phero(
                "Reviews",
                "(Patient reviews)",
                "What our patients in <em>downtown Vancouver</em> say.",
                "Twenty-eight verified five-star Google reviews, quoted word for word. "
                "Complex cases other offices turned down, results still holding eighteen "
                "years on, and the same specialist at every visit."),
            rating=RATING, gurl=GOOGLE_URL, count=str(COUNT), topics=topics,
            liners=liners, wall=wall, harvested=HARVESTED,
            total=str(len(REVIEWS)), hidden=str(hidden_count),
            sptext=sp_text, spini=sp_name[0], spname=sp_name, spwhen=sp_when, spchip=sp_chip,
            cta=cta_band(
                "Your case is the one <em>we have not heard yet.</em>",
                "A free consultation with Dr. Daher gets you a specialist&rsquo;s diagnosis, honest "
                "options and an exact price. What you do next is up to you.",
                # Concatenated, not %-formatted: this string contains a literal "0%",
                # which Python reads as a format spec. Same trap as common.py.
                "Free consultation. No referral needed. $1,000 down, from $220/mo at 0% in-house "
                "financing. <a href=\"" + GOOGLE_URL + "\" target=\"_blank\" rel=\"noopener\">"
                "Leave us a review</a>."),
            )

# `Dentist` only. No AggregateRating. No Review objects. This is the spec's one loud rule
# and two of its three reference sites get it wrong.
SCHEMA = """{
  "@context": "https://schema.org",
  "@type": "Dentist",
  "@id": "%(d)s/#practice",
  "name": "Downtown Orthodontics",
  "mainEntityOfPage": { "@id": "%(d)s/reviews" }
}""" % {"d": C.DOMAIN} % {"d": C.DOMAIN}

C.write("reviews.html", C.page(
    title="Patient Reviews | Downtown Orthodontics, Vancouver, BC",
    desc=("Twenty-eight verified five-star Google reviews for Downtown Orthodontics "
          "in downtown Vancouver, quoted word for word."),
    slug="reviews",
    body=BODY,
    schema=SCHEMA,
))
