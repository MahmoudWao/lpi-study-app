"""Verify the rebuilt study app is valid and functional."""
import json, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\Users\miikharo\lpi-study-app\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

errors = []

# Basic HTML structure
if '<!DOCTYPE html>' not in html: errors.append('Missing DOCTYPE')
if '</html>' not in html: errors.append('Missing closing html tag')
if '__STRUCTURED_DATA__' in html: errors.append('Data placeholder not replaced')

# Check data is valid JSON
match = re.search(r'const DATA = ({.*?});\s*\nconst TOPICS', html, re.DOTALL)
if not match:
    errors.append('Could not find embedded DATA')
else:
    try:
        data = json.loads(match.group(1))
        print(f"✓ Valid JSON with {len(data)} sections")
        for k in sorted(data.keys()):
            sec = data[k]
            print(f"  {k}: {sec['title']} — {len(sec['qa_pairs'])} Q&A, {len(sec['commands'])} cmds, {len(sec['concepts'])} concepts")
    except json.JSONDecodeError as e:
        errors.append(f'Invalid JSON: {e}')

# Check key features exist
features = [
    ('Spaced repetition', 'gradeCard'),
    ('Self-grading', 'grade-btn'),
    ('Challenge mode', 'challenge'),
    ('Flashcards', 'fc-container'),
    ('Progress tracking', 'localStorage'),
    ('Streak tracking', 'streak'),
    ('Mastery levels', 'mastery'),
    ('Problem-first', 'Problem-first'),
    ('Hint system', 'hintBtn'),
    ('Keyboard nav', 'keydown'),
    ('Topic filtering', 'topicFilter'),
    ('SM-2 algorithm', 'ease'),
]
print(f"\n✓ Feature check:")
for name, keyword in features:
    if keyword in html:
        print(f"  ✓ {name}")
    else:
        errors.append(f'Missing feature: {name}')

# Check bracket balance in script
script_match = re.search(r'<script>(.*?)</script>', html, re.DOTALL)
if script_match:
    js = script_match.group(1)
    opens = js.count('{') + js.count('[') + js.count('(')
    closes = js.count('}') + js.count(']') + js.count(')')
    if opens == closes:
        print(f"\n✓ JS bracket balance: OK ({opens} pairs)")
    else:
        errors.append(f'Bracket imbalance: {opens} opens, {closes} closes (diff: {opens-closes})')

print(f"\nFile size: {len(html):,} bytes")

if errors:
    print(f"\n✗ ERRORS ({len(errors)}):")
    for e in errors:
        print(f"  - {e}")
else:
    print("\n✓ ALL CHECKS PASSED")
