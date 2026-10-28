import re

raw = open('/home/ubuntu/contenthub/bbc_raw.html', encoding='utf-8').read()

# The JSON uses escaped quotes inside the text values
# Pattern: \"text\":\"...\"
matches = re.findall(r'\\"text\\":\\"(.*?)\\"', raw)
seen = set()
for m in matches:
    t = m.replace('\\n', ' ').replace('\\u003C', '<').replace('\\u003E', '>')
    t = re.sub(r'\\"', '"', t)
    t = t.strip()
    if len(t) > 30 and t not in seen and not t.startswith('Copyright') and not t.startswith('Read') and not t.startswith('More on'):
        seen.add(t)
        print(t[:500])
        print('---')
