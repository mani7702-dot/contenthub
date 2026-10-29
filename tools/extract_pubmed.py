import re

with open('/tmp/pubmed_sugar.html', 'r') as f:
    html = f.read()

text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
text = re.sub(r'<[^>]+>', ' ', text)
text = re.sub(r'\s+', ' ', text)

# Find the abstract and key sections
for kw in ['Abstract', 'cognitive', 'sweetener', 'Neurology', 'aspartame', 'saccharin', 'Brazil']:
    idx = text.find(kw)
    if idx >= 0:
        print(f"--- Around '{kw}' (at {idx}) ---")
        print(text[max(0,idx-50):idx+500])
        print()
