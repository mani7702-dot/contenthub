import urllib.request
import re
from html.parser import HTMLParser

url = 'https://www.goodnewsnetwork.org/family-thats-fostered-500-children-saved-from-housefire-thanks-to-strangers-wrong-turn/'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)'})
resp = urllib.request.urlopen(req, timeout=15)
html = resp.read().decode('utf-8')

# Extract article body - look for the main content paragraphs
# Find the article body section
idx = html.find('class="entry-content')
if idx > 0:
    chunk = html[idx:idx+8000]
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '\n', chunk)
    text = re.sub(r'\n\s*\n', '\n', text)
    text = re.sub(r'\s+', ' ', text)
    print(text[:5000])
else:
    print("Could not find article body")
