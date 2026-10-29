import re

with open('/tmp/msn-amos.html', encoding='utf-8') as f:
    html = f.read()

# Find all occurrences of key facts
for kw in ['Amos Channel', 'Rothschild', 'Alexander Island', '1986', '1997', '2024', 'Athena Dinar', 'Jonathan Amos', 'Antarctica']:
    for m in re.finditer(re.escape(kw), html, re.IGNORECASE):
        start = max(0, m.start()-40)
        end = min(len(html), m.end()+80)
        snippet = html[start:end]
        snippet = re.sub(r'<[^>]+>', ' ', snippet)
        snippet = re.sub(r'\s+', ' ', snippet).strip()
        print(f"[{kw}]: ...{snippet}...")

print("---TOTAL LEN---", len(html))
# print a chunk around 'channel'
idx = html.lower().find('amos channel')
if idx >= 0:
    chunk = html[idx-200:idx+1500]
    chunk = re.sub(r'<[^>]+>', ' ', chunk)
    chunk = re.sub(r'\s+', ' ', chunk)
    print("CONTEXT:", chunk[:1600])
