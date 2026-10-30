#!/usr/bin/env python3
"""Fetch the full PMC article and Nature article for the gut microbiome aging study."""
import subprocess, re

ua = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# PubMed PMID: 42443264
# DOI: 10.1038/s41598-026-52974-x
# PMC: PMC13365576

# Fetch the full PMC article text
print("=== PMC Full Text ===")
pmc_url = "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC13365576/"
p = subprocess.run(["curl", "-sL", "--max-time", "15", "-A", ua, "-H", "Accept: text/html", pmc_url], capture_output=True)
html = p.stdout.decode("utf-8", errors="replace")
print(f"PMC chars: {len(html)}")
# Extract title
title = re.search(r'<title[^>]*>(.*?)</title>', html, re.DOTALL | re.IGNORECASE)
if title:
    print(f"Title: {title.group(1).strip()[:200]}")
# Extract abstract
abstract_match = re.search(r'<h2[^>]*>Abstract</h2>(.*?)</div>', html, re.DOTALL | re.IGNORECASE)
if abstract_match:
    abstract = re.sub(r"<[^>]+>", "", abstract_match.group(1)).strip()
    print(f"\nAbstract: {abstract[:500]}")
# Extract body paragraphs
html_clean = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)
html_clean = re.sub(r"<style[^>]*>.*?</style>", "", html_clean, flags=re.DOTALL | re.IGNORECASE)
paras = re.findall(r"<p[^>]*>(.*?)</p>", html_clean, re.DOTALL | re.IGNORECASE)
for i, para in enumerate(paras):
    clean = re.sub(r"<[^>]+>", "", para).strip()
    if len(clean) > 40 and any(term in clean.lower() for term in ["bifidobacterium", "succinivibrio", "dunedin", "15%", "123", "microbiome", "aging", "blood", "stool"]):
        print(f"\nPARA {i}: {clean[:400]}")

# Fetch the Nature article page
print("\n\n=== Nature Article Page ===")
nature_url = "https://www.nature.com/articles/s41598-026-52974-x"
p = subprocess.run(["curl", "-sL", "--max-time", "15", "-A", ua, "-H", "Accept: text/html", nature_url], capture_output=True)
html2 = p.stdout.decode("utf-8", errors="replace")
print(f"Nature chars: {len(html2)}")
title2 = re.search(r'<meta name="dc.title" content="(.*?)"', html2) or re.search(r'<title[^>]*>(.*?)</title>', html2, re.DOTALL | re.IGNORECASE)
if title2:
    print(f"Title: {title2.group(1).strip()[:200]}")
description = re.search(r'<meta name="description" content="(.*?)"', html2)
if description:
    print(f"Description: {description.group(1).strip()[:300]}")
# Look for abstract
abstract2 = re.search(r'<div[^>]*id="abstract"[^>]*>(.*?)</div>', html2, re.DOTALL | re.IGNORECASE)
if abstract2:
    abs_text = re.sub(r"<[^>]+>", "", abstract2.group(1)).strip()
    print(f"Abstract: {abs_text[:500]}")
# Check for key terms
for term in ["Bifidobacterium", "Succinivibrio", "DunedinPACE", "123", "15%", "stool", "blood"]:
    if term.lower() in html2.lower():
        print(f"  ✓ Found: {term}")
    else:
        print(f"  ✗ Missing: {term}")
# Extract abstract from meta
abstract_meta = re.search(r'<meta name="citation_abstract" content="(.*?)"', html2, re.DOTALL)
if abstract_meta:
    print(f"\nCitation Abstract: {abstract_meta.group(1)[:500]}")
