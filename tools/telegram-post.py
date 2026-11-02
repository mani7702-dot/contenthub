#!/usr/bin/env python3
"""Post ContentHub articles to Telegram (channel or DM).

Usage:
  python3 tools/telegram-post.py --count 3                 # post next 3 unposted
  python3 tools/telegram-post.py --count 3 --chat -100123  # to a channel
  python3 tools/telegram-post.py --dry-run                 # show what would post
  python3 tools/telegram-post.py --status                  # how many posted / left

State: logs/telegram-posted.json (article ids already sent).
Token: read from /home/ubuntu/.hermes/config.yaml (telegram.bot_token) — never hardcoded.
"""
import argparse, json, os, sys, time, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.environ.get("SITE_BASE", "https://mani7702-dot.github.io/contenthub").rstrip("/")
STATE = os.path.join(ROOT, "logs", "telegram-posted.json")
CONFIG = os.path.expanduser("~/.hermes/config.yaml")
DEFAULT_CHAT = "1363604644"          # owner DM; swap for a channel id when one exists
CAPTION_LIMIT = 1024


def bot_token():
    import yaml
    with open(CONFIG) as f:
        cfg = yaml.safe_load(f)
    tok = (cfg.get("telegram") or {}).get("bot_token")
    if not tok:
        sys.exit("no telegram.bot_token in %s" % CONFIG)
    return tok


def api(token, method, params):
    url = "https://api.telegram.org/bot%s/%s" % (token, method)
    data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(url, data)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return json.loads(e.read().decode())


def load_articles():
    with open(os.path.join(ROOT, "content.json")) as f:
        feed = json.load(f)
    out = []
    for board in ("news", "blog", "trending"):
        for a in feed.get("boards", {}).get(board, []):
            out.append(a)
    out.sort(key=lambda a: a.get("date", ""), reverse=True)
    return out


def load_state():
    if os.path.exists(STATE):
        with open(STATE) as f:
            return set(json.load(f))
    return set()


def save_state(ids):
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    with open(STATE, "w") as f:
        json.dump(sorted(ids), f, indent=1)


def caption_for(a):
    title = (a.get("title") or "").strip()
    excerpt = (a.get("excerpt") or "").strip()
    url = "%s/articles/%s.html" % (SITE, a.get("id"))
    head = "<b>%s</b>" % title.replace("&", "&amp;").replace("<", "&lt;")
    body = excerpt.replace("&", "&amp;").replace("<", "&lt;")
    text = head + "\n\n" + body + '\n\n<a href="%s">Read more →</a>' % url
    if len(text) > CAPTION_LIMIT:
        text = text[:CAPTION_LIMIT - 40].rstrip() + '…\n\n<a href="%s">Read more →</a>' % url
    return text, url


def post_one(token, chat, a):
    text, url = caption_for(a)
    img = a.get("image")
    if img:
        photo = img if img.startswith("http") else "%s/%s" % (SITE, img.lstrip("/"))
        r = api(token, "sendPhoto", {
            "chat_id": chat, "photo": photo, "caption": text,
            "parse_mode": "HTML",
        })
        if r.get("ok"):
            return True, "photo"
        # fall back to a text message if the image is unusable
    r = api(token, "sendMessage", {
        "chat_id": chat, "text": text, "parse_mode": "HTML",
        "disable_web_page_preview": False,
    })
    return bool(r.get("ok")), (r.get("description") or "message")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--count", type=int, default=1)
    ap.add_argument("--chat", default=os.environ.get("TELEGRAM_CHAT", DEFAULT_CHAT))
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--delay", type=float, default=3.0, help="seconds between posts")
    a = ap.parse_args()

    arts = load_articles()
    posted = load_state()

    if a.status:
        print("articles total : %d" % len(arts))
        print("already posted : %d" % len(posted))
        print("remaining      : %d" % len([x for x in arts if x.get("id") not in posted]))
        return

    todo = [x for x in arts if x.get("id") not in posted][:a.count]
    if not todo:
        print("nothing to post — all %d articles already sent" % len(arts))
        return

    if a.dry_run:
        for x in todo:
            print("[dry-run] %s -> %s/articles/%s.html" % (x.get("title"), SITE, x.get("id")))
        return

    token = bot_token()
    sent = 0
    for i, x in enumerate(todo):
        ok, how = post_one(token, a.chat, x)
        print("%s %s (%s)" % ("OK " if ok else "FAIL", x.get("id"), how))
        if ok:
            posted.add(x.get("id"))
            sent += 1
            save_state(posted)
        if i < len(todo) - 1:
            time.sleep(a.delay)
    print("posted %d/%d" % (sent, len(todo)))


if __name__ == "__main__":
    main()