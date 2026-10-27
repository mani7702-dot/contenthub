#!/usr/bin/env bash
# ContentHub publish loop: build -> commit -> push -> wait for Pages -> verify live URL.
# Usage: tools/deploy.sh "<commit message>" ["<md file relative to repo root>"]
set -uo pipefail
cd "$(dirname "$0")/.."
MSG="${1:-publish content}"
MD="${2:-}"

python3 build.py >logs/build.log 2>&1 || { echo "ERROR: build.py failed"; tail -20 logs/build.log; exit 1; }
tail -1 logs/build.log

git add -A
if git diff --cached --quiet; then
  echo "nothing to publish"; exit 0
fi
git -c user.name="mani7702-dot" -c user.email="mani7702-dot@users.noreply.github.com" \
    commit -q -m "$MSG"
git pull --rebase --autostash -q origin main
git push -q origin main || { echo "ERROR: push failed"; exit 6; }
echo "pushed: $(git rev-parse --short HEAD)"

# article URL = title-derived slug (build.py logic), same as build.py
SLUG=""
if [ -n "$MD" ]; then
  TITLE=$(sed -n "s/^title: *[\"\x27]*\(.*\)[\"\x27]*$/\1/p" "$MD" | head -1)
  SLUG=$(echo "$TITLE" | tr "[:upper:]" "[:lower:]" | sed "s/[^a-z0-9]\+/-/g; s/^-//; s/-\$//" | cut -c1-90)
fi
[ -z "$SLUG" ] && exit 0

BASE="https://mani7702-dot.github.io/contenthub"
for i in $(seq 1 20); do
  code=$(curl -s -o /dev/null -w "%{http_code}" "$BASE/articles/$SLUG.html" || true)
  [ "$code" = "200" ] && { echo "live 200 -> $BASE/articles/$SLUG.html"; exit 0; }
  sleep 15
done
echo "WARN: $SLUG not 200 yet (last $code)"
exit 7
