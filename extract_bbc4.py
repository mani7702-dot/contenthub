import re, json

raw = open('/home/ubuntu/contenthub/bbc_raw.html', encoding='utf-8').read()

# The article text appears as escaped JSON in the page
# Look for patterns like: "text":"actual text content with spaces"
# The content has escaped newlines as \n (literal backslash-n)

# Find the script block that contains the article content
# BBC uses __APOLLO_STATE__ or similar
# Let's find all large text blocks

# Try finding the JSON content for the article
matches = re.findall(r'\\"text\\":\\"([^\\"]*?\\.[^\\"]*?\\.[^\\"]*?\\.)\\"', raw)
seen = set()
for m in matches:
    t = m.replace('\\n', ' ').replace('\\u003C', '<').replace('\\u003E', '>')
    t = t.strip()
    if len(t) > 30 and t not in seen:
        seen.add(t)
        print(t[:500])
        print('---')

# Also try direct extraction of article body
print("=== Direct search ===")
# Find the article body content - look for sentences about Amos
idx = raw.find('"Amos was given the honour')
if idx >= 0:
    snippet = raw[idx:idx+2000]
    # Remove escaped quotes
    snippet = snippet.replace('\\"', '"').replace('\\/', '/').replace('\\n', ' ')
    print(snippet[:800])
