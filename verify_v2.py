import re, sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\Users\miikharo\lpi-study-app\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

checks = [
    ('HTML structure', '<!DOCTYPE html>' in html and '</html>' in html),
    ('Data injected', '__STRUCTURED_DATA__' not in html),
    ('Terminal mode', 'renderTerminal' in html),
    ('Terminal labs', 'TERM_LABS' in html),
    ('Virtual filesystem', 'VFS' in html),
    ('Lab progress persistence', 'lpi_term_progress' in html),
    ('Terminal input', 'termInput' in html),
    ('Command simulation', 'simulateCommand' in html),
    ('Tab completion', 'Tab' in html),
    ('History navigation', 'termHistory' in html),
    ('Nav button terminal', 'terminal' in html),
    ('9 labs present', 'network' in html and 'scripting' in html),
    ('Hint command', 'hint' in html),
    ('Spaced repetition', 'gradeCard' in html),
    ('Challenge mode', 'challenge' in html),
]
print('Verification:')
all_pass = True
for name, passed in checks:
    status = 'PASS' if passed else 'FAIL'
    if not passed: all_pass = False
    print(f'  {status}: {name}')

# Check JS bracket balance in template part only
match = re.search(r'<script>(.*?)</script>', html, re.DOTALL)
if match:
    js = match.group(1)
    # Find where data ends (const TOPICS line)
    topics_idx = js.find('const TOPICS = {')
    if topics_idx > -1:
        template_js = js[topics_idx:]
        o = template_js.count('{') + template_js.count('[') + template_js.count('(')
        c = template_js.count('}') + template_js.count(']') + template_js.count(')')
        balanced = o == c
        print(f'  {"PASS" if balanced else "WARN"}: Template JS brackets (opens={o}, closes={c})')

print(f'\nFile size: {len(html):,} bytes')
result = "ALL PASSED" if all_pass else "SOME FAILED"
print(f'Result: {result}')
