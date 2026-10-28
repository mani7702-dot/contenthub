import re

# The regex from build.py line 41
pattern = r"^---\s*\n(.*?)\\n---\s*\n?(.*)$"
print(f"Pattern chars: {[c for c in pattern]}")

text = open("content/news/2026-10-28-how-did-a-wrong-turn-save-14-lives-from-a-burning-house-in-georgia.md", encoding="utf-8").read()

m = re.match(pattern, text, re.S)
if m:
    print("Matched!")
else:
    print("No match with build.py pattern")

# Try with corrected pattern
pattern2 = r"^---\s*\n(.*?)\n---\s*\n?(.*)$"
m2 = re.match(pattern2, text, re.S)
if m2:
    print("Matched with corrected pattern!")
    print("Frontmatter:", m2.group(1)[:100])
else:
    print("No match with corrected pattern")

# Test with walrus article
text2 = open("content/news/how-did-a-baby-walrus-named-annautaq-get-a-second-chance.md", encoding="utf-8").read()
m3 = re.match(pattern, text2, re.S)
if m3:
    print("Walrus matched with build.py pattern!")
else:
    print("Walrus did NOT match with build.py pattern")
