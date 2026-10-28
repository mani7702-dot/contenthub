import re

html = open('/home/ubuntu/contenthub/sd_raw.html', encoding='utf-8').read()

# Extract all paragraph text
paras = re.findall(r'<p[^>]*>(.{0,600})</p>', html, re.S)
for p in paras:
    text = re.sub(r'<[^>]+>', '', p)
    text = re.sub(r'&[a-z]+;', ' ', text)
    text = text.strip()
    if len(text) > 30:
        print(text[:400])
        print('---')
