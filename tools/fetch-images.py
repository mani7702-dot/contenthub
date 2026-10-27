#!/usr/bin/env python3
"""ContentHub - fetch a Wikimedia Commons cover image for an article.

Usage:
  python3 tools/fetch-images.py --slug <slug> --title "<title>" --query "kw1 kw2 kw3"
    [--out assets/images/<slug>.jpg]   (default: assets/images/<slug>.jpg)

Writes `image:` + `image_caption:` into the frontmatter of the article
(discovered by scanning content/ for a file whose basename matches the slug).
Stdlib + requests. Falls back gracefully: exit 0 with a note when nothing fits.
"""
import argparse, glob, io, json, os, re, sys
import requests
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://commons.wikimedia.org/w/api.php"
UA = {"User-Agent": "ContentHub/1.0 (image sourcing)"}
BAD_EXT = (".svg", ".tif", ".tiff", ".gif", ".webm", ".ogg", ".ogv", ".pdf", ".djvu")
OK_LICENSE = ("public domain", "cc0", "cc by")
MAXW = 1600


def article_path(slug):
    for f in glob.glob(os.path.join(ROOT, "content", "*", "*.md")):
        if os.path.basename(f)[:-3] == slug:
            return f
    return None


def api(params):
    r = requests.get(API, params=params, headers=UA, timeout=25)
    r.raise_for_status()
    return r.json()


def search_files(query, limit=8):
    d = api({"action": "query", "format": "json", "generator": "search",
             "gsrsearch": query, "gsrlimit": limit, "gsrnamespace": 6,
             "prop": "imageinfo", "iiprop": "url|extmetadata|size|mime",
             "iiurlwidth": MAXW})
    pages = (d.get("query") or {}).get("pages", {})
    out = []
    for pg in pages.values():
        ii = (pg.get("imageinfo") or [{}])[0]
        if not ii:
            continue
        ext = os.path.splitext(pg.get("title", ""))[1].lower()
        if ext in BAD_EXT:
            continue
        md = ii.get("extmetadata") or {}
        lic = (md.get("LicenseShortName") or {}).get("value", "").lower()
        if not any(k in lic for k in OK_LICENSE):
            continue
        out.append({"title": pg["title"], "url": ii.get("thumburl") or ii.get("url"),
                    "w": ii.get("thumbwidth") or ii.get("width"),
                    "h": ii.get("thumbheight") or ii.get("height"),
                    "lic": lic,
                    "artist": (md.get("Artist") or {}).get("value", "")})
    return out


def download(url):
    b = requests.get(url, headers=UA, timeout=40).content
    im = Image.open(io.BytesIO(b)).convert("RGB")
    if im.width < 500:
        return None
    if im.width > MAXW:
        im = im.resize((MAXW, round(im.height * MAXW / im.width)), Image.LANCZOS)
    return im


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--title", default="")
    ap.add_argument("--query", action="append", required=True)
    ap.add_argument("--out", default="")
    a = ap.parse_args()
    out = a.out or os.path.join(ROOT, "assets", "images", a.slug + ".jpg")
    path = article_path(a.slug)

    for q in a.query:
        try:
            cands = search_files(q)
        except Exception as e:
            print(f"[fetch-images] API error: {e}")
            continue
        for c in cands:
            try:
                im = download(c["url"])
            except Exception:
                continue
            if im is None:
                continue
            os.makedirs(os.path.dirname(out), exist_ok=True)
            im.save(out, "JPEG", quality=82, optimize=True, progressive=True)
            rel = os.path.relpath(out, ROOT).replace(os.sep, "/")
            artist = re.sub(r"<[^>]+>", "", c["artist"]).strip()[:80]
            cap = f"Photo: {artist} / {c['lic']} / Wikimedia Commons" if artist \
                else f"Photo: Wikimedia Commons"
            print(f"[fetch-images] OK {rel} ({c['w']}x{c['h']})")
            if path:
                txt = open(path, encoding="utf-8").read()
                txt = re.sub(r"^image:.*$", f"image: {rel}", txt, count=1, flags=re.M)
                txt = re.sub(r"^image_caption:.*$", f'image_caption: "{cap}"',
                             txt, count=1, flags=re.M)
                open(path, "w", encoding="utf-8").write(txt)
            return 0
    print("[fetch-images] NO usable image — publishing image-less is fine")
    return 0


if __name__ == "__main__":
    sys.exit(main())