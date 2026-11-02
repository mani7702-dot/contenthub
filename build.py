#!/usr/bin/env python3
"""ContentHub - static site builder (v2).

Generates the WHOLE site as real static HTML so search engines can crawl
every page without executing JavaScript:

    articles/<slug>.html    one page per article
    index.html              home (static cards, ticker, games)
    blog.html / news.html   static listings + client-side filter/paging
    categories.html         static topic sections
    facts.html              static fact rotator
    all-articles.html       full link index
    404.html                branded not-found page
    content.json            slim feed, used only by the global search overlay
    sitemap.xml feed.xml robots.txt .nojekyll CNAME

Publish flow: drop a .md into content/<board>/ -> python3 build.py -> push.
Stdlib only.
"""
import html as html_mod
import json
import os
import re
from datetime import datetime, timezone

import monetize

ROOT = os.path.dirname(os.path.abspath(__file__))
CONTENT_DIR = os.path.join(ROOT, "content")
ARTICLES_DIR = os.path.join(ROOT, "articles")
TEMPLATES_DIR = os.path.join(ROOT, "templates")
SITE_BASE = os.environ.get("SITE_BASE", "https://mani7702-dot.github.io/contenthub").rstrip("/")
SITE_CNAME = os.environ.get("SITE_CNAME", "")
# URL path the site is served under ("/contenthub" on GitHub Pages, "" on a
# custom domain). robots.txt Disallow rules are matched against the *domain*
# root, so they must carry this prefix or they silently match nothing.
SITE_PATH = "/" + SITE_BASE.split("//", 1)[-1].split("/", 1)[1] if "/" in SITE_BASE.split("//", 1)[-1] else ""
DEFAULT_OG = "assets/images/og-default.png"

BOARD_TITLE = {"news": "News", "blog": "Blog", "trending": "Trending"}
BOARD_CLASS = {"news": "tag-news", "blog": "tag-blog", "trending": "tag-fact"}

UMAMI = ('<script defer src="https://bots.tail35fa6b.ts.net/script.js" '
         'data-website-id="3b119c81-4072-4c80-8b9b-61b2dfc2219f"></script>')

NAV_ITEMS = [("index.html", "Home"), ("blog.html", "Blog"), ("news.html", "News"),
             ("facts.html", "Facts"), ("categories.html", "Explore"), ("games.html", "Games")]

GAMES = [
    ("Tic-Tac-Toe", "Classic three-in-a-row against a friend.", "⭕", "games.html#tictactoe"),
    ("Memory Match", "Flip cards and match the pairs.", "\U0001f9e0", "games.html#memory"),
    ("Reaction Click", "How fast can you click?", "⚡", "games.html#reaction"),
    ("Number Guess", "Guess the secret number fast.", "\U0001f3af", "games.html#guess"),
]


# ---------------------------------------------------------------- io helpers
def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def write(path, text):
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def esc(s):
    return html_mod.escape(s or "", quote=False)


def esca(s):
    return html_mod.escape(s or "", quote=True)


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")[:90]


# ------------------------------------------------------------ markdown render
def parse_frontmatter(text):
    """Tolerant key:value frontmatter; returns (meta dict, body markdown).

    Handles YAML block scalars (`excerpt: >-` followed by indented lines),
    which the older single-line parser read as the literal string ">-".
    """
    meta, body = {}, text
    m = re.match("^---\\s*\\n(.*?)\\n---\\s*\\n?(.*)$", text, re.S)
    if not m:
        return meta, body
    lines = m.group(1).split("\n")
    body = m.group(2)
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.startswith((" ", "\t", "-")) or ":" not in line:
            i += 1
            continue
        k, v = line.split(":", 1)
        k, v = k.strip(), v.strip()
        if v in (">", ">-", ">+", "|", "|-", "|+"):
            folded = v.startswith(">")
            block = []
            i += 1
            while i < len(lines) and (not lines[i].strip() or lines[i].startswith((" ", "\t"))):
                block.append(lines[i].strip())
                i += 1
            v = " ".join(x for x in block if x) if folded else "\n".join(block).strip()
        else:
            v = v.strip().strip('"').strip("'")
            i += 1
        meta[k] = v
    return meta, body


def inline(s):
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)",
               lambda m: monetize.link(m.group(2), m.group(1)), s)
    return s


def render_markdown(md):
    """Minimal markdown -> HTML for headings, paragraphs, bold, lists, quotes."""
    md = (md or "").replace("{{SITE_BASE}}", SITE_BASE)
    out, lines = [], md.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("### "):
            out.append("<h3>%s</h3>" % inline(line[4:].strip()))
        elif line.startswith("## "):
            out.append("<h2>%s</h2>" % inline(line[3:].strip()))
        elif line.startswith("# "):
            out.append("<h1>%s</h1>" % inline(line[2:].strip()))
        elif line.startswith("> "):
            out.append("<blockquote>%s</blockquote>" % inline(line[2:].strip()))
        elif line.strip().startswith("- "):
            items = []
            while i < len(lines) and lines[i].strip().startswith("- "):
                items.append("<li>%s</li>" % inline(lines[i].strip()[2:]))
                i += 1
            out.append("<ul>%s</ul>" % "".join(items))
            continue
        elif line.startswith("**") or line.strip():
            out.append("<p>%s</p>" % inline(line.strip()))
        i += 1
    return "\n".join(out)


def first_paragraph(body_md):
    """First real paragraph of a markdown body - used as an excerpt fallback."""
    for chunk in (body_md or "").split("\n"):
        c = chunk.strip()
        if not c or c.startswith(("#", "-", ">", "|", "*")):
            continue
        c = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", c)   # links -> text
        c = c.replace("**", "").replace("*", "").replace("`", "")
        c = re.sub(r"\s+", " ", c).strip()
        if len(c) > 20:
            return c
    return ""


# ------------------------------------------------------------------- collect
def collect():
    """Return article dicts, newest first, de-duplicated by id."""
    seen = {}
    order = []
    for board in sorted(os.listdir(CONTENT_DIR)):
        bdir = os.path.join(CONTENT_DIR, board)
        if not os.path.isdir(bdir):
            continue
        for fn in sorted(os.listdir(bdir)):
            if not fn.endswith(".md"):
                continue
            meta, body = parse_frontmatter(read(os.path.join(bdir, fn)))
            title = (meta.get("title") or fn[:-3]).strip()
            slug = (meta.get("slug") or slugify(title) or fn[:-3]).strip()
            if not slug:
                slug = fn[:-3]

            excerpt = (meta.get("excerpt") or "").strip()
            if not re.search(r"[A-Za-z]{3}", excerpt):
                excerpt = ""        # empty, or a leftover YAML marker like ">-"
            if not excerpt:
                excerpt = first_paragraph(body)
            if len(excerpt) > 220:
                excerpt = excerpt[:217].rsplit(" ", 1)[0] + "..."

            image = (meta.get("image") or "").strip().lstrip("/")
            if image and not os.path.exists(os.path.join(ROOT, image)):
                image = ""      # broken reference -> drop it entirely

            rec = {
                "id": slug,
                "board": board,
                "type": board,
                "title": title,
                "excerpt": excerpt,
                "body_md": body,
                "tag": meta.get("category") or meta.get("tag") or "General",
                "author": meta.get("author", ""),
                "date": meta.get("date", "2026-10-27"),
                "read": meta.get("read", "3 min"),
                "image": image,
                "image_caption": meta.get("image_caption", ""),
                "video": (meta.get("video") or "").strip(),
            }
            if slug in seen:
                continue        # first board wins (blog < news < trending)
            seen[slug] = rec
            order.append(slug)

    items = [seen[s] for s in order]
    items.sort(key=lambda a: (a["date"], a["id"]), reverse=True)
    return items


# ---------------------------------------------------------------- page chrome
def head_html(title, desc, canonical, ogimg="", ogtype="website", extra=""):
    img = ogimg or (SITE_BASE + "/" + DEFAULT_OG)
    return """<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>%s</title>
<meta name="description" content="%s">
<link rel="canonical" href="%s">
<meta property="og:type" content="%s">
<meta property="og:site_name" content="ContentHub">
<meta property="og:title" content="%s">
<meta property="og:description" content="%s">
<meta property="og:url" content="%s">
<meta property="og:image" content="%s">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="%s">
<meta name="twitter:description" content="%s">
<meta name="twitter:image" content="%s">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="%sassets/style.css">
%s
%s""" % (esc(title), esca(desc), esca(canonical), ogtype,
         esca(title), esca(desc), esca(canonical), esca(img),
         esca(title), esca(desc), esca(img),
         "" if ogtype == "article" else "", UMAMI, extra)


def nav_html(active):
    links = "".join(
        '      <a%s href="%s">%s</a>\n' % (' class="active"' if href == active else "", href, label)
        for href, label in NAV_ITEMS)
    return ('<header class="topbar">\n  <nav class="nav container">\n'
            '    <a class="logo" href="index.html"><span class="mark">◆</span><span>ContentHub</span></a>\n'
            '    <div class="nav-links">\n' + links +
            '    </div>\n'
            '    <button id="themeToggle" class="theme-btn" aria-label="Toggle theme">\U0001f319</button>\n'
            '  </nav>\n</header>')


def footer_html(full=False):
    if not full:
        return ('<footer>\n  <div class="container">\n'
                '    <p class="copy">© 2026 ContentHub · Your daily hub of ideas &amp; games.</p>\n'
                '    <p class="copy" style="margin-top:8px">'
                '<a href="about.html" style="margin-right:14px">About</a>'
                '<a href="privacy.html" style="margin-right:14px">Privacy</a>'
                '<a href="categories.html" style="margin-right:14px">Explore</a>'
                '<a href="mailto:andugulamani722@gmail.com">Contact</a></p>\n'
                '    <p style="color:var(--ink-soft);font-size:.85rem;margin-top:8px">'
                '<a href="all-articles.html">All Articles</a></p>\n'
                '  </div>\n</footer>')
    return """<footer>
  <div class="container">
    <div class="footer-grid">
      <div>
        <a class="logo" href="index.html"><span class="mark">◆</span><span>ContentHub</span></a>
        <p style="color:var(--ink-soft);margin-top:12px;max-width:320px">A living library of blog posts, news, facts, and games — fresh, vibrant, and always updating.</p>
      </div>
      <div>
        <h4>Explore</h4>
        <a href="blog.html">Blog</a>
        <a href="news.html">News</a>
        <a href="facts.html">Facts</a>
        <a href="categories.html">Categories</a>
      </div>
      <div>
        <h4>Play</h4>
        <a href="games.html#tictactoe">Tic-Tac-Toe</a>
        <a href="games.html#memory">Memory Match</a>
        <a href="games.html#reaction">Reaction Click</a>
      </div>
      <div>
        <h4>About</h4>
        <a href="about.html">About</a>
        <a href="privacy.html">Privacy</a>
        <a href="all-articles.html">All Articles</a>
      </div>
    </div>
    <p class="copy">© 2026 ContentHub · Built for creators, readers, and players.</p>
  </div>
</footer>"""


def page(title, desc, canonical, body, active="", ogimg="", ogtype="website", extra="", full_footer=False):
    return ('<!DOCTYPE html>\n<html lang="en">\n<head>\n'
            + head_html(title, desc, canonical, ogimg, ogtype, extra) +
            '\n</head>\n<body>\n\n' + nav_html(active) +
            '\n<!--CH-AD:top--><!--/CH-AD:top-->\n\n' + body +
            '\n\n' + footer_html(full_footer) +
            '\n\n<script src="assets/script.js"></script>\n</body>\n</html>\n')


# ----------------------------------------------------------------- card render
def clip(text, n=150):
    """Trim a card excerpt at a word boundary. Listing pages repeat this text
    once per card, so the full excerpt is pure page weight — the article page
    still carries the complete text."""
    text = (text or "").strip()
    if len(text) <= n:
        return text
    cut = text[:n].rsplit(" ", 1)[0].rstrip(" ,;:—-")
    return cut + "…"


def card_html(a, board=None):
    b = board or a["board"]
    cls = BOARD_CLASS.get(b, "tag-blog")
    media = ""
    if a.get("image"):
        media = '<img class="thumb" src="%s" alt="%s" loading="lazy">' % (
            esca(a["image"]), esca(a["title"]))
    elif a.get("video"):
        media = ('<video class="thumb-video" src="%s" muted loop autoplay playsinline></video>'
                 % esca(a["video"]))
    if b == "news":
        author = a.get("author") or "News Desk"
        meta = ('<span class="stat">\U0001f4f0 %s</span><span class="stat">%s</span>'
                '<span class="stat">%s read</span>' % (esc(author), esc(a["date"]), esc(a["read"])))
    else:
        author = a.get("author") or "ContentHub"
        meta = ('<span class="stat">✍️ %s</span><span class="stat">%s</span>'
                '<span class="stat">%s</span>' % (esc(author), esc(a["date"]), esc(a["read"])))
    return ('<article class="card" data-tag="%s">%s'
            '<span class="tag %s">%s</span>'
            '<h3><a href="articles/%s.html">%s</a></h3>'
            '<p class="excerpt">%s</p>'
            '<div class="meta">%s</div></article>') % (
        esca(a["tag"]), media, cls, esc(a["tag"]),
        esca(a["id"]), esc(a["title"]), esc(clip(a["excerpt"])), meta)


FILTER_JS = """<script>
(function(){
  var grid=document.getElementById('grid');
  if(!grid)return;
  // The search index is built from the rendered card text at runtime, so the
  // markup doesn't carry a duplicate copy of every title + excerpt.
  var cards=[].slice.call(grid.querySelectorAll('.card')).map(function(el){
    return {el:el, text:(el.textContent||'').toLowerCase()};
  });
  var empty=document.getElementById('empty');
  var pager=document.getElementById('pager');
  var PER=6,page=1,q='',tag='';
  function matches(c){
    var okTag=!tag||c.el.getAttribute('data-tag')===tag;
    var okQ=!q||c.text.indexOf(q)>-1;
    return okTag&&okQ;
  }
  function render(){
    var list=cards.filter(matches);
    cards.forEach(function(c){c.el.style.display='none';});
    var pages=Math.max(1,Math.ceil(list.length/PER));
    if(page>pages)page=pages;
    list.slice((page-1)*PER,page*PER).forEach(function(c){c.el.style.display='';});
    if(empty)empty.style.display=list.length?'none':'block';
    if(!pager)return;
    if(pages<=1){pager.innerHTML='';return;}
    var h='<button '+(page===1?'disabled':'')+' data-p="'+(page-1)+'">← Prev</button>';
    for(var i=1;i<=pages;i++)h+='<button class="'+(i===page?'on':'')+'" data-p="'+i+'">'+i+'</button>';
    h+='<button '+(page===pages?'disabled':'')+' data-p="'+(page+1)+'">Next →</button>';
    pager.innerHTML=h;
    [].forEach.call(pager.querySelectorAll('button[data-p]'),function(b){
      b.onclick=function(){page=parseInt(b.getAttribute('data-p'),10);render();window.scrollTo({top:0,behavior:'smooth'});};
    });
  }
  var si=document.getElementById('searchInput');
  if(si)si.addEventListener('input',function(){q=si.value.toLowerCase();page=1;render();});
  var chips=document.getElementById('chips');
  if(chips){
    [].forEach.call(chips.querySelectorAll('.chip'),function(c){
      c.onclick=function(){
        [].forEach.call(chips.querySelectorAll('.chip'),function(x){x.classList.remove('on');});
        c.classList.add('on');tag=c.getAttribute('data-tag')||'';page=1;render();
      };
    });
  }
  render();
})();
</script>"""


# --------------------------------------------------------------- listing pages
def render_index(items):
    blog = [a for a in items if a["board"] == "blog"][:3]
    news = [a for a in items if a["board"] == "news"][:3]
    trend = (news + blog)[:4]
    facts = [a for a in items if a["board"] == "trending"]

    ticker_items = []
    for a in items[:14]:
        ticker_items.append("<span><b>%s</b> %s</span>" % (a["board"].upper(), esc(a["title"])))
    ticker = "".join(ticker_items) * 2

    trend_html = "".join(
        '<a class="trend-item" href="articles/%s.html"><span class="rank">%d</span>'
        '<div style="flex:1"><h4>%s</h4><div class="trend-meta">%s</div></div>'
        '<span class="fire">\U0001f525</span></a>' % (esca(a["id"]), i + 1, esc(a["title"]), esc(a["tag"]))
        for i, a in enumerate(trend))

    games_html = "".join(
        '<a class="game-card" href="%s"><div class="g-ico">%s</div><h3>%s</h3><p>%s</p>'
        '<span class="btn btn-ghost">Play now</span></a>' % (u, i, esc(n), esc(d))
        for n, d, i, u in GAMES)

    fact = facts[0] if facts else None
    fact_head = "Honey never spoils."
    fact_body = ("Even after 3,000 years in an Egyptian tomb, honey remains perfectly edible. "
                 "A tiny daily fact to brighten your mind.")
    if fact:
        fact_head = re.split(r"(?<=\.)\s", fact["title"])[0] or fact["title"]
        fact_body = fact["excerpt"] or fact["title"]

    body = """<section class="hero">
  <div class="blobs"><div class="blob b1"></div><div class="blob b2"></div><div class="blob b3"></div></div>
  <div class="container">
    <h1>Create. Read. <span class="grad">Play.</span><br>Your daily hub of ideas &amp; games.</h1>
    <p>Blogs, breaking news, and surprising facts — plus quick, lightweight games for every mood. All in one colorful place.</p>
    <div class="hero-cta">
      <a class="btn btn-solid" href="blog.html">Read the latest ✨</a>
      <a class="btn btn-ghost" href="games.html">Play a game \U0001f3ae</a>
    </div>
  </div>
  <div class="ticker" id="ticker" aria-hidden="true">
    <div class="ticker-track" id="tickerTrack">%s</div>
  </div>
</section>

<main>
  <section class="section container">
    <div class="section-head reveal">
      <div>
        <span class="eyebrow">Our Writers</span>
        <h2>Latest Blog Posts</h2>
        <p>Long-form stories and practical guides from across the web.</p>
      </div>
      <a class="btn btn-ghost" href="blog.html">All posts →</a>
    </div>
    <div class="card-grid" id="blogGrid">%s</div>
  </section>

  <section class="section container">
    <div class="section-head reveal">
      <div>
        <span class="eyebrow">Around the Clock</span>
        <h2>Top News</h2>
        <p>The stories shaping today, gathered automatically as they publish.</p>
      </div>
      <a class="btn btn-ghost" href="news.html">All news →</a>
    </div>
    <div class="card-grid" id="newsGrid">%s</div>
  </section>

  <section class="section container">
    <div class="section-head reveal">
      <div>
        <span class="eyebrow">What's Hot</span>
        <h2>Trending Now \U0001f525</h2>
        <p>The stories readers are checking out the most right now.</p>
      </div>
    </div>
    <div class="trending-bar" id="trendGrid">%s</div>
  </section>

  <div class="container">
    <section class="feat-banner reveal">
      <div>
        <span class="eyebrow" style="color:#fff;opacity:.9">Did You Know?</span>
        <h2 id="factHead">%s</h2>
        <p id="factBody">%s</p>
        <a class="btn" href="facts.html">More surprising facts</a>
      </div>
      <div class="orb"></div><div class="orb o2"></div>
    </section>
  </div>

  <section class="section container">
    <div class="section-head reveal">
      <div>
        <span class="eyebrow">Light &amp; Fast</span>
        <h2>Play a Game</h2>
        <p>Quick, fun games that run right in your browser — no downloads, no lag.</p>
      </div>
      <a class="btn btn-ghost" href="games.html">Games hub →</a>
    </div>
    <div class="games-grid" id="gamePreview">%s</div>
  </section>
</main>""" % (ticker, "".join(card_html(a) for a in blog),
              "".join(card_html(a) for a in news), trend_html,
              esc(fact_head), esc(fact_body), games_html)

    return page("ContentHub — Create, Read, Play",
                "A living library of blog posts, news, facts, and games — fresh, vibrant, and always updating.",
                SITE_BASE + "/", body, active="index.html", full_footer=True)


def render_listing(items, board, title, h1, h1grad, blurb, desc, placeholder, chips=True):
    arts = [a for a in items if a["board"] == board]
    cards = "".join(card_html(a, board) for a in arts)

    chip_html = ""
    if chips:
        tags = []
        for a in arts:
            if a["tag"] not in tags:
                tags.append(a["tag"])
        chip_html = ('<div class="chips" id="chips" style="width:100%;justify-content:center">'
                     '<button class="chip on" data-tag="">All</button>'
                     + "".join('<button class="chip" data-tag="%s">%s</button>' % (esca(t), esc(t))
                               for t in tags)
                     + '</div>')

    body = """<section class="hero" style="padding:40px 0 20px">
  <div class="container">
    <h1>%s <span class="grad">%s</span></h1>
    <p>%s</p>
    <div class="search" style="max-width:760px;margin:26px auto 0">
      <input id="searchInput" type="text" placeholder="%s">
      %s
    </div>
  </div>
</section>

<main class="container">
  <div class="card-grid" id="grid">%s</div>
  <div class="pager" id="pager"></div>
  <p id="empty" style="display:none;text-align:center;color:var(--ink-soft);padding:40px">No stories match your search. Try another keyword.</p>
</main>

%s""" % (h1, h1grad, blurb, esca(placeholder), chip_html, cards, FILTER_JS)

    return page(title, desc, SITE_BASE + "/" + board + ".html", body, active=board + ".html")


def render_categories(items):
    groups = {}
    for a in items:
        if a["board"] == "trending":
            continue
        groups.setdefault(a["tag"], []).append(a)
    keys = sorted(groups)

    chips = ('<a href="#" class="on" data-cat="all">All Topics (%d)</a>' % sum(len(v) for v in groups.values())
             + "".join('<a href="#" data-cat="%s">%s (%d)</a>' % (esca(k), esc(k), len(groups[k]))
                       for k in keys))

    # Compact link lists, not cards: a category index repeats every article
    # once per tag, so full cards made this page ~850 KB. Plain links keep
    # every article crawlable at a fraction of the weight.
    blocks = []
    for k in keys:
        lis = "".join(
            '<li><a href="articles/%s.html">%s</a>'
            '<span class="cat-date">%s</span></li>'
            % (esca(a["id"]), esc(a["title"]), esc(a["date"]))
            for a in groups[k])
        blocks.append('<div class="cat-block" data-cat="%s" style="margin-bottom:38px">'
                      '<h2 style="font-size:1.3rem;margin-bottom:12px;display:flex;align-items:center;gap:10px">'
                      '<span class="tag tag-blog">%s</span> (%d stories)</h2>'
                      '<ul class="cat-list">%s</ul></div>'
                      % (esca(k), esc(k), len(groups[k]), lis))

    js = """<script>
(function(){
  var chips=document.getElementById('catFilterChips');
  var blocks=[].slice.call(document.querySelectorAll('.cat-block'));
  if(!chips)return;
  [].forEach.call(chips.querySelectorAll('a'),function(a){
    a.onclick=function(e){
      e.preventDefault();
      [].forEach.call(chips.querySelectorAll('a'),function(x){x.classList.remove('on');});
      a.classList.add('on');
      var cat=a.getAttribute('data-cat');
      blocks.forEach(function(b){b.style.display=(cat==='all'||b.getAttribute('data-cat')===cat)?'':'none';});
    };
  });
})();
</script>"""

    body = """<style>
.cat-list{list-style:none;margin:0;padding:0;columns:2;column-gap:34px}
.cat-list li{break-inside:avoid;display:flex;gap:10px;align-items:baseline;padding:7px 0;border-bottom:1px solid rgba(42,27,61,.07)}
.cat-list a{color:inherit;text-decoration:none;font-weight:600;font-size:.95rem;line-height:1.35}
.cat-list a:hover{color:#7C5CFF}
.cat-date{margin-left:auto;font-size:.78rem;color:#8b7ea3;white-space:nowrap}
@media(max-width:700px){.cat-list{columns:1}}
</style>

<section class="hero" style="padding:40px 0 10px">
  <div class="container">
    <h1>Explore by <span class="grad">Category</span></h1>
    <p>Browse all blog posts and news stories grouped automatically by topic tag.</p>
  </div>
</section>

<main class="container" style="padding:20px 0 60px">
  <div class="cat-row" id="catFilterChips">%s</div>
  <div id="catSections">%s</div>
</main>

%s""" % (chips, "".join(blocks), js)

    return page("Explore Topics — ContentHub",
                "Browse every ContentHub story grouped by topic: science, space, animals, history, technology and more.",
                SITE_BASE + "/categories.html", body, active="categories.html")


def render_facts(items):
    facts = [a for a in items if a["board"] == "trending"]
    data = [{"t": a["title"], "c": a["tag"], "u": "articles/%s.html" % a["id"]} for a in facts]
    first = data[0]["t"] if data else "Honey never spoils."

    js = """<script>
(function(){
  var facts=%s;
  if(!facts.length)return;
  var i=0,card=document.getElementById('factCard'),numEl=document.getElementById('factNum'),
      textEl=document.getElementById('factText'),dotsEl=document.getElementById('dots');
  facts.forEach(function(_,idx){
    var d=document.createElement('span');
    d.className='dotx'+(idx===0?' on':'');
    d.onclick=function(){show(idx);};
    dotsEl.appendChild(d);
  });
  var dots=dotsEl.children;
  function show(n){
    i=(n+facts.length)%%facts.length;
    card.classList.remove('swap');void card.offsetWidth;card.classList.add('swap');
    numEl.textContent='FACT '+String(i+1).padStart(2,'0');
    textEl.textContent=facts[i].t;
    for(var x=0;x<dots.length;x++)dots[x].className='dotx'+(x===i?' on':'');
  }
  document.getElementById('prevFact').onclick=function(){show(i-1);};
  document.getElementById('nextFact').onclick=function(){show(i+1);};
  show(0);
})();
</script>""" % json.dumps(data, ensure_ascii=False)

    extra = """<style>
  .fact-stage{max-width:640px;margin:0 auto;padding:20px 0 50px;text-align:center}
  .fact-card{
    background:var(--surface);border:1px solid var(--line);border-radius:24px;padding:44px 32px;
    box-shadow:var(--card-shadow);min-height:220px;display:flex;flex-direction:column;justify-content:center;gap:16px;
    position:relative;overflow:hidden
  }
  .fact-card::before{content:"";position:absolute;top:0;left:0;right:0;height:5px;background:var(--brand-grad)}
  .fact-card .num{font-size:.85rem;font-weight:800;letter-spacing:.08em;color:var(--violet)}
  .fact-card .text{font-size:clamp(1.25rem,3vw,1.7rem);font-weight:700;line-height:1.5}
  .fact-controls{display:flex;gap:14px;justify-content:center;margin-top:26px}
  .fact-controls .btn{padding:12px 20px}
  .fact-dots{display:flex;gap:8px;justify-content:center;margin-top:18px}
  .dotx{width:9px;height:9px;border-radius:50%;background:var(--line);transition:.3s}
  .dotx.on{background:var(--violet);transform:scale(1.3)}
  @keyframes flipIn{from{opacity:0;transform:translateY(26px) rotateX(45deg)}to{opacity:1;transform:translateY(0) rotateX(0)}}
  .fact-card.swap{animation:flipIn .5s ease both}
</style>"""

    body = """<section class="hero" style="padding:40px 0 10px">
  <div class="container">
    <h1>Mind-<span class="grad">Blowing</span> Facts</h1>
    <p>A fresh surprise every click. Flip through and amaze yourself.</p>
  </div>
</section>

<main class="fact-stage container">
  <div class="fact-card" id="factCard">
    <span class="num" id="factNum">FACT 01</span>
    <p class="text" id="factText">%s</p>
  </div>
  <div class="fact-dots" id="dots"></div>
  <div class="fact-controls">
    <button class="btn btn-ghost" id="prevFact">← Previous</button>
    <button class="btn btn-solid" id="nextFact">Next fact ✨</button>
  </div>
</main>

%s""" % (esc(first), js)

    return page("Facts — ContentHub",
                "Quick, surprising facts to brighten your day — a fresh one every click.",
                SITE_BASE + "/facts.html", body, active="facts.html", extra=extra)


def render_all_articles(items):
    groups = {}
    for a in items:
        groups.setdefault(a["board"], []).append(a)

    rows = []
    for board in ("blog", "news", "trending"):
        arts = groups.get(board)
        if not arts:
            continue
        rows.append('<section class="allarts-board"><h2>%s</h2><ul>' % esc(BOARD_TITLE[board]))
        for a in arts:
            rows.append('<li><a href="articles/%s.html">%s</a> '
                        '<span class="allarts-date">%s</span></li>'
                        % (esca(a["id"]), esc(a["title"]), esc(a["date"])))
        rows.append("</ul></section>")

    body = """<section class="hero" style="padding:44px 0 16px">
  <div class="container">
    <h1>All <span class="grad">Articles</span></h1>
    <p>Complete index of everything on ContentHub, newest first.</p>
  </div>
</section>
<main class="container" style="padding:8px 0 60px;max-width:820px">
%s
</main>""" % "\n".join(rows)

    extra = """<style>
  .allarts-board{margin:28px 0}
  .allarts-board h2{font-size:1.3rem;color:var(--ink);margin-bottom:12px}
  .allarts-board ul{list-style:none;padding:0}
  .allarts-board li{padding:8px 0;border-bottom:1px solid var(--line)}
  .allarts-board a{color:var(--ink);text-decoration:none;font-weight:600}
  .allarts-board a:hover{text-decoration:underline}
  .allarts-date{color:var(--ink-soft);font-size:.85rem;margin-left:8px}
</style>"""

    return page("All Articles — ContentHub",
                "Every article on ContentHub, listed: science, space, animals, history, technology and more.",
                SITE_BASE + "/all-articles.html", body, extra=extra)


def render_404():
    body = """<section class="hero" style="padding:70px 0 30px">
  <div class="container">
    <h1>404 — <span class="grad">Lost in the hub</span></h1>
    <p>That page has moved, been renamed, or never existed. Here's the way back.</p>
    <div class="hero-cta">
      <a class="btn btn-solid" href="index.html">Go home \U0001f3e0</a>
      <a class="btn btn-ghost" href="all-articles.html">Browse all articles</a>
    </div>
  </div>
</section>
<main class="container" style="padding:10px 0 60px;max-width:820px">
  <p style="color:var(--ink-soft)">Popular destinations:</p>
  <ul>
    <li><a href="blog.html">Blog</a> — explainers and how-things-work pieces</li>
    <li><a href="news.html">News</a> — fresh reports from around the world</li>
    <li><a href="facts.html">Facts</a> — quick, surprising things to know</li>
    <li><a href="categories.html">Categories</a> — browse by topic</li>
    <li><a href="games.html">Games</a> — free in-browser games</li>
  </ul>
</main>"""
    return page("Page not found — ContentHub",
                "The page you were looking for could not be found on ContentHub.",
                SITE_BASE + "/404.html", body)


# ------------------------------------------------------------- article pages
def render_article_html(a):
    tpl_path = os.path.join(TEMPLATES_DIR, "article.html")
    if not os.path.exists(tpl_path):
        tpl_path = os.path.join(ROOT, "article.html")
    tpl = read(tpl_path)

    body = render_markdown(a["body_md"])

    head = ""
    if a.get("image"):
        head += ('<img class="article-cover" src="../%s" alt="%s">'
                 % (esca(a["image"]), esca(a["title"])))
    if a.get("video"):
        head += ('<video class="article-cover" src="%s" controls muted loop></video>'
                 % esca(a["video"]))

    meta_html = ('<span>%s</span><span>%s</span><span>%s</span>'
                 % (esc(a.get("author") or "ContentHub"), esc(a["date"]), esc(a["read"])))

    desc = a.get("excerpt") or (a["title"] + " — read it on ContentHub.")
    canonical = SITE_BASE + "/articles/" + a["id"] + ".html"
    ogimg = (SITE_BASE + "/" + a["image"]) if a.get("image") else (SITE_BASE + "/" + DEFAULT_OG)

    page_html = tpl
    page_html = page_html.replace("<!--CONTENTHUB-TITLE-->", esc(a["title"]))
    page_html = page_html.replace("<!--CONTENTHUB-META-->", meta_html)
    page_html = page_html.replace("<!--CONTENTHUB-TAG-->", esc(a["tag"]))
    page_html = page_html.replace("<!--CONTENTHUB-EXCERPT-->", "")
    page_html = page_html.replace("<!--CONTENTHUB-HEAD-->", head)
    page_html = page_html.replace("<!--CONTENTHUB-BODY-->", monetize.insert_mid(body))
    page_html = page_html.replace("<!--CONTENTHUB-DESC-->", esca(desc[:300]))
    page_html = page_html.replace("<!--CONTENTHUB-CANONICAL-->", esca(canonical))
    page_html = page_html.replace("<!--CONTENTHUB-OGIMAGE-->", esca(ogimg))
    page_html = page_html.replace('<meta name="robots" content="noindex,follow">\n', "")
    return monetize.inject(page_html)


# --------------------------------------------------------------------- build
def build():
    items = collect()
    os.makedirs(ARTICLES_DIR, exist_ok=True)

    # 1. Article pages
    expected = set()
    for a in items:
        expected.add(a["id"] + ".html")
        write(os.path.join(ARTICLES_DIR, a["id"] + ".html"), render_article_html(a))

    # 1b. Delete orphaned article pages left over from older builds
    removed = []
    for fn in sorted(os.listdir(ARTICLES_DIR)):
        if fn.endswith(".html") and fn not in expected:
            os.remove(os.path.join(ARTICLES_DIR, fn))
            removed.append(fn)

    # 2. Static listing pages
    write(os.path.join(ROOT, "index.html"), monetize.inject(render_index(items)))
    write(os.path.join(ROOT, "blog.html"), monetize.inject(render_listing(
        items, "blog", "Blog — ContentHub", "Blog", "Posts",
        "Stories, guides, and ideas from across the web — written and published around the clock.",
        "Stories, guides, and ideas from across the web.", "Search posts…")))
    write(os.path.join(ROOT, "news.html"), monetize.inject(render_listing(
        items, "news", "News — ContentHub", "News", "Wire",
        "The latest headlines collected automatically from across the web — accurate and always fresh.",
        "The stories shaping today, gathered as they publish.", "Search the news…", chips=False)))
    write(os.path.join(ROOT, "categories.html"), monetize.inject(render_categories(items)))
    write(os.path.join(ROOT, "facts.html"), monetize.inject(render_facts(items)))
    write(os.path.join(ROOT, "all-articles.html"), monetize.inject(render_all_articles(items)))
    write(os.path.join(ROOT, "404.html"), monetize.inject(render_404()))

    # 3. Slim feed - only the global search overlay reads this now
    feed = {"updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "blog": [], "news": [], "facts": []}
    for a in items:
        row = {"id": a["id"], "title": a["title"], "excerpt": a["excerpt"],
               "tag": a["tag"], "date": a["date"]}
        if a["board"] == "blog":
            feed["blog"].append(row)
        elif a["board"] == "news":
            feed["news"].append(row)
        elif a["board"] == "trending":
            feed["facts"].append({"id": a["id"], "fact": a["title"], "category": a["tag"]})
    write(os.path.join(ROOT, "content.json"), json.dumps(feed, ensure_ascii=False))

    # 4. sitemap.xml
    static_pages = ["", "blog.html", "news.html", "facts.html", "categories.html",
                    "all-articles.html", "games.html", "about.html", "privacy.html"]
    urls = [(SITE_BASE + "/" + p, "") for p in static_pages]
    urls += [(SITE_BASE + "/articles/" + a["id"] + ".html", a["date"]) for a in items]
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>',
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, lastmod in urls:
        sitemap.append("  <url><loc>%s</loc>%s</url>"
                       % (esc(loc), ("<lastmod>%s</lastmod>" % lastmod) if lastmod else ""))
    sitemap.append("</urlset>")
    write(os.path.join(ROOT, "sitemap.xml"), "\n".join(sitemap) + "\n")

    # 5. feed.xml
    rss_items = []
    for a in items[:25]:
        rss_items.append(
            "  <item>\n    <title>%s</title>\n    <link>%s/articles/%s.html</link>\n"
            "    <guid>%s/articles/%s.html</guid>\n    <pubDate>%s</pubDate>\n"
            "    <description>%s</description>\n  </item>\n"
            % (esc(a["title"]), SITE_BASE, a["id"], SITE_BASE, a["id"],
               esc(a["date"]), esc(a["excerpt"])))
    write(os.path.join(ROOT, "feed.xml"),
          '<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0">\n<channel>\n'
          '<title>ContentHub</title>\n<link>%s/</link>\n'
          '<description>Blog posts, news, facts and games.</description>\n'
          '%s</channel>\n</rss>\n' % (SITE_BASE, "".join(rss_items)))

    # 6. robots.txt + .nojekyll + CNAME
    write(os.path.join(ROOT, "robots.txt"),
          "User-agent: *\nAllow: /\n"
          + "".join("Disallow: %s/%s/\n" % (SITE_PATH, d)
                    for d in ("content", "templates", "tools", "scripts", "logs"))
          + "\nSitemap: %s/sitemap.xml\n" % SITE_BASE)
    write(os.path.join(ROOT, ".nojekyll"), "")
    if SITE_CNAME:
        write(os.path.join(ROOT, "CNAME"), SITE_CNAME + "\n")

    # 7. Re-inject monetization into the hand-maintained static pages
    for name in ("games.html", "about.html", "privacy.html"):
        p = os.path.join(ROOT, name)
        if os.path.exists(p):
            write(p, monetize.inject(read(p)))

    print("Built %d articles (%d orphan pages removed)" % (len(items), len(removed)))
    print("Static pages: index, blog, news, categories, facts, all-articles, 404")
    print("Monetization: AdSense %s" % (
        "ON (%s)" % monetize.ADSENSE_CLIENT if monetize.adsense_enabled()
        else "off (set ADSENSE_CLIENT to enable)"))


if __name__ == "__main__":
    build()
