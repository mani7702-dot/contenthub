#!/usr/bin/env python3
"""ContentHub — static site builder.

Reads content/<board>/*.md, renders each article as a static HTML page under
articles/, and regenerates content.json, sitemap.xml and feed.xml so the
client-side pages (home, blog, news, categories, article) are SEO-friendly.

Publish flow: drop a .md into content/<board>/ -> run `python build.py` -> push.
Stdlib only.
"""
import html as html_mod
import json
import os
import re
from datetime import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
CONTENT_DIR = os.path.join(ROOT, "content")
ARTICLES_DIR = os.path.join(ROOT, "articles")
SITE_BASE = os.environ.get("SITE_BASE", "https://mani7702-dot.github.io/contenthub").rstrip("/")
SITE_CNAME = os.environ.get("SITE_CNAME", "")

BOARD_TITLE = {"news": "News", "blog": "Blog", "trending": "Trending"}
BOARD_CLASS = {"news": "tag-news", "blog": "tag-blog", "trending": "tag-fact"}


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def parse_frontmatter(text):
    """Tolerant key:value frontmatter; returns (meta dict, body markdown)."""
    meta, body = {}, text
    # Fix (confirmed 2026-10-28, contenthub-publishing-bugs skill):
    # In a raw string r"...", \\n is two chars (backslash + n), which regex
    # interprets as "literal backslash followed by n" — NOT a newline.
    # This breaks ALL frontmatter parsing. The fix is to use \n (single backslash)
    # so regex matches an actual newline character.
    # Using a non-raw string to make the newline explicit and unambiguous.
    m = re.match("^---\\s*\\n(.*?)\\n---\\s*\\n?(.*)$", text, re.S)
    if m:
        for line in m.group(1).split("\n"):
            if ":" in line and not line.startswith((" ", "-")):
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip().strip('"')
        body = m.group(2)
    return meta, body


def esc(s):
    return html_mod.escape(s or "", quote=False)


def inline(s):
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", s)
    return s


def render_markdown(md):
    """Minimal markdown -> HTML for headings, paragraphs, bold, lists, quotes."""
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


def collect():
    """Return list of article dicts sorted newest-first."""
    items = []
    for board in os.listdir(CONTENT_DIR):
        bdir = os.path.join(CONTENT_DIR, board)
        if not os.path.isdir(bdir):
            continue
        for fn in os.listdir(bdir):
            if not fn.endswith(".md"):
                continue
            meta, body = parse_frontmatter(read(os.path.join(bdir, fn)))
            title = meta.get("title", fn[:-3]).strip()
            slug = meta.get("slug") or re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:90]
            if not slug:
                slug = fn[:-3]
            items.append({
                "id": slug,
                "board": board,
                "type": board,
                "title": title,
                "excerpt": meta.get("excerpt", ""),
                "body_md": body,
                "tag": meta.get("category", "General"),
                "author": meta.get("author", ""),
                "date": meta.get("date", "2026-10-27"),
                "read": meta.get("read", "3 min"),
                "image": meta.get("image", ""),
                "image_caption": meta.get("image_caption", ""),
                "video": meta.get("video", ""),
            })
    items.sort(key=lambda a: a["date"], reverse=True)
    return items


def render_article_html(a):
    """Render a single article page from the article.html shell."""
    tpl = read(os.path.join(ROOT, "article.html"))
    body = render_markdown(a["body_md"])
    head = ""
    if a.get("image"):
        head += '<img class="article-cover" src="../' + a["image"] + '" alt="' + esc(a["title"]) + '">'
    if a.get("video"):
        head += '<video class="article-cover" src="' + a["video"] + '" controls muted loop></video>'
    excerpt_p = '<p>' + esc(a.get("excerpt", "")) + '</p>' if a.get("excerpt") else ""
    meta_html = '<span>' + esc(a.get("author", "ContentHub")) + '</span><span>' + a.get("date", "") + '</span><span>' + a.get("read", "3 min") + '</span>'
    page = tpl
    page = page.replace("<!--CONTENTHUB-TITLE-->", esc(a["title"]))
    page = page.replace("<!--CONTENTHUB-META-->", meta_html)
    page = page.replace("<!--CONTENTHUB-TAG-->", esc(a.get("tag", "General")))
    page = page.replace("<!--CONTENTHUB-EXCERPT-->", excerpt_p)
    page = page.replace("<!--CONTENTHUB-HEAD-->", head)
    page = page.replace("<!--CONTENTHUB-BODY-->", body)
    return page




def render_all_articles_page(items):
    """Static HTML hub listing every article as a plain <a> link (crawl path for search engines)."""
    from collections import OrderedDict
    boards = OrderedDict()
    for a in items:
        boards.setdefault(a["board"], []).append(a)

    rows = []
    for board, arts in boards.items():
        rows.append('<section class="allarts-board"><h2>' + esc(board.title()) + '</h2><ul>')
        for a in arts:
            rows.append('<li><a href="articles/' + a["id"] + '.html">' + esc(a["title"]) + '</a> <span class="allarts-date">' + esc(a["date"]) + '</span></li>')
        rows.append('</ul></section>')

    nav = '''<header class="topbar">
  <nav class="nav container">
    <a class="logo" href="index.html"><span class="mark">◆</span><span>ContentHub</span></a>
    <div class="nav-links">
      <a href="index.html">Home</a>
      <a href="blog.html">Blog</a>
      <a href="news.html">News</a>
      <a href="facts.html">Facts</a>
      <a href="games.html">Games</a>
    </div>
    <button id="themeToggle" class="theme-btn" aria-label="Toggle theme">🌙</button>
  </nav>
</header>'''

    footer = '''<footer>
  <div class="container">
    <p class="copy">© 2026 ContentHub · Built for creators, readers, and players.</p>
  </div>
</footer>'''

    theme_js = '''<script>window.addEventListener("DOMContentLoaded",()=>{const t=document.getElementById("themeToggle"),s=localStorage.getItem("ch_theme");document.documentElement.dataset.theme=s||(matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light");t.textContent=document.documentElement.dataset.theme==="dark"?"☀️":"🌙";t.onclick=()=>{const d=document.documentElement.dataset.theme==="dark"?"light":"dark";document.documentElement.dataset.theme=d;localStorage.setItem("ch_theme",d);t.textContent=d==="dark"?"☀️":"🌙";};});</script>'''

    return '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>All Articles — ContentHub</title>
<meta name="description" content="Every article on ContentHub, listed: science, space, animals, history, technology and more.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css">
<style>
  .allarts-board{margin:28px 0}
  .allarts-board h2{font-size:1.3rem;color:var(--ink);margin-bottom:12px}
  .allarts-board ul{list-style:none;padding:0}
  .allarts-board li{padding:8px 0;border-bottom:1px solid var(--line)}
  .allarts-board a{color:var(--ink);text-decoration:none;font-weight:600}
  .allarts-board a:hover{text-decoration:underline}
  .allarts-date{color:var(--ink-soft);font-size:.85rem;margin-left:8px}
</style>
</head>
<body>
''' + nav + '''
<section class="hero" style="padding:44px 0 16px">
  <div class="container">
    <h1>All <span class="grad">Articles</span></h1>
    <p>Complete index of everything on ContentHub, newest first.</p>
  </div>
</section>
<main class="container" style="padding:8px 0 60px;max-width:820px">
''' + "\n".join(rows) + '''
</main>
''' + footer + '''
<script src="assets/script.js"></script>
''' + theme_js + '''
</body>
</html>'''

def build():
    items = collect()
    os.makedirs(ARTICLES_DIR, exist_ok=True)

    # 1. Static article pages (SEO)
    for a in items:
        write(os.path.join(ARTICLES_DIR, a["id"] + ".html"), render_article_html(a))

    # 2. content.json feed (client-side)
    feed = {"updated": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"), "boards": {}}
    for b in BOARD_TITLE:
        feed["boards"][b] = [{
            "id": a["id"], "title": a["title"], "excerpt": a["excerpt"],
            "tag": a["tag"], "author": a["author"], "date": a["date"],
            "read": a["read"], "image": a["image"], "video": a.get("video", ""),
            "url": SITE_BASE + "/articles/" + a["id"] + ".html",
        } for a in items if a["board"] == b]
    # Flat lists for the existing pages
    feed["blog"] = feed["boards"]["blog"]
    feed["news"] = feed["boards"]["news"]
    feed["facts"] = [{"id": a["id"], "fact": a["title"], "category": a["tag"],
                      "title": a["title"]} for a in items if a["board"] == "trending"]
    write(os.path.join(ROOT, "content.json"), json.dumps(feed, indent=2))

    # 3. sitemap.xml
    urls = [SITE_BASE + "/"]
    for a in items:
        urls.append(SITE_BASE + "/articles/" + a["id"] + ".html")
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in urls:
        sitemap += '  <url><loc>%s</loc></url>\n' % u
    sitemap += '</urlset>\n'
    write(os.path.join(ROOT, "sitemap.xml"), sitemap)

    # 4. feed.xml (RSS-ish)
    feed_items = []
    for a in items[:20]:
        feed_items.append(
            '  <item>\n'
            '    <title>%s</title>\n'
            '    <link>%s/articles/%s.html</link>\n'
            '    <guid>%s/articles/%s.html</guid>\n'
            '    <description>%s</description>\n'
            '  </item>\n' % (esc(a["title"]), SITE_BASE, a["id"], SITE_BASE, a["id"], esc(a.get("excerpt", ""))))
    rss = ('<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0">\n<channel>\n'
           '<title>ContentHub</title>\n<link>%s/</link>\n%s</channel>\n</rss>\n' % (SITE_BASE, "".join(feed_items)))
    write(os.path.join(ROOT, "feed.xml"), rss)

    # 4b. Static all-articles link hub (crawl path)
    write(os.path.join(ROOT, "all-articles.html"), render_all_articles_page(items))
    # 5. CNAME for custom domain
    if SITE_CNAME:
        write(os.path.join(ROOT, "CNAME"), SITE_CNAME)

    # 6. robots.txt
    write(os.path.join(ROOT, "robots.txt"),
          "User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n" % SITE_BASE if SITE_BASE else
          "User-agent: *\nAllow: /\n")

    print("Built %d articles -> articles/, content.json, sitemap.xml, feed.xml" % len(items))


if __name__ == "__main__":
    build()