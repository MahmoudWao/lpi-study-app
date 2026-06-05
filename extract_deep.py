"""
Deep extraction of LPI Linux Essentials PDF content.
Extracts: lesson text, key concepts, definitions, exercises, answers, and summaries.
"""
import PyPDF2, json, sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

reader = PyPDF2.PdfReader(r'C:\Users\miikharo\Downloads\LPI Study.pdf .pdf')
all_pages = [reader.pages[i].extract_text() for i in range(len(reader.pages))]
print(f"Loaded {len(all_pages)} pages")

def clean(text):
    """Remove LPI headers/footers noise."""
    text = re.sub(r'Linux Essentials \(Version 1\.6\)[^\n]*', '', text)
    text = re.sub(r'Version: \d{4}-\d{2}-\d{2}[^\n]*', '', text)
    text = re.sub(r'\d+\s*[|│]\s*\n?\s*learning\.lpi\.org[^\n]*', '', text)
    text = re.sub(r'learning\.lpi\.org[^\n]*', '', text)
    text = re.sub(r'Licensed under CC BY-NC-ND[^\n]*', '', text)
    text = re.sub(r'[|│]\s*\d+', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

# Section page ranges (0-indexed) based on analysis of the PDF structure
# Each section has: objective page, lesson pages, exercise pages, answer pages, summary page
sections = {
    '1.1': {'title': 'Linux Evolution and Popular Operating Systems',
            'lesson_pages': list(range(11, 17)), 'ex_pages': [16, 17], 'ans_pages': [19, 20, 21], 'summary_pages': [18]},
    '1.2': {'title': 'Major Open Source Applications',
            'lesson_pages': list(range(23, 37)), 'ex_pages': [37, 38], 'ans_pages': [41, 42, 43], 'summary_pages': [40]},
    '1.3': {'title': 'Open Source Software and Licensing',
            'lesson_pages': list(range(44, 54)), 'ex_pages': [54, 55], 'ans_pages': [57, 58, 59], 'summary_pages': [56]},
    '1.4': {'title': 'ICT Skills and Working in Linux',
            'lesson_pages': list(range(61, 71)), 'ex_pages': [71, 72], 'ans_pages': [75, 76, 77], 'summary_pages': [74]},
    '2.1': {'title': 'Command Line Basics',
            'lesson_pages': list(range(79, 87)) + list(range(93, 99)), 'ex_pages': [87, 88, 99, 100], 'ans_pages': [91, 92, 102, 103], 'summary_pages': [90, 101]},
    '2.2': {'title': 'Using the Command Line to Get Help',
            'lesson_pages': list(range(105, 112)), 'ex_pages': [112, 113], 'ans_pages': [116, 117], 'summary_pages': [115]},
    '2.3': {'title': 'Using Directories and Listing Files',
            'lesson_pages': list(range(119, 127)) + list(range(133, 143)), 'ex_pages': [127, 128, 143, 144], 'ans_pages': [131, 132, 147, 148], 'summary_pages': [130, 146]},
    '2.4': {'title': 'Creating, Moving and Deleting Files',
            'lesson_pages': list(range(150, 166)), 'ex_pages': [166, 167], 'ans_pages': [171, 172, 173], 'summary_pages': [169]},
    '3.1': {'title': 'Archiving Files on the Command Line',
            'lesson_pages': list(range(175, 187)), 'ex_pages': [187, 188], 'ans_pages': [191, 192], 'summary_pages': [189]},
    '3.2': {'title': 'Searching and Extracting Data from Files',
            'lesson_pages': list(range(194, 202)) + list(range(207, 213)), 'ex_pages': [202, 203, 213, 214], 'ans_pages': [205, 206, 216, 217], 'summary_pages': [204, 215]},
    '3.3': {'title': 'Turning Commands into a Script',
            'lesson_pages': list(range(219, 232)) + list(range(239, 250)), 'ex_pages': [232, 233, 250, 251], 'ans_pages': [237, 238, 254, 255], 'summary_pages': [236, 253]},
    '4.1': {'title': 'Choosing an Operating System',
            'lesson_pages': list(range(257, 266)), 'ex_pages': [266, 267], 'ans_pages': [270, 271], 'summary_pages': [269]},
    '4.2': {'title': 'Understanding Computer Hardware',
            'lesson_pages': list(range(272, 284)), 'ex_pages': [284, 285], 'ans_pages': [287, 288], 'summary_pages': [286]},
    '4.3': {'title': 'Where Data is Stored',
            'lesson_pages': list(range(290, 303)) + list(range(310, 321)), 'ex_pages': [303, 304, 321, 322], 'ans_pages': [308, 309, 328, 329], 'summary_pages': [307, 327]},
    '4.4': {'title': 'Your Computer on the Network',
            'lesson_pages': list(range(331, 348)), 'ex_pages': [348, 349], 'ans_pages': [351, 352, 353], 'summary_pages': [350]},
    '5.1': {'title': 'Basic Security and Identifying User Types',
            'lesson_pages': list(range(355, 370)), 'ex_pages': [370, 371], 'ans_pages': [375, 376], 'summary_pages': [374]},
    '5.2': {'title': 'Creating Users and Groups',
            'lesson_pages': list(range(377, 389)), 'ex_pages': [389, 390], 'ans_pages': [393, 394], 'summary_pages': [392]},
    '5.3': {'title': 'Managing File Permissions and Ownership',
            'lesson_pages': list(range(396, 413)), 'ex_pages': [413, 414], 'ans_pages': [417, 418, 419], 'summary_pages': [416]},
    '5.4': {'title': 'Special Directories and Files',
            'lesson_pages': list(range(420, 431)), 'ex_pages': [431, 432], 'ans_pages': [436, 437, 438], 'summary_pages': [435]},
}

TOPICS = {
    '1': 'The Linux Community and a Career in Open Source',
    '2': 'Finding Your Way on a Linux System',
    '3': 'The Power of the Command Line',
    '4': 'The Linux Operating System',
    '5': 'Security and File Permissions'
}

output = {}
for sec_id, info in sections.items():
    topic_num = sec_id.split('.')[0]
    
    # Extract lesson content
    lesson_text = ''
    for p in info['lesson_pages']:
        if p < len(all_pages):
            lesson_text += all_pages[p] + '\n'
    lesson_text = clean(lesson_text)
    
    # Extract exercises
    ex_text = ''
    for p in info['ex_pages']:
        if p < len(all_pages):
            ex_text += all_pages[p] + '\n'
    ex_text = clean(ex_text)
    
    # Extract answers
    ans_text = ''
    for p in info['ans_pages']:
        if p < len(all_pages):
            ans_text += all_pages[p] + '\n'
    ans_text = clean(ans_text)
    
    # Extract summary
    summary_text = ''
    for p in info['summary_pages']:
        if p < len(all_pages):
            summary_text += all_pages[p] + '\n'
    summary_text = clean(summary_text)
    
    output[sec_id] = {
        'title': info['title'],
        'topic': TOPICS[topic_num],
        'topic_num': topic_num,
        'lesson': lesson_text,
        'exercises': ex_text,
        'answers': ans_text,
        'summary': summary_text
    }

with open(r'C:\Users\miikharo\lpi-study-app\deep_content.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"\nExtracted {len(output)} sections with deep content:")
for k, v in output.items():
    print(f"  {k}: {v['title']}")
    print(f"      Lesson: {len(v['lesson']):,} chars | Exercises: {len(v['exercises']):,} | Answers: {len(v['answers']):,} | Summary: {len(v['summary']):,}")
