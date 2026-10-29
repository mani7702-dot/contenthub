import re
t = 'Who Was Panther Pat, the First Woman to Play Pro Football?'
slug = re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')[:90]
print(slug)
