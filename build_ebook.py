"""Embed ebook_pages.json directly into ebook.html so it works with file:// protocol."""
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\Users\miikharo\lpi-study-app\ebook_pages.json', 'r', encoding='utf-8') as f:
    pages = json.load(f)

with open(r'C:\Users\miikharo\lpi-study-app\ebook.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the fetch() call with inline data
old_init = """async function init(){
  const resp=await fetch('ebook_pages.json');
  pages=await resp.json();"""

new_init = f"""async function init(){{
  pages={json.dumps(pages, ensure_ascii=False)};"""

html = html.replace(old_init, new_init)

with open(r'C:\Users\miikharo\lpi-study-app\ebook.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Embedded {len(pages)} pages into ebook.html ({len(html):,} bytes)")
