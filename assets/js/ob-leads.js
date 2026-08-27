/* Downtown Orthodontics lead forms.
 *
 * No dependencies and no third-party script. The only network call this file can make
 * is the POST to the GoHighLevel webhook itself.
 *
 * Configuration arrives as window.OB_LEADS, emitted per page by the Python generators
 * from GHL_WEBHOOK_URL in build/common.py, which is the one place the endpoint is set.
 *
 * While the endpoint is unset the generators already ship every form disabled with a
 * notice, so this file does nothing on submit. It still runs, because it also fires the
 * ob_generate_lead event on the confirmation page.
 *
 * Storage (localStorage only, never a cookie):
 *   ob_attr_first_touch_v1  first-touch attribution, expires after OB_LEADS.attr_days
 *   ob_lead_queue_v1        leads whose POST failed, expires after OB_LEADS.queue_days
 *   ob_lead_event_pending_v1 (sessionStorage) one-shot flag for the confirmation event
 *
 * Retrieve queued leads from the browser console:  obLeadQueue()
 */
(function () {
  'use strict';

  var CFG = window.OB_LEADS || {};
  var ENDPOINT = String(CFG.endpoint || '').trim();
  var CONFIRM = CFG.confirm || '/appointment-request-confirmation';
  var PHONE = CFG.phone || '';
  var TEL = CFG.tel || '';

  var ATTR_KEY = 'ob_attr_first_touch_v1';
  var QUEUE_KEY = 'ob_lead_queue_v1';
  var EVENT_KEY = 'ob_lead_event_pending_v1';
  var ATTR_MS = (CFG.attr_days || 90) * 864e5;
  var QUEUE_MS = (CFG.queue_days || 30) * 864e5;
  var QUEUE_MAX = 20;

  var PARAMS = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content',
                'gclid', 'fbclid', 'gbraid', 'wbraid', 'offer'];

  /* ---------------------------------------------------------------- storage
     Every access is wrapped: private-browsing modes throw on the property itself,
     not just on set, so even reading has to be guarded. */
  function lsGet(k) { try { return window.localStorage.getItem(k); } catch (e) { return null; } }
  function lsSet(k, v) { try { window.localStorage.setItem(k, v); return true; } catch (e) { return false; } }
  function lsDel(k) { try { window.localStorage.removeItem(k); } catch (e) { /* ignore */ } }
  function ssGet(k) { try { return window.sessionStorage.getItem(k); } catch (e) { return null; } }
  function ssSet(k, v) { try { window.sessionStorage.setItem(k, v); return true; } catch (e) { return false; } }
  function ssDel(k) { try { window.sessionStorage.removeItem(k); } catch (e) { /* ignore */ } }
  function parse(s) { try { return JSON.parse(s); } catch (e) { return null; } }

  /* ---------------------------------------------------------------- attribution */
  function query() {
    var out = {};
    var s = String(location.search || '').replace(/^\?/, '');
    if (!s) return out;
    s.split('&').forEach(function (pair) {
      if (!pair) return;
      var i = pair.indexOf('=');
      var rawK = i < 0 ? pair : pair.slice(0, i);
      var rawV = i < 0 ? '' : pair.slice(i + 1);
      var k, v;
      try { k = decodeURIComponent(rawK.replace(/\+/g, ' ')); } catch (e) { k = rawK; }
      try { v = decodeURIComponent(rawV.replace(/\+/g, ' ')); } catch (e) { v = rawV; }
      if (k) out[k] = v;
    });
    return out;
  }

  function refHost() {
    var ref = document.referrer || '';
    if (!ref) return '';
    try { return new URL(ref).hostname.replace(/^www\./, ''); } catch (e) { return ''; }
  }

  /* A visitor with no UTMs at all still gets a usable source and medium, so the GHL
     contact is never blank on attribution. */
  function inferred(q) {
    var src = q.utm_source || '';
    var med = q.utm_medium || '';
    if (src) return { utm_source: src, utm_medium: med };
    var host = refHost();
    var self = String(location.hostname || '').replace(/^www\./, '');
    if (q.gclid || q.gbraid || q.wbraid) return { utm_source: 'google', utm_medium: med || 'cpc' };
    if (q.fbclid) return { utm_source: 'facebook', utm_medium: med || 'paid-social' };
    if (host && host !== self) return { utm_source: host, utm_medium: med || 'referral' };
    return { utm_source: 'direct', utm_medium: med || 'none' };
  }

  /* First touch is written once and then left alone, so a visitor who arrives from an
     ad and converts on a later page keeps the ad's attribution. The record carries its
     own expiry and is dropped on read once past it: nothing here lives forever. */
  function firstTouch(q) {
    var rec = parse(lsGet(ATTR_KEY));
    if (rec && rec.exp && Date.now() <= rec.exp && rec.data) return rec;
    if (rec) lsDel(ATTR_KEY);

    // sessionStorage mirror covers the case where localStorage is blocked but
    // sessionStorage is not, so first touch still survives internal navigation.
    var mirror = parse(ssGet(ATTR_KEY));
    if (mirror && mirror.data) return mirror;

    var inf = inferred(q);
    var data = {};
    PARAMS.forEach(function (p) { data[p] = q[p] || ''; });
    if (!data.utm_source) data.utm_source = inf.utm_source;
    if (!data.utm_medium) data.utm_medium = inf.utm_medium;

    var now = Date.now();
    rec = {
      at: new Date(now).toISOString(),
      exp: now + ATTR_MS,
      landing: String(location.pathname || ''),
      referrer: document.referrer || '',
      data: data
    };
    var raw = JSON.stringify(rec);
    lsSet(ATTR_KEY, raw);
    ssSet(ATTR_KEY, raw);
    return rec;
  }

  /* Current URL wins when it carries a value, otherwise the stored first touch. */
  function resolve(q, first) {
    var store = (first && first.data) || {};
    var out = {};
    PARAMS.forEach(function (p) { out[p] = q[p] || store[p] || ''; });
    return out;
  }

  function fillHidden(form, vals) {
    PARAMS.forEach(function (p) {
      var el = form.querySelector('input[type=hidden][name="' + p + '"]');
      if (!el) return;
      // offer ships with a build-time default; only a real URL value overrides it.
      if (p === 'offer') { if (vals.offer) el.value = vals.offer; return; }
      el.value = vals[p] || '';
    });
  }

  /* ---------------------------------------------------------------- payload */
  function val(form, name) {
    var el = form.elements ? form.elements[name] : null;
    if (!el || typeof el.value === 'undefined') return '';
    return String(el.value).trim();
  }

  /* Canonical OrthoBoost keys first (these are the ones the standard GHL workflow maps
     as {{inboundWebhookRequest.<key>}}), then this site's extras. Key names, including
     capitalisation and the space in "Full Name", must not be changed: GHL matches them
     literally. See build/GHL-WIRING.md. */
  function payload(form, vals, first) {
    var fn = val(form, 'first_name');
    var ln = val(form, 'last_name');
    var data = {
      'Full Name': (fn + ' ' + ln).trim(),
      'Email': val(form, 'email'),
      'Phone': val(form, 'phone'),
      'utm_source': vals.utm_source,
      'utm_medium': vals.utm_medium,
      'utm_campaign': vals.utm_campaign,
      'utm_content': vals.utm_content,
      'gclid': vals.gclid,
      'fbclid': vals.fbclid,
      'gbraid': vals.gbraid,
      'wbraid': vals.wbraid,
      'Offer': val(form, 'offer') || vals.offer || '',
      // extras, optional to map in GHL
      'first_name': fn,
      'last_name': ln,
      'utm_term': vals.utm_term,
      'interest': val(form, 'interest'),
      'message': val(form, 'message'),
      'page': val(form, 'page'),
      'form_id': form.getAttribute('id') || '',
      'page_url': String(location.href || ''),
      'referrer': document.referrer || '',
      'first_touch_at': (first && first.at) || '',
      'submitted_at': new Date().toISOString()
    };
    return data;
  }

  /* ---------------------------------------------------------------- messages */
  function msgEl(form) {
    var el = form.querySelector('.ob-msg');
    if (el) return el;
    el = document.createElement('p');
    el.className = 'ob-msg microline';
    el.setAttribute('role', 'status');
    el.setAttribute('aria-live', 'polite');
    el.style.cssText = 'margin:var(--sp-4) 0 0;';
    form.appendChild(el);
    return el;
  }

  function say(form, html) {
    var el = msgEl(form);
    el.innerHTML = html || '';
    el.style.display = html ? '' : 'none';
  }

  function telLink() {
    if (!PHONE) return '';
    return '<a class="tlink" href="tel:' + TEL + '">' + PHONE + '</a>';
  }

  /* ---------------------------------------------------------------- the event
     ob_generate_lead. No analytics vendor is wired on this site and none is added
     here: this dispatches a DOM event and pushes onto window.dataLayer if anything
     ever creates one. Creating the array loads nothing. No name, email or phone is
     put in the event detail. */
  function fireEvent(d) {
    var detail = {
      event: 'ob_generate_lead',
      form_id: d.form_id || '',
      page: d.page || '',
      interest: d.interest || '',
      utm_source: d.utm_source || '',
      utm_medium: d.utm_medium || '',
      utm_campaign: d.utm_campaign || '',
      offer: d.Offer || d.offer || ''
    };
    try {
      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push(detail);
    } catch (e) { /* ignore */ }
    try {
      document.dispatchEvent(new CustomEvent('ob_generate_lead', { detail: detail }));
    } catch (e) { /* ignore */ }
  }

  /* ---------------------------------------------------------------- queue */
  function readQueue() {
    var list = parse(lsGet(QUEUE_KEY));
    if (!(list instanceof Array)) return [];
    var now = Date.now();
    return list.filter(function (r) { return r && r.exp && r.exp > now; });
  }

  function writeQueue(list) {
    if (!list.length) { lsDel(QUEUE_KEY); return true; }
    if (list.length > QUEUE_MAX) list = list.slice(list.length - QUEUE_MAX);
    return lsSet(QUEUE_KEY, JSON.stringify(list));
  }

  function enqueue(data) {
    var now = Date.now();
    var list = readQueue();
    list.push({ queued_at: new Date(now).toISOString(), exp: now + QUEUE_MS, payload: data });
    return writeQueue(list);
  }

  // Exposed so the office or a developer can recover leads from the visitor's browser.
  window.obLeadQueue = function () { return readQueue(); };

  function post(data) {
    // GHL's webhook trigger only parses application/json. Its CORS headers allow this
    // request from the browser, so no proxy is needed.
    return fetch(ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
      keepalive: true
    }).then(function (res) {
      if (!res || !res.ok) throw new Error('HTTP ' + (res ? res.status : 'no response'));
      return res;
    });
  }

  /* Retry anything queued by an earlier failure. Quiet: the visitor is not told, and a
     failure just leaves the entry queued. A retry can create a duplicate contact if the
     original POST actually landed but its response was unreadable; GHL's create/update
     contact action collapses those by email and phone. */
  function flushQueue() {
    if (!ENDPOINT) return;
    var list = readQueue();
    if (!list.length) { writeQueue(list); return; }
    var kept = [];
    var pending = list.length;
    list.forEach(function (rec) {
      post(rec.payload).then(function () {
        pending -= 1;
        if (!pending) writeQueue(kept);
      }).catch(function () {
        kept.push(rec);
        pending -= 1;
        if (!pending) writeQueue(kept);
      });
    });
  }

  /* ---------------------------------------------------------------- submit */
  function onSuccess(data) {
    fireEvent(data);
    // Fire again on the confirmation page. The redirect below can cut a tag's own
    // request short, and the confirmation page is the conversion URL, so the flag is
    // replayed there. One-shot, so a direct visit to that URL fires nothing.
    ssSet(EVENT_KEY, JSON.stringify({
      form_id: data.form_id || '', page: data.page || '', interest: data.interest || '',
      utm_source: data.utm_source || '', utm_medium: data.utm_medium || '',
      utm_campaign: data.utm_campaign || '', offer: data.Offer || ''
    }));
    location.href = CONFIRM;
  }

  function onFailure(form, btn, label, data) {
    var saved = enqueue(data);
    if (btn) { btn.disabled = false; btn.innerHTML = label; }
    say(form, '<b>We could not send that just now.</b> Please call the practice on '
      + telLink() + ' and we will book you in straight away.'
      + (saved ? ' Your details are saved in this browser, so you can try again.' : ''));
  }

  function wire(form) {
    var btn = form.querySelector('button[type=submit]');
    form.addEventListener('submit', function (ev) {
      // Endpoint unset: the generators already disabled this form, so there is nothing
      // to intercept. Never fake a success here.
      if (!ENDPOINT) return;
      ev.preventDefault();

      var q = query();
      var first = firstTouch(q);
      var vals = resolve(q, first);
      fillHidden(form, vals);

      // The forms carry novalidate so one message can be shown in place, but the
      // required attributes are real and checkValidity still honours them.
      if (typeof form.checkValidity === 'function' && !form.checkValidity()) {
        var bad = form.querySelector(':invalid');
        if (bad && bad.focus) bad.focus();
        say(form, 'Please check the highlighted fields and try again.');
        return;
      }

      var data = payload(form, vals, first);
      var label = btn ? btn.innerHTML : '';
      say(form, '');
      if (btn) { btn.disabled = true; btn.textContent = 'Sending...'; }

      post(data)
        .then(function () { onSuccess(data); })
        .catch(function () { onFailure(form, btn, label, data); });
    });
  }

  /* ---------------------------------------------------------------- boot */
  function onConfirmPage() {
    var here = String(location.pathname || '').replace(/\.html$/, '').replace(/\/$/, '');
    var want = String(CONFIRM).replace(/\.html$/, '').replace(/\/$/, '');
    return here === want;
  }

  function start() {
    if (onConfirmPage()) {
      var raw = ssGet(EVENT_KEY);
      if (raw) {
        ssDel(EVENT_KEY);
        fireEvent(parse(raw) || {});
      }
    }

    // Record first touch on EVERY page that loads this script, not just pages with a
    // form: an ad can land on any page and the visitor converts on another one, by
    // which time the URL no longer carries the parameters.
    firstTouch(query());

    var forms = document.querySelectorAll('form[data-ob-lead]');
    Array.prototype.forEach.call(forms, function (form) {
      if (form.getAttribute('data-ob-lead') === '1') wire(form);
    });

    flushQueue();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start);
  else start();
})();
