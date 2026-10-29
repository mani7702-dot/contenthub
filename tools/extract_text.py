import re

# Parse ScienceDaily search results - look for links and headlines
with open('/tmp/sd-search.html', encoding='utf-8') as f:
    sd = f.read()

# Find result links
links = re.findall(r'href="(https?://[^"]+)"', sd)
for l in links:
    if 'sciencedaily' not in l and 'bbc' not in l.lower() and len(l) > 30:
        print("SD LINK:", l)

# Find headlines
heads = re.findall(r'<h3[^>]*>(.*?)</h3>', sd, re.S)
for h in heads[:10]:
    clean = re.sub(r'<[^>]+>', '', h).strip()
    if clean:
        print("SD HEAD:", clean)

print("----NEWSLUPLOOK----")
with open('/tmp/newslookup.html', encoding='utf-8') as f:
    nl = f.read()
heads2 = re.findall(r'<h3[^>]*>(.*?)</h3>', nl, re.S)
for h in heads2[:15]:
    clean = re.sub(r'<[^>]+>', '', h).strip()
    if clean:
        print("NL HEAD:", clean)
links2 = re.findall(r'href="(https?://[^"]+)"', nl)
for l in links2:
    if 'bbc' not in l.lower() and 'newslookup' not in l:
        print("NL LINK:", l)
