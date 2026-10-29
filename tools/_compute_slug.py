import re
title = "How Did Scientists Date 128,000-Year-Old Ice From Tibet?"
slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:90]
print(repr(slug))
