import sys, io, json, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\Users\miikharo\lpi-study-app\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Basic checks
assert '<!DOCTYPE html>' in html
assert '</html>' in html
assert 'QUIZ_DATA_PLACEHOLDER' not in html
assert 'const DATA =' in html
assert '1.1' in html
assert 'Linux Evolution' in html
assert 'flashcard' in html
assert 'quiz' in html

# Check JSON is valid embedded data
match = re.search(r'const DATA = ({.*?});\s*\n', html, re.DOTALL)
if match:
    data = json.loads(match.group(1))
    print(f'Valid JSON data with {len(data)} sections')
    for k in sorted(data.keys()):
        title = data[k]["title"]
        print(f'  {k}: {title}')
else:
    print('Could not find embedded data')

print(f'\nFile size: {len(html):,} bytes')
print('All checks passed!')
