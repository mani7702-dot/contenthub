import re

raw = open('/home/ubuntu/contenthub/scar.html', encoding='utf-8').read()
# Find links mentioning gazetteer
links = re.findall(r'href="([^"]*gazetteer[^"]*)"', raw, re.I)
for l in links:
    print(l)
print("---")
# Also find the composite gazetteer link
links2 = re.findall(r'href="([^"]*)"', raw)
for l in links2:
    if 'gazetteer' in l.lower() or 'placename' in l.lower():
        print(l)
