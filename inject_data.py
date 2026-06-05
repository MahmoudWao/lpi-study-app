"""Inject quiz data into the HTML template to produce the final app."""
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\Users\miikharo\lpi-study-app\quiz_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open(r'C:\Users\miikharo\lpi-study-app\template.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Embed the JSON data
json_str = json.dumps(data, ensure_ascii=False)
html = html.replace('QUIZ_DATA_PLACEHOLDER', json_str)

with open(r'C:\Users\miikharo\lpi-study-app\index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Built index.html ({len(html)} bytes)")
print(f"Embedded {len(data)} sections of quiz data")
