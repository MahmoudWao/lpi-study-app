"""Build the LPI Linux Essentials Study App from extracted PDF data."""
import json, sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\Users\miikharo\lpi_raw_content.json', 'r', encoding='utf-8') as f:
    content = json.load(f)

with open(r'C:\Users\miikharo\lpi_summaries.json', 'r', encoding='utf-8') as f:
    summaries = json.load(f)

# Build structured quiz data from the extracted exercises and answers
quiz_data = {}
topics = {
    '1': 'The Linux Community and a Career in Open Source',
    '2': 'Finding Your Way on a Linux System',
    '3': 'The Power of the Command Line',
    '4': 'The Linux Operating System',
    '5': 'Security and File Permissions'
}

for sec_id, sec_content in content.items():
    topic_num = sec_id.split('.')[0]
    # Clean the exercise text - remove footer/header noise
    ex_text = sec_content['exercises']
    ans_text = sec_content['answers']

    # Remove LPI footer/header lines
    noise_pattern = r'Linux Essentials \(Version 1\.6\).*?\n.*?\n.*?\n'
    ex_text = re.sub(noise_pattern, '', ex_text)
    ans_text = re.sub(noise_pattern, '', ans_text)

    quiz_data[sec_id] = {
        'title': sec_content['title'],
        'topic': topics[topic_num],
        'topic_num': topic_num,
        'exercises': ex_text.strip(),
        'answers': ans_text.strip(),
        'summary': summaries.get(sec_id, '')
    }

# Clean summaries too
for sec_id in quiz_data:
    noise_pattern = r'Linux Essentials \(Version 1\.6\).*?\n.*?\n.*?\n'
    quiz_data[sec_id]['summary'] = re.sub(noise_pattern, '', quiz_data[sec_id]['summary'])

# Save as JSON for embedding
with open(r'C:\Users\miikharo\lpi-study-app\quiz_data.json', 'w', encoding='utf-8') as f:
    json.dump(quiz_data, f, indent=2, ensure_ascii=False)

print(f"Built quiz data: {len(quiz_data)} sections")
for k, v in quiz_data.items():
    print(f"  {k}: {v['title']}")
