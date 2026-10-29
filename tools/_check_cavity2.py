#!/usr/bin/env python3
"""Try different URLs for the SDF/ScienceDaily article."""
import urllib.request
import re

urls = [
    "https://www.sciencedaily.com/news/matter_energy/health_meds/dental_health/",
    "https://www.sciencedaily.com/news/mind_brain/autism/",
]

# Actually, let's just try to search on the GNN page for the ScienceDaily link
url = "https://www.goodnewsnetwork.org/fda-approval-for-drill-free-cavity-care-may-be-imminent-after-great-phase-3-treatment-trial/"

req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)'
})
resp = urllib.request.urlopen(req, timeout=15)
html = resp.read().decode('utf-8', errors='replace')

# Look for ScienceDaily links
links = re.findall(r'https://www\.sciencedaily\.com/[^\s"]+', html)
for link in links:
    print(f"  {link}")
