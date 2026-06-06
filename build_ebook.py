"""Build ebook.html from template + pages data."""
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\Users\miikharo\lpi-study-app\ebook_pages.json', 'r', encoding='utf-8') as f:
    pages = json.load(f)

with open(r'C:\Users\miikharo\lpi-study-app\ebook_template.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('__EBOOK_DATA__', json.dumps(pages, ensure_ascii=False))

with open(r'C:\Users\miikharo\lpi-study-app\ebook.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Built ebook.html ({len(html):,} bytes, {len(pages)} pages)")
