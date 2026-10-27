# ContentHub — Deploy & Traffic Guide

ContentHub is a plain static site: HTML + CSS + JS + generated `articles/` pages and
`content/` markdown boards. Free to host, no database, no 24/7 server needed. This mirrors the
proven Our World setup but runs **entirely on GitHub Pages** with your bots on the VPS pushing
content via git — so no VPS is needed to serve traffic.

---

## 1. Push to GitHub

From this `contenthub/` folder (Windows + git-bash assumed):

```bash
gh repo create contenthub --public --source=. --push
# or by hand:
git remote add origin https://github.com/<your-username>/contenthub.git
git push -u origin main
```

Your EU.org domain later: I'll point it at GitHub Pages.

---

## 2. Host on GitHub Pages (primary)

1. Repo → **Settings** → **Pages**.
2. **Source:** Deploy from a branch → **Branch:** `main`, **Folder:** `/(root)` → **Save**.
3. After ~1 minute the site is live at `https://<your-username>.github.io/contenthub/`.

> The site is already built (all `*.html`, `articles/`, `content.json`, `sitemap.xml`,
> `feed.xml` are committed). GitHub Pages serves them as-is. No build step needed on GitHub.

---

## 3. Add your EU.org custom domain

When you register a new free domain at **nic.eu.org** (e.g. `<name>.eu.org`):

1. In EU.org control panel, set **nameservers** to a DNS provider you control (Cloudflare free is
   easiest and adds HTTPS + speed).
2. In that DNS provider, create these records pointing at GitHub Pages:
   - `A` → `185.199.108.153`
   - `A` → `185.199.109.153`
   - `A` → `185.199.110.153`
   - `A` → `185.199.111.153`
   - `CNAME` `www` → `<your-username>.github.io`
3. On GitHub: Repo → **Settings** → **Pages** → **Custom domain** → enter `<name>.eu.org` → **Save**.
   This writes the `CNAME` file for you (build.py also writes one when you pass `SITE_CNAME`).
4. Tick **Enforce HTTPS** once DNS resolves (takes a few minutes).

### Rebuild so all SEO URLs use the domain

```bash
SITE_BASE="https://<name>.eu.org" SITE_CNAME="<name>.eu.org" python3 build.py
```

That regenerates canonical URLs, `sitemap.xml`, `feed.xml`, `robots.txt`, and writes `CNAME`.
Then commit + push.

---

## 4. The daily publish loop (bots on your VPS)

Every change — a post, a board, a design — follows the same loop. Your VPS agents run this:

```bash
# 1. drop a markdown file into content/<board>/
# 2. rebuild
python3 build.py
# 3. commit and push
git add -A
git commit -m "publish <board>: <title>"
git push origin main
```

GitHub Pages redeploys within ~1 minute. **Never push without running `build.py` first.**
Content source: drop into `content/news/`, `content/blog/`, or `content/trending/`.
Optional `video:` field in a post's frontmatter adds a hero video on the article + home board.

Bots fetch from free first-party feeds (NASA, BBC, ScienceDaily, Smithsonian, NPR, Reddit TIL)
— the exact pattern from the old `fetch-news.py` / `tools/ow-deploy.sh`. Reuse those scripts,
pointing them at this repo.

---

## 5. Grow traffic (recommendations)

- **SEO**: `sitemap.xml` + `robots.txt` are auto-generated. Submit the sitemap in **Google
  Search Console** and **Bing Webmaster Tools** once the domain is livewing; verify ownership.
- **Open Graph / social cards**: each article is its own HTML page with a hero image — set the
  `og:` meta tags so shares show a rich preview (add to `article.html` if not already).
- **Media = engagement**: articles + home board show images/videos (from open sources or Hermes
  AI media). Looping hero video on the home board boosts time-on-page.
- **Repeat visits**: games save best scores / play counts in the browser; the games page shows a
  "Welcome back" bar. That pulls visitors back and lifts your per-hour visit metrics.
- **Feeds**: `feed.xml` lets RSS readers and aggregators pick up every new post automatically.
- **Share buttons**: every article has Post-to-X, WhatsApp, and Copy-link — word-of-mouth growth.
- **Freshness**: your bots publishing several boards daily keeps the site "new" for search
  engines and returning readers — the biggest traffic lever.

---

## 6. Verify after each deploy

- Open the live URL.
- Check one article page (image + reading), one game (plays + progress persists), the dark-mode
  toggle, and the search (Ctrl+K).
- Browser console (F12): expect zero errors.

## Rollback

GitHub Pages keeps commit history. To revert, `git revert` the bad commit and push — Pages
rebuilds from `main` automatically.

---

## Note on your old project

The previous `ourworld.eu.org` was a placeholder created by an agent — it was not registered.
ContentHub uses a **new** EU.org name you register. All SEO/domain strings are controlled by the
`SITE_BASE` / `SITE_CNAME` env vars in `build.py`, so the domain can change anytime with a
one-line rebuild.