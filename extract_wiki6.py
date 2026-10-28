import re, html as html_mod

raw = open('/home/ubuntu/contenthub/wiki_apc.html', encoding='utf-8').read()
print("Title:", re.findall(r'<title>(.*?)</title>', raw)[:1])
body = re.findall(r'<div id="mw-content-text".*?>(.*?)<div id="catlinks"', raw, re.S)
if body:
    text = re.sub(r'<[^>]+>', ' ', body[0])
    text = html_mod.unescape(text)
    text = re.sub(r'\s+', ' ', text)
    print(text[:1000])
else:
    print("Could not find mw-content-text, trying body...")
    body = re.findall(r'<body.*?>(.*?)<div id=', raw, re.S)
    if body:
        text = re.sub(r'<[^>]+>', ' ', body[0][:2000])
        text = html_mod.unescape(text)
        text = re.sub(r'\s+', ' ', text)
        print(text[:1000])
