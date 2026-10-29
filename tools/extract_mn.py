import re

with open('/tmp/mn_sugar.html', 'r') as f:
    html = f.read()

text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
text = re.sub(r'<[^>]+>', ' ', text)
text = re.sub(r'\s+', ' ', text)
# Find content around key terms
for kw in ['sweetener', 'cognitive', 'Neurology', 'brain', 'aspartame', 'saccharin']:
    idx = text.lower().find(kw.lower())
    if idx >= 0:
        print(f"\n--- Around '{kw}' ---")
        print(text[max(0,idx-100):idx+300])
print("\n\n=== First 3000 chars of body ===")
body_start = text.find('Artificial sweeteners')
if body_start < 0:
    body_start = text.find('sweetener')
print(text[body_start:body_start+3000])
