import re, urllib.request

def fetch(url, desc=""):
    print(f"=== {desc}: {url} ===")
    req = urllib.request.Request(url, headers={'User-Agent': 'ContentHub (research; contact andugulamani722@gmail.com)'})
    try:
        html = urllib.request.urlopen(req, timeout=20).read().decode('utf-8', errors='ignore')
        # Extract paragraph text
        paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', html, re.DOTALL)
        text = ' '.join(p for p in paragraphs)
        text = re.sub(r'<[^>]+>', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        print(text[:2000] if text else "(no paragraph text found)")
    except Exception as e:
        print(f"ERROR: {e}")

# Source 2: Nature News article
fetch("https://www.nature.com/articles/d44151-026-00164-z", "Nature News")

# Source 3: Discover Wildlife
fetch("https://www.discoverwildlife.com/animal-facts/fish/gangaichthys-indonepalicus-india", "Discover Wildlife")

# Source 4: PMC (original paper)
fetch("https://www.ncbi.nlm.nih.gov/pmc/articles/PMC13487515", "PMC/NCBI paper")
