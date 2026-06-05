"""
Build structured learning data from deep PDF content.
Creates problem-first cards, concept explanations, and multi-level questions.
"""
import json, sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\Users\miikharo\lpi-study-app\deep_content.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def extract_key_concepts(lesson_text):
    """Extract key terms and their definitions/context from lesson text."""
    concepts = []
    lines = lesson_text.split('\n')
    for i, line in enumerate(lines):
        # Look for definition patterns: term followed by explanation
        # Pattern: "A Linux distribution is a bundle..."
        m = re.match(r'^(?:A |An |The )?(\w[\w\s]{2,30}?)(?:\s+is\s+|\s+are\s+|\s+refers to\s+|\s+means\s+)(.{30,200})', line)
        if m:
            term = m.group(1).strip()
            definition = m.group(2).strip()
            if len(term) > 3 and not term[0].islower():
                concepts.append({'term': term, 'definition': line.strip()})
        # Look for bullet-point definitions
        if line.startswith('•') or line.startswith('◦'):
            content = line.lstrip('•◦ ').strip()
            if len(content) > 20 and ':' in content[:60]:
                parts = content.split(':', 1)
                if len(parts[0]) < 40 and len(parts[1]) > 15:
                    concepts.append({'term': parts[0].strip(), 'definition': parts[1].strip()})
    return concepts[:15]  # Limit per section

def extract_commands(lesson_text):
    """Extract command examples from lesson text."""
    commands = []
    lines = lesson_text.split('\n')
    for i, line in enumerate(lines):
        # Look for $ command patterns
        if line.strip().startswith('$ '):
            cmd = line.strip()[2:].strip()
            # Get context from surrounding lines
            context = ''
            for j in range(max(0, i-3), i):
                if lines[j].strip() and not lines[j].strip().startswith('$'):
                    context = lines[j].strip()
            if len(cmd) > 2 and len(cmd) < 100:
                commands.append({'command': cmd, 'context': context})
    return commands[:20]

def parse_exercises(ex_text, ans_text):
    """Parse exercises and their answers into Q&A pairs."""
    # Split on numbered items
    questions = re.split(r'\n(?=\d+\.)', ex_text)
    answers = re.split(r'\n(?=\d+\.)', ans_text)
    
    pairs = []
    for q in questions:
        q = q.strip()
        if not re.match(r'^\d+\.', q):
            continue
        num_match = re.match(r'^(\d+)\.', q)
        if not num_match:
            continue
        num = num_match.group(1)
        question = re.sub(r'^\d+\.', '', q).strip()
        
        # Find matching answer
        answer = ''
        for a in answers:
            a = a.strip()
            if re.match(rf'^{num}\.', a):
                answer = re.sub(r'^\d+\.', '', a).strip()
                break
        
        if question and len(question) > 10:
            # Determine difficulty based on question complexity
            difficulty = 'basic'
            if any(w in question.lower() for w in ['explain', 'describe', 'why', 'compare', 'analyze']):
                difficulty = 'advanced'
            elif any(w in question.lower() for w in ['what command', 'which', 'name', 'list']):
                difficulty = 'intermediate'
            
            pairs.append({
                'question': question,
                'answer': answer if answer else 'See lesson material for answer.',
                'difficulty': difficulty
            })
    return pairs

def extract_paragraph_concepts(lesson_text):
    """Extract important paragraphs that explain key ideas."""
    paragraphs = lesson_text.split('\n\n')
    explanations = []
    for p in paragraphs:
        p = p.strip()
        # Look for explanatory paragraphs (not commands, not too short)
        if (len(p) > 100 and len(p) < 800 and 
            not p.startswith('$') and 
            not p.startswith('#') and
            any(w in p.lower() for w in ['is used', 'allows', 'provides', 'enables', 'means', 'refers', 'important', 'note that', 'remember'])):
            explanations.append(p)
    return explanations[:8]

# Build the final structured data
structured = {}
for sec_id, sec in data.items():
    concepts = extract_key_concepts(sec['lesson'])
    commands = extract_commands(sec['lesson'])
    qa_pairs = parse_exercises(sec['exercises'], sec['answers'])
    explanations = extract_paragraph_concepts(sec['lesson'])
    
    structured[sec_id] = {
        'title': sec['title'],
        'topic': sec['topic'],
        'topic_num': sec['topic_num'],
        'concepts': concepts,
        'commands': commands,
        'qa_pairs': qa_pairs,
        'explanations': explanations,
        'summary': sec['summary'],
        'lesson_excerpt': sec['lesson'][:3000],  # First part for reading mode
        'full_lesson': sec['lesson']
    }

with open(r'C:\Users\miikharo\lpi-study-app\structured_data.json', 'w', encoding='utf-8') as f:
    json.dump(structured, f, indent=2, ensure_ascii=False)

print(f"Built structured data for {len(structured)} sections:")
total_cards = 0
for k, v in structured.items():
    n_concepts = len(v['concepts'])
    n_commands = len(v['commands'])
    n_qa = len(v['qa_pairs'])
    n_explain = len(v['explanations'])
    section_cards = n_concepts + n_commands + n_qa
    total_cards += section_cards
    print(f"  {k}: {v['title']}")
    print(f"      Concepts: {n_concepts} | Commands: {n_commands} | Q&A: {n_qa} | Explanations: {n_explain}")

print(f"\nTotal study cards: {total_cards}")
