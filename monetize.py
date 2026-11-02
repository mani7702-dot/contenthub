"""ContentHub monetization layer.

Turns the site into an ad + affiliate machine without touching content.
Everything is driven by environment variables, so the site builds *exactly
as it does today* when nothing is configured — and switches on the moment
the AdSense publisher ID exists.

Env vars (all optional):
  ADSENSE_CLIENT       AdSense publisher id, e.g. ca-pub-1234567890123456
  ADSENSE_SLOT_TOP     numeric ad-slot id for the unit above the article
  ADSENSE_SLOT_MID     numeric ad-slot id for the in-article unit
  ADSENSE_SLOT_BOTTOM  numeric ad-slot id for the unit after the article
  AFFILIATE_DOMAINS    comma-separated domains whose links get rel="sponsored nofollow"

Markers injected into pages (idempotent — safe to rebuild any number of times):
  <!--CH-AD:head-->    -> AdSense loader <script> (goes in <head>)
  <!--CH-AD:top-->     -> display unit above the article body
  <!--CH-AD:bottom-->  -> display unit after the article body

Stdlib only.
"""
import os
import re

ADSENSE_CLIENT = os.environ.get("ADSENSE_CLIENT", "").strip()
SLOTS = {
    "top": os.environ.get("ADSENSE_SLOT_TOP", "").strip(),
    "mid": os.environ.get("ADSENSE_SLOT_MID", "").strip(),
    "bottom": os.environ.get("ADSENSE_SLOT_BOTTOM", "").strip(),
}
AFFILIATE_DOMAINS = [d.strip().lower() for d in
                     os.environ.get("AFFILIATE_DOMAINS", "").split(",") if d.strip()]

AD_LABEL = "Advertisement"


def adsense_enabled():
    return bool(ADSENSE_CLIENT)


def head_script():
    """The AdSense loader. Empty until a publisher id is configured."""
    if not ADSENSE_CLIENT:
        return ""
    return ('<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js'
            '?client=%s" crossorigin="anonymous"></script>' % ADSENSE_CLIENT)


def ad_unit(slot, label=AD_LABEL):
    """One responsive display unit. Empty until client + slot are configured."""
    if not ADSENSE_CLIENT or not slot:
        return ""
    return ('<div class="ch-ad" role="complementary" aria-label="%s">'
            '<ins class="adsbygoogle" style="display:block" data-ad-client="%s" '
            'data-ad-slot="%s" data-ad-format="auto" data-full-width-responsive="true"></ins>'
            '</div><script>(adsbygoogle=window.adsbygoogle||[]).push({});</script>'
            ) % (label, ADSENSE_CLIENT, slot)


_FILLERS = {
    "head": head_script,
    "top": lambda: ad_unit(SLOTS["top"]),
    "bottom": lambda: ad_unit(SLOTS["bottom"]),
}


def ensure_markers(html):
    """Seed the ad markers into a page that doesn't have them yet."""
    if "</head>" in html and "CH-AD:head" not in html:
        html = html.replace("</head>", "<!--CH-AD:head-->\n</head>", 1)
    if "</header>" in html and "CH-AD:top" not in html:
        html = html.replace("</header>", "</header>\n<!--CH-AD:top-->", 1)
    return html


def inject(html):
    """Replace every <!--CH-AD:x--> marker (and its paired block) with live code.

    Idempotent: a marker becomes <!--CH-AD:x-->...<!--/CH-AD:x--> and is
    replaced wholesale on the next run, so rebuilds never stack duplicates.
    """
    html = ensure_markers(html)
    for name, fn in _FILLERS.items():
        start, end = "<!--CH-AD:%s-->" % name, "<!--/CH-AD:%s-->" % name
        block = start + fn() + end
        pat = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
        if pat.search(html):
            html = pat.sub(lambda m: block, html)
        elif start in html:
            html = html.replace(start, block)
    return html


def insert_mid(body_html):
    """Drop an in-article ad unit roughly halfway through the rendered body."""
    unit = ad_unit(SLOTS["mid"])
    if not unit:
        return body_html
    parts = body_html.split("</p>")
    if len(parts) < 5:
        return body_html
    mid = len(parts) // 2
    return "</p>".join(parts[:mid]) + "</p>" + unit + "</p>".join(parts[mid:])


def is_affiliate(url):
    u = (url or "").lower()
    return any(d in u for d in AFFILIATE_DOMAINS)


def link(url, text):
    """Render an <a> with the right rel/target for internal vs affiliate links."""
    if is_affiliate(url):
        return '<a href="%s" rel="sponsored nofollow noopener" target="_blank">%s</a>' % (url, text)
    if url.startswith("http"):
        return '<a href="%s" rel="noopener" target="_blank">%s</a>' % (url, text)
    return '<a href="%s">%s</a>' % (url, text)
