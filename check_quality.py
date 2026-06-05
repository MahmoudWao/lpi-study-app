import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\Users\miikharo\lpi-study-app\structured_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for sec_id in ['1.1', '2.1', '3.2', '5.3']:
    sec = data[sec_id]
    print(f'\n=== {sec_id}: {sec["title"]} ===')
    print('Concepts:')
    for c in sec['concepts'][:3]:
        t = c['term']
        d = c['definition'][:80]
        print(f'  - {t}: {d}...')
    print('Q&A:')
    for q in sec['qa_pairs'][:2]:
        qtext = q['question'][:80]
        atext = q['answer'][:80]
        print(f'  Q: {qtext}...')
        print(f'  A: {atext}...')
        print(f'  Difficulty: {q["difficulty"]}')
    if sec['commands']:
        print('Commands:')
        for cmd in sec['commands'][:3]:
            c = cmd['command']
            ctx = cmd['context'][:50]
            print(f'  $ {c} ({ctx})')
