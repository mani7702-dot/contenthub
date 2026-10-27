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
SITE_BASE = os.environ.get("SITE_BASE", "")
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
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.S)
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