import re

html = open('/home/ubuntu/contenthub/bbc_raw.html', encoding='utf-8').read()

# The JSON has escaped quotes, so look for text fragments with escaped patterns
blocks = re.findall(r'"text":"([^"]*)"', html)
seen = set()
for b in blocks:
    # Handle escaped unicode
    text = b.replace('\\n', ' ')
    # Replace escaped unicode sequences
    text = re.sub(r'\\u003C', '<', text)
    text = re.sub(r'\\u003E', '>', text)
    text = re.sub(r'\\u0022', '"', text)
    text = text.strip()
    if len(text) > 20 and text not in seen:
        seen.add(text)
        print(text[:500])
        print('---')
