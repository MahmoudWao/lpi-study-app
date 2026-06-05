"""Inject structured data into app template to produce final index.html."""
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\Users\miikharo\lpi-study-app\structured_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Remove full_lesson from embedded data to reduce file size (keep lesson_excerpt)
for sec in data.values():
    if 'full_lesson' in sec:
        # Keep only first 5000 chars of full lesson for the app (it's still deep)
        sec['full_lesson'] = sec['full_lesson'][:5000]

with open(r'C:\Users\miikharo\lpi-study-app\app_template.html', 'r', encoding='utf-8') as f:
    html = f.read()

json_str = json.dumps(data, ensure_ascii=False)
html = html.replace('__STRUCTURED_DATA__', json_str)

with open(r'C:\Users\miikharo\lpi-study-app\index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Built index.html: {len(html):,} bytes")
print(f"Sections: {len(data)}")
total_cards = sum(
    len(s['qa_pairs']) + len(s['commands']) + len(s['concepts'])
    for s in data.values()
)
print(f"Total potential cards: {total_cards}")
