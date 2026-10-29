#!/usr/bin/env python3
"""Cross-check more nuclear testing facts - round 3."""
import subprocess, re

UA = "Mozilla/5.0 (ContentHub reader; contact andugulamani722@gmail.com)"

def fetch(url):
    p = subprocess.run(["curl", "-sL", "--max-time", "30", "-A", UA, url], capture_output=True)
    return p.stdout.decode("utf-8", errors="replace")

def strip_html(text):
    result = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL)
    result = re.sub(r'<style[^>]*>.*?</style>', '', result, flags=re.DOTALL)
    result = re.sub(r'<[^>]+>', ' ', result)
    result = re.sub(r'&[a-z#0-9]+;', ' ', result)
    result = re.sub(r'\s+', ' ', result).strip()
    return result

# Wikipedia on Fallout - baby teeth section
print("=== Wikipedia Fallout - baby teeth ===")
url1 = "https://en.wikipedia.org/wiki/Nuclear_fallout"
html1 = fetch(url1)
text1 = strip_html(html1)
for keyword in ["baby tooth", "tooth", "strontium-90", "Sr-90", "milk teeth", "St. Louis"]:
    idx = text1.lower().find(keyword.lower())
    if idx >= 0:
        print(f"\n[{keyword}]: {text1[max(0,idx-100):idx+400]}")

# Wikipedia on Strontium-90
print("\n\n=== Wikipedia Strontium-90 ===")
url2 = "https://en.wikipedia.org/wiki/Strontium-90"
html2 = fetch(url2)
text2 = strip_html(html2)
for keyword in ["baby", "tooth", "bone", "milk", "children", "fallout", "bomb"]:
    idx = text2.lower().find(keyword.lower())
    if idx >= 0:
        print(f"\n[{keyword}]: {text2[max(0,idx-100):idx+400]}")
        break

# Wikipedia on wild boar / boar radiation
print("\n\n=== Wikipedia Wild boar / radiation ===")
url3 = "https://en.wikipedia.org/wiki/Wild_boar#Interaction_with_humans"
html3 = fetch(url3)
text3 = strip_html(html3)
idx = text3.lower().find("radioactive")
if idx >= 0:
    print(text3[max(0,idx-100):idx+500])

# Also search for Chernobyl boar study
url4 = "https://en.wikipedia.org/wiki/Chernobyl_disaster#Wildlife"
html4 = fetch(url4)
text4 = strip_html(html4)
idx4 = text4.lower().find("boar")
if idx4 >= 0:
    print(f"\n[boar]: {text4[max(0,idx4-100):idx4+400]}")
