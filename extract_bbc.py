import re

html = open('/home/ubuntu/contenthub/bbc_raw.html', encoding='utf-8').read()

# Find the article text blocks - BBC uses JSON with "text":"..." patterns
# Also look for the full article body
blocks = re.findall(r'"text":"([^"]{0,800})"', html)
seen = set()
for b in blocks:
    text = b.replace('\\n', ' ').replace('\\u003C', '<').replace('\\u003E', '>').strip()
    if len(text) > 30 and text not in seen:
        seen.add(text)
        print(text[:400])

print("=== Also checking for the full text block ===")
# Look for a larger context around "Amos Channel"
idx = html.find("Amos Channel")
if idx >= 0:
    snippet = html[idx-200:idx+500]
    snippet = snippet.replace('\\n', ' ').replace('\\u003C', '<').replace('\\u003E', '>')
    print(snippet[:800])
