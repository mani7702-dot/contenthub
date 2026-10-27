import re, sys, os

def extract_article(html_path):
    with open(html_path, 'r', errors='replace') as f:
        html = f.read()
    
    # Try to find the main article body
    # BBC articles often have content in <article> tags or specific divs
    # Let's look for paragraphs
    paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', html, re.DOTALL)
    
    print(f"\n=== Found {len(paragraphs)} paragraphs ===")
    for i, p in enumerate(paragraphs):
        # Clean HTML tags
        clean = re.sub(r'<[^>]+>', '', p).strip()
        if len(clean) > 30:
            print(f"P{i}: {clean[:200]}")

for slug in ["badge-sends-to-space", "spaceplane"]:
    path = f"/home/ubuntu/contenthub/temp_{slug}.html"
    if os.path.exists(path):
        print(f"\n{'='*60}")
        print(f"Article: {slug}")
        print('='*60)
        extract_article(path)
