"""Clean up lesson content: strip metadata headers, fix whitespace, remove wrong-section content."""
import json, sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\Users\miikharo\lpi-study-app\structured_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def clean_lesson(text, section_title):
    # Remove metadata headers at the start
    text = re.sub(r'^.*?Introduction\n', 'Introduction\n', text, count=1, flags=re.DOTALL)
    # If no Introduction found, try to strip the LPI header block
    if text.startswith('Certificate:') or text.startswith('Reference to LPI'):
        # Find where actual content begins (after Key knowledge/Partial list blocks)
        m = re.search(r'\n(Introduction|[A-Z][a-z]+ [A-Z])', text[200:])
        if m:
            text = text[200 + m.start():]
    
    # Remove "Answers to" sections that leaked in
    ans_idx = text.find('Answers to Guided Exercises')
    if ans_idx > 0 and ans_idx < 500:
        # Content starts with answers from prev section - find real start
        # Look for the actual section intro after the answers
        m = re.search(r'\n\d+\.\d+ Lesson \d+\n|Topic \d+:', text[ans_idx:])
        if m:
            text = text[ans_idx + m.start():]
    
    ans_idx2 = text.find('Answers to Explorational')
    if ans_idx2 > 0 and ans_idx2 < 500:
        m = re.search(r'\n[A-Z]', text[ans_idx2 + 30:])
        if m:
            text = text[ans_idx2 + 30 + m.start():]
    
    # Remove trailing exercise answers if they leaked in
    for marker in ['Answers to Guided Exercises', 'Answers to Explorational Exercises']:
        idx = text.rfind(marker)
        if idx > len(text) * 0.7:  # Only trim if in the last 30%
            text = text[:idx]
    
    # Clean excessive whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'  +', ' ', text)
    # Remove LPI page footers/headers that leaked through
    text = re.sub(r'\n\s*\d+\s*\|\s*\n', '\n', text)
    text = re.sub(r'\|\s*\d+\s*\n', '\n', text)
    
    # Trim to 5000 chars for the app (keeps it readable)
    if len(text) > 5000:
        text = text[:5000]
    
    return text.strip()

for sec_id, sec in data.items():
    lesson = sec.get('full_lesson', '') or sec.get('lesson_excerpt', '')
    if lesson:
        cleaned = clean_lesson(lesson, sec['title'])
        sec['full_lesson'] = cleaned
        sec['lesson_excerpt'] = cleaned[:3000]

with open(r'C:\Users\miikharo\lpi-study-app\structured_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

# Verify
print("Cleaned lessons:")
for sec_id in sorted(data.keys()):
    sec = data[sec_id]
    lesson = sec.get('full_lesson', '')
    title = sec['title']
    first_line = lesson.split('\n')[0][:80] if lesson else 'EMPTY'
    print(f"  {sec_id}: {title}")
    print(f"       Starts: {first_line}")
    print(f"       Length: {len(lesson)} chars")
