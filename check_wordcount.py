import re

with open('content/news/2026-10-27-welsh-school-pupils-meet-nasa-astronaut-after-badge-flies-to-iss.md') as f:
    content = f.read()

m = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.S)
if m:
    body = m.group(2)
    words = len(body.split())
    print(f'Body word count: {words}')
