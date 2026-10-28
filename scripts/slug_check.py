import re
title = "10 Amazing Animals Discovered in Places You Least Expect"
slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:90]
print(slug)
