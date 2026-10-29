import re
title = "How Did an Ancient Eclipse Show Earth Spun Faster 2,700 Years Ago?"
slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')[:90]
print("TITLE:", title)
print("SLUG:", slug)
print("LEN:", len(slug))
print("FILE:", slug + ".md")
