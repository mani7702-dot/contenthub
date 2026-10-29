#!/usr/bin/env python3
"""Cross-check more nuclear testing facts."""
import subprocess, re

UA = "Mozilla/5.0 (ContentHub reader; contact andugulamani722@gmail.com)"

def fetch(url):
    p = subprocess.run(["curl", "-sL", "--max-time", "30", "-A", UA, url], capture_output=True)
    return p.stdout.decode("utf-8", errors="replace")

def strip_html(text):
    html = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
    html = re.sub(r'<[^>]+>', ' ', html)
    html = re.sub(r'&[a-z#0-9]+;', ' ', html)
    html = re.sub(r'\s+', ' ', html).strip()
    return html

# Source: Wikipedia on Cesium-137
print("=== Wikipedia Cesium-137 ===")
url1 = "https://en.wikipedia.org/wiki/Caesium-137"
html1 = fetch(url1)
text1 = strip_html(html1)
for keyword in ["Chernobyl", "nuclear weapon", "bomb", "half-life", "fallout"]:
    idx = text1.lower().find(keyword.lower())
    if idx >= 0:
        print(f"\n[{keyword}]: {text1[max(0,idx-100):idx+400]}")
        break

# Source: Wikipedia on nuclear weapon tests and environmental impact
print("\n\n=== Wikipedia on environmental effects ===")
url2 = "https://en.wikipedia.org/wiki/Environmental_impact_of_nuclear_weapons"
html2 = fetch(url2)
text2 = strip_html(html2)
# Look for relevant sections
for keyword in ["honey", "wild boar", "boar", "baby tooth", "tooth", "strontium-90", "cesium", "bomb pulse", "Law Dome", "Antarctica"]:
    idx = text2.lower().find(keyword.lower())
    if idx >= 0:
        print(f"\n[{keyword}]: {text2[max(0,idx-100):idx+300]}")
        break

# Source: Wikipedia on Baby Tooth Survey
print("\n\n=== Wikipedia Baby Tooth Survey ===")
url3 = "https://en.wikipedia.org/wiki/Baby_Tooth_Health_Curve_Study"
html3 = fetch(url3)
text3 = strip_html(html3)
idx = text3.find("strontium")
if idx >= 0:
    print(text3[max(0,idx-100):idx+500])
else:
    print(text3[:3000])
