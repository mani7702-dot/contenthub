import re

raw = open('/home/ubuntu/contenthub/wiki_alex.html', encoding='utf-8').read()

# Check what the page actually contains
print("Title:", re.findall(r'<title>(.*?)</title>', raw)[:1])
print("First 500 chars of body:")
body = re.findall(r'<body.*?>(.*?)</body>', raw, re.S)
if body:
    text = re.sub(r'<[^>]+>', ' ', body[0])
    text = re.sub(r'\s+', ' ', text)
    print(text[:500])
else:
    # Try finding main content
    mw = re.findall(r'<div id="mw-content-text".*?</div>', raw, re.S)
    if mw:
        text = re.sub(r'<[^>]+>', ' ', mw[0])
        text = re.sub(r'\s+', ' ', text)
        print(text[:500])
    else:
        print("No content found, searching for key terms...")
        print("Alexander Island" in raw)
        print("Rothschild" in raw)
