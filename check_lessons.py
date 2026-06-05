import json,sys,io
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
with open(r'C:\Users\miikharo\lpi-study-app\structured_data.json','r',encoding='utf-8') as f:
    data=json.load(f)

for sec_id in ['1.1','2.1','3.1','4.4','5.3']:
    sec=data[sec_id]
    lesson=sec.get('full_lesson','') or sec.get('lesson_excerpt','')
    title = sec['title']
    print(f'=== {sec_id}: {title} ({len(lesson)} chars) ===')
    # Show first 600 chars
    print(lesson[:600])
    print('...')
    # Check for common issues
    issues = []
    if len(lesson) < 500:
        issues.append('TOO SHORT')
    if '\x00' in lesson:
        issues.append('NULL BYTES')
    if lesson.count('  ') > 50:
        issues.append('EXCESSIVE WHITESPACE')
    # Check for LPI noise that should have been cleaned
    noise_count = lesson.count('learning.lpi.org') + lesson.count('Licensed under CC')
    if noise_count > 0:
        issues.append(f'LPI NOISE ({noise_count} occurrences)')
    # Check for garbled text
    if lesson.count('???') > 3 or lesson.count('\ufffd') > 3:
        issues.append('GARBLED CHARS')
    if issues:
        print(f'  ISSUES: {", ".join(issues)}')
    print()
