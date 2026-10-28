import re

html = open('/home/ubuntu/contenthub/bbc_raw.html', encoding='utf-8').read()
matches = re.findall(r'"text":"([^"]{0,800})', html)
for m in matches:
    t = m.replace('\\n', ' ').replace('\\u003C', '<').replace('\\u003E', '>')
    if any(k in t.lower() for k in ['amos', 'channel', 'antarctica', 'rothchild', 'alexander', 'shackleton', 'endurance']):
        print(t[:400])
        print('---')
