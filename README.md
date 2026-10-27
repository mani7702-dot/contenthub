# ContentHub — Content Creation Website

A vibrant, fully-animated content site for **blog posts**, **news articles**, **facts**, and **lightweight browser games**. Designed so your **AI bots on a VPS** can continuously publish fresh content to it automatically.

## ✨ Features

- **Bright, animated design** — floating color blobs, a scrolling news ticker, card hover animations, fact-flip transitions.
- **Light / Dark mode** — auto-detects your system theme; manual toggle is remembered.
- **Four content sections** — Blog, News, Facts, and a Games hub.
- **Search + filters** on Blog and News; a flip-through fact deck.
- **4 lightweight games** — Tic-Tac-Toe, Memory Match, Reaction Click, Number Guess. All pure client-side JS (zero server load), easy to add more anytime.

## 📁 Files

```
contenthub/
├── index.html        Homepage (hero, ticker, previews)
├── blog.html         Blog listing + search + tag filters
├── news.html         News listing + search
├── facts.html        Flip-through fact deck
├── article.html      Full article reader (?type=&id=)
├── games.html        Games hub (all 4 games)
├── content.json      THE feed your bots write to
├── publish.php       API your bots POST new content to
├── assets/
│   ├── style.css     All styles (light/dark themes)
│   └── script.js     Theme, animations, feed loader
└── README.md
```

## 🚀 Deploy (5 minutes)

1. Upload the whole `contenthub/` folder to your web server (any PHP host, or any static host if you only post via bots).
2. Edit **`publish.php`** and change the secret key:
   ```php
   $SECRET_KEY = 'CHANGE_ME_to_a_long_random_secret';
   ```
   Pick a long random string (e.g. 40+ random characters).
3. Open `index.html` in a browser — the site shows sample content immediately.

## 🤖 Connecting your VPS AI bots

Your bots write content straight into `content.json` in two ways:

### Option A — HTTP API (recommended)

Bots call your server:

```bash
curl -X POST "https://YOUR-DOMAIN.com/contenthub/publish.php?key=YOUR_SECRET_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "blog",
    "title": "5 Ways to Boost Focus",
    "excerpt": "Quick, practical habits.",
    "body": "Full article text here…",
    "tag": "Lifestyle",
    "author": "Bot-01"
  }'
```

- `type` = `blog`, `news`, or `facts`
- **blog / news** need: `title`, `body` (optional: `excerpt`, `tag`, `author`, `read`)
- **facts** need: `fact` (optional: `category`, `tag`)
- Response: `{"ok":true,"id":"n1042","total":42}`
- New items are **prepended** (newest first). File is capped at 200 items per type.

### Option B — Direct file write

Your bot (SSH/script on the VPS) reads `content.json`, prepends new items to the matching array, and writes it back. The site will pick the change up on next page load.

> ⚠️ Keep the structure of `content.json` exactly as-is: three arrays named `blog`, `news`, `facts`, each item needs a unique `id`.

## 🎮 Adding a new game

Games are pure HTML/CSS/JS. To add one:
1. Add a new `<section class="game-box" id="g-mygame">` in `games.html`.
2. Add a matching `<button data-g="mygame">` in the `.game-nav`.
3. Write the game logic in the `<script>` block.
No backend changes needed — the page stays fast because games run entirely in the visitor's browser.

## 🎨 Theming

- **Light** and **dark** palettes are CSS variables at the top of `assets/style.css` (`:root` and `[data-theme="dark"]`).
- The site defaults to the visitor's **system** preference and remembers a manual override in the browser.

## 🔒 Security note

The `publish.php` endpoint accepts write access. Keep `$SECRET_KEY` secret and, if possible, allow-list the endpoint to your bot's IP via your host's firewall for extra safety.