#!/usr/bin/env bash
# ContentHub publish loop: build -> verify -> commit -> push -> wait for Pages.
# Usage: tools/deploy.sh "<board>: <title>" "<slug>"
set -euo pipefail
cd "$(dirname "$0")/.."

MSG="${1:-publish content}"
SLUG="${2:-}"
BRANCH=main

# never push a stale build
python3 build.py >logs/build.log 2>&1 || { echo "ERROR: build.py failed"; tail -20 logs/build.log; exit 1; }
tail -1 logs/build.log

git add -A
if git diff --cached --quiet; then
  echo "nothing to publish"; exit 0
fi
git -c user.name="mani7702-dot" -c user.email="mani7702-dot@users.noreply.github.com" \
    commit -q -m "$MSG"
git pull --rebase --autostash -q origin "$BRANCH"
git push -q origin "$BRANCH" || { echo "ERROR: push failed"; exit 6; }
echo "pushed: $(git rev-parse --short HEAD)"

# wait for Pages, then verify the article is live
BASE="https://mani7702-dot.github.io/contenthub"
[ -z "$SLUG" ] && exit 0
for i in $(seq 1 20); do
  code=$(curl -s -o /dev/null -w %{http_code} "$BASE/articles/$SLUG.html" || true)
  if [ "$code" = "200" ]; then echo "live 200 -> $BASE/articles/$SLUG.html"; exit 0; fi
  sleep 15
done
echo "WARN: article not 200 yet (last $code) -> $BASE/articles/$SLUG.html"
exit 7
