import re, html as html_mod

raw = open('/home/ubuntu/contenthub/wiki_naming.html', encoding='utf-8').read()

paras = re.findall(r'<p[^>]*>(.{0,800})</p>', raw, re.S)
for p in paras:
    text = re.sub(r'<[^>]+>', '', p)
    text = html_mod.unescape(text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    if len(text) > 30:
        print(text[:500])
        print('---')
