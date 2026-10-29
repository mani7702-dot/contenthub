import re

title = "How Did a TikTok Video Reveal a Whole New Kind of Underground Fish?"
slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:90]
print(f"Title: {title}")
print(f"Slug:  {slug}")
