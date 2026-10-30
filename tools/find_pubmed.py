#!/usr/bin/env python3
"""Try PubMed and Europe PMC to find the gut microbiome aging study."""
import subprocess, re, json

ua = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# Try PubMed search
print("=== PubMed search ===")
pm_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=gut+microbiome+biological+aging+Maunakea&retmode=json&retmax=5"
p = subprocess.run(["curl", "-sL", "--max-time", "15", "-A", ua, pm_url], capture_output=True)
pm_response = p.stdout.decode("utf-8", errors="replace")
print(f"PubMed response: {pm_response[:500]}")

# If we got PMIDs, fetch details
try:
    pm_data = json.loads(pm_response)
    if "esearchresult" in pm_data and pm_data["esearchresult"]["idlist"]:
        pmids = pm_data["esearchresult"]["idlist"]
        print(f"PMIDs found: {pmids}")
        for pmid in pmids:
            detail_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={pmid}&retmode=text&rettype=abstract"
            p2 = subprocess.run(["curl", "-sL", "--max-time", "15", "-A", ua, detail_url], capture_output=True)
            abstract = p2.stdout.decode("utf-8", errors="replace")
            print(f"\n--- PMID: {pmid} ---")
            print(abstract[:1000])
except Exception as e:
    print(f"PubMed parse error: {e}")

# Try Europe PMC
print("\n=== Europe PMC ===")
epc_url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=gut+microbiome+biological+aging+Maunakea&format=json&resultType=core"
p = subprocess.run(["curl", "-sL", "--max-time", "15", "-A", ua, epc_url], capture_output=True)
epc_response = p.stdout.decode("utf-8", errors="replace")
print(f"Europe PMC chars: {len(epc_response)}")
print(f"Response: {epc_response[:500]}")

# Try the DOI directly - find via Crossref
print("\n=== Crossref search ===")
cr_url = "https://api.crossref.org/works?query=gut+microbiome+biological+aging+Maunakea&rows=3"
p = subprocess.run(["curl", "-sL", "--max-time", "15", "-A", ua, cr_url], capture_output=True)
cr_response = p.stdout.decode("utf-8", errors="replace")
print(f"Crossref chars: {len(cr_response)}")
# Parse JSON
try:
    cr_data = json.loads(cr_response)
    if "message" in cr_data and "items" in cr_data["message"]:
        for item in cr_data["message"]["items"]:
            title = item.get("title", [""])[0] if isinstance(item.get("title"), list) else item.get("title", "")
            doi = item.get("DOI", "")
            journal = item.get("container-title", [""])[0] if isinstance(item.get("container-title"), list) else item.get("container-title", "")
            print(f"  Title: {title[:200]}")
            print(f"  DOI: {doi}")
            print(f"  Journal: {journal}")
            print(f"  URL: {item.get('URL', '')}")
            print()
except Exception as e:
    print(f"Crossref parse error: {e}")
    print(cr_response[:500])
