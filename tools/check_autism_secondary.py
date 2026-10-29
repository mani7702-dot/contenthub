#!/usr/bin/env python3
"""Find secondary sources confirming the autism face processing study."""
import requests
import re

headers = {"User-Agent": "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"}

# Check PubMed for the exact paper
try:
    r = requests.get("https://pubmed.ncbi.nlm.nih.gov/?term=Griffin+McPartland+face+autism+Nature+Mental+Health+2026", headers=headers, timeout=15)
    print(f"PubMed exact search Status: {r.status_code}")
    # Look for the paper
    ids = re.findall(r'/pubmed/(\d+)', r.text)
    print(f"Found PubMed IDs: {ids[:5]}")

    # Also try the more specific author search
    r2 = requests.get("https://pubmed.ncbi.nlm.nih.gov/?term=decoding+temporal+dynamics+face+specific+neural+representations+autism", headers=headers, timeout=15)
    print(f"\nPubMed title search Status: {r2.status_code}")
    # Extract PMID
    pmids = re.findall(r'pmid["\s:]+(\d+)', r2.text, re.IGNORECASE)
    print(f"Found PMIDs: {pmids[:5]}")
    # Extract titles
    titles = re.findall(r'<a[^>]*class="docsum-title"[^>]*>(.*?)</a>', r2.text, re.DOTALL)
    for t in titles[:5]:
        text = re.sub(r'<[^>]+>', '', t).strip()
        text = re.sub(r'\s+', ' ', text)
        print(f"  PubMed: {text[:200]}")
except Exception as e:
    print(f"PubMed Error: {e}")

# Check the journal Nature Mental Health
try:
    r = requests.get("https://www.nature.com/nmeth/", headers=headers, timeout=15)
    print(f"\nNature Mental Health journal Status: {r.status_code}")
except Exception as e:
    print(f"Nature journal Error: {e}")

# Check ScienceDaily related stories section for corroborating articles
try:
    r = requests.get("https://www.sciencedaily.com/releases/2026/10/261027063824.htm", headers=headers, timeout=20)
    print(f"\nScienceDaily article Status: {r.status_code}")
    # Extract the journal reference
    doi_match = re.search(r'DOI:\s*([\d\.\/-]+)', r.text)
    if doi_match:
        print(f"DOI: {doi_match.group(1)}")
    # Extract journal name
    journal_match = re.search(r'<i>(.*?)</i>', r.text)
    if journal_match:
        print(f"Journal: {journal_match.group(1).strip()[:100]}")
    # Look for related story links
    related = re.findall(r'href="(https://www\.sciencedaily\.com/releases/[^"]+)"', r.text)
    for link in related[:3]:
        print(f"Related: {link}")
except Exception as e:
    print(f"ScienceDaily fetch error: {e}")
