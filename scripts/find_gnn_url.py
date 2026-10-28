import urllib.request
import re

# Fetch GNN homepage to find the actual URL
url = 'https://www.goodnewsnetwork.org/category/family/'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)'})
resp = urllib.request.urlopen(req, timeout=15)
html = resp.read().decode('utf-8')

# Find links containing 'housefire' or 'fostered'
links = re.findall(r'href="(https://www\.goodnewsnetwork\.org/[^"]*fostered[^"]*)"', html, re.IGNORECASE)
if not links:
    links = re.findall(r'href="(https://www\.goodnewsnetwork\.org/[^"]*housefire[^"]*)"', html, re.IGNORECASE)
if not links:
    links = re.findall(r'href="(https://www\.goodnewsnetwork\.org/[^"]*500[^"]*)"', html, re.IGNORECASE)

print("Found links:", links)

# If not found on family page, search the main GNN page
if not links:
    url2 = 'https://www.goodnewsnetwork.org/'
    req2 = urllib.request.Request(url2, headers={'User-Agent': 'Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)'})
    resp2 = urllib.request.urlopen(req2, timeout=15)
    html2 = resp2.read().decode('utf-8')
    links = re.findall(r'href="(https://www\.goodnewsnetwork\.org/[^"]*(?:fostered|housefire|500)[^"]*)"', html2, re.IGNORECASE)
    print("Found links from homepage:", links)
