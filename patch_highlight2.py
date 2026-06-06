"""Fix highlighting: use pre-wrapped spans instead of TreeWalker."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\Users\miikharo\lpi-study-app\app_template.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find and replace the formatLesson function to wrap chunks in spans
# Also replace highlightChunk to just toggle classes

# 1. Find formatLesson
fmt_start = None
fmt_end = None
for i, line in enumerate(lines):
    if 'function formatLesson(raw){' in line:
        fmt_start = i
    if fmt_start and i > fmt_start and line.strip().startswith('function ') and 'formatLesson' not in line:
        fmt_end = i
        break

new_format = '''function formatLesson(raw){
  let text=esc(raw);
  let paras=text.split(/\\n{2,}/);
  let html='';
  let chunkId=0;
  paras.forEach(p=>{
    p=p.trim();if(!p)return;
    if(/^(Introduction|Summary|Guided Exercises|Explorational Exercises)$/.test(p)){html+=`<h3 style="color:var(--primary);font-size:1rem;margin:1.5rem 0 0.5rem;font-family:-apple-system,sans-serif">${p}</h3>`;return}
    if(/^\\$ /.test(p)){html+=`<pre style="background:var(--card);padding:0.8rem 1rem;border-radius:8px;font-family:monospace;font-size:0.85rem;overflow-x:auto;margin:0.8rem 0;border:1px solid var(--border)">${p}</pre>`;return}
    if(/^[\\u2022\\u25E6]/.test(p)){
      const items=p.split(/\\n/).map(l=>l.replace(/^[\\u2022\\u25E6]\\s*/,'').trim()).filter(Boolean);
      html+=`<ul style="margin:0.8rem 0 0.8rem 1.2rem">${items.map(i=>`<li style="margin-bottom:0.3rem">${i}</li>`).join('')}</ul>`;return}
    // Wrap sentences in spans with data-chunk for highlighting
    const joined=p.replace(/\\n/g,' ').replace(/\\s{2,}/g,' ');
    // Split into ~200 char chunks at sentence boundaries
    const sentences=joined.match(/.{1,200}(?:[.!?]\\s|$)|.{1,200}(?:\\s|$)/g)||[joined];
    const spans=sentences.map(s=>`<span data-chunk="${chunkId++}">${s}</span>`).join('');
    html+=`<p style="margin-bottom:1rem">${spans}</p>`;
  });
  return html;
}
'''

lines[fmt_start:fmt_end] = [new_format]

# Now find and replace highlightChunk
content = ''.join(lines)

old_highlight = '''function highlightChunk(idx){
  const el=document.getElementById('lessonText');if(!el)return;
  // Get the full text and wrap current chunk in a highlight span
  const text=el.textContent||el.innerText;
  const start=idx*TTS_CHUNK_SIZE;
  const end=Math.min(start+TTS_CHUNK_SIZE,text.length);
  // Find the chunk text in the HTML and scroll to it
  const spans=el.querySelectorAll('.tts-highlight');
  spans.forEach(s=>{s.outerHTML=s.textContent});
  // Use TreeWalker to find and highlight text node
  const range=document.createRange();
  const walker=document.createTreeWalker(el,NodeFilter.SHOW_TEXT);
  let charCount=0,found=false;
  while(walker.nextNode()){
    const node=walker.currentNode;
    const nodeLen=node.textContent.length;
    if(!found&&charCount+nodeLen>start){
      const localStart=start-charCount;
      const localEnd=Math.min(end-charCount,nodeLen);
      range.setStart(node,localStart);
      range.setEnd(node,localEnd);
      const span=document.createElement('span');
      span.className='tts-highlight';
      range.surroundContents(span);
      span.scrollIntoView({behavior:'smooth',block:'center'});
      found=true;
      break;
    }
    charCount+=nodeLen;
  }
}'''

new_highlight = '''function highlightChunk(idx){
  const el=document.getElementById('lessonText');if(!el)return;
  el.querySelectorAll('[data-chunk]').forEach(s=>s.classList.remove('tts-highlight'));
  const span=el.querySelector(`[data-chunk="${idx}"]`);
  if(span){span.classList.add('tts-highlight');span.scrollIntoView({behavior:'smooth',block:'center'})}
}'''

content = content.replace(old_highlight, new_highlight)

# Fix stopLessonTTS to just remove classes
old_clear = "if(el){const hl=el.querySelectorAll('.tts-highlight');hl.forEach(s=>{s.outerHTML=s.textContent})}"
new_clear = "if(el){el.querySelectorAll('.tts-highlight').forEach(s=>s.classList.remove('tts-highlight'))}"
content = content.replace(old_clear, new_clear)

# Also fix the chunk counting in speakChunk - use chunk spans count, not char-based
# The ttsChunks should map to data-chunk indices
old_split = """  ttsChunks=[];
  for(let i=0;i<text.length;i+=TTS_CHUNK_SIZE)ttsChunks.push(text.substring(i,i+TTS_CHUNK_SIZE));
  ttsChunkIdx=0;
  speakChunk();"""

new_split = """  // Build chunks matching the data-chunk spans in the rendered HTML
  const spans=document.querySelectorAll('#lessonText [data-chunk]');
  ttsChunks=Array.from(spans).map(s=>s.textContent);
  if(!ttsChunks.length){ttsChunks=[text];} // fallback
  ttsChunkIdx=0;
  speakChunk();"""

content = content.replace(old_split, new_split)

with open(r'C:\Users\miikharo\lpi-study-app\app_template.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed highlighting: uses pre-wrapped spans + class toggle")
