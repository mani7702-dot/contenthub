import re

text = open("content/news/2026-10-28-how-did-a-wrong-turn-save-14-lives-from-a-burning-house-in-georgia.md", encoding="utf-8").read()

m = re.match(r"^---\s*\n(.*?)\\n---\s*\n?(.*)$", text, re.S)
if m:
    print("Matched!")
    print("Frontmatter:", m.group(1)[:200])
    print("Body:", m.group(2)[:200])
else:
    print("No match")
    
# Try the regex with single backslash
m2 = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.S)
if m2:
    print("\nMatched with single backslash!")
    print("Frontmatter:", m2.group(1)[:200])
    print("Body:", m2.group(2)[:200])
else:
    print("\nNo match with single backslash either")
