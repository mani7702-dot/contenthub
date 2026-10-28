#!/usr/bin/env python3
"""Cross-check: search for corroborating articles about the teacher positivity story."""
import subprocess, re, html

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

queries = [
    "Tyler Richards Rex Elementary School positive affirmations Kansas",
    "Rex Elementary Haysville Kansas daily positivity affirmations Principal Shane Paulus",
    "Kansas elementary school positive affirmations children 'I can do hard things'",
]

for q in queries:
    print(f"\n=== Query: {q} ===")
    search_url = f"https://www.google.com/search?q={subprocess.quote(q)}"
    r = subprocess.run(["curl", "-s", "--max-time", "20", "-A", UA, "-L", search_url], capture_output=True, text=True)
    print(f"Page length: {len(r.stdout)}")
    text = re.sub(r"<script[^>]*>.*?</script>", "", r.stdout, flags=re.DOTALL)
    text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", "\n", text)
    text = html.unescape(text)
    lines = [l.strip() for l in text.split("\n") if l.strip() and len(l.strip()) > 30]
    for line in lines[:20]:
        print(line[:300])
