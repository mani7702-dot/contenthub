import re

raw = open('/home/ubuntu/contenthub/bbc_raw.html', encoding='utf-8').read()

# The JSON has escaped quotes. Let me find all text content between escaped quotes
# Pattern: \"text\":\"... content ...\",\"blocks
matches = re.findall(r'\\"text\\":\\"(.*?)\\"\s*,\s*\\"blocks', raw, re.DOTALL)
print(f"Found {len(matches)} blocks")
for m in matches:
    t = m.replace('\\n', ' ').replace('\\u003C', '<').replace('\\u003E', '>')
    t = re.sub(r'\\"', '"', t)
    t = t.strip()
    if len(t) > 20:
        print(t[:500])
        print('---')
