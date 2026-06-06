"""Add text highlighting that follows TTS playback."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\Users\miikharo\lpi-study-app\app_template.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add highlight CSS
highlight_css = """
.tts-highlight{background:var(--highlight,#fffbeb);border-radius:3px;transition:background 0.2s}
.dark .tts-highlight{background:#3a3a5a}
"""
content = content.replace('</style>', highlight_css + '</style>')

# 2. Replace speakChunk to highlight current chunk
old_speak = """function speakChunk(){
  if(ttsChunkIdx>=ttsChunks.length){stopLessonTTS();return}
  const synth=window.speechSynthesis;synth.cancel();
  const u=new SpeechSynthesisUtterance(ttsChunks[ttsChunkIdx]);
  u.lang='en-US';u.rate=0.9;
  u.onend=()=>{ttsChunkIdx++;updateTTSProgress();if(lessonTtsActive)speakChunk()};
  u.onerror=()=>stopLessonTTS();
  synth.speak(u);updateTTSProgress();
  clearInterval(ttsInterval);
  ttsInterval=setInterval(()=>{if(synth.speaking)synth.resume()},8000);
}"""

new_speak = """function speakChunk(){
  if(ttsChunkIdx>=ttsChunks.length){stopLessonTTS();return}
  const synth=window.speechSynthesis;synth.cancel();
  highlightChunk(ttsChunkIdx);
  const u=new SpeechSynthesisUtterance(ttsChunks[ttsChunkIdx]);
  u.lang='en-US';u.rate=0.9;
  u.onend=()=>{ttsChunkIdx++;updateTTSProgress();if(lessonTtsActive)speakChunk()};
  u.onerror=()=>stopLessonTTS();
  synth.speak(u);updateTTSProgress();
  clearInterval(ttsInterval);
  ttsInterval=setInterval(()=>{if(synth.speaking)synth.resume()},8000);
}

function highlightChunk(idx){
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
}"""

content = content.replace(old_speak, new_speak)

# 3. Also highlight during Piper audio playback using timeupdate
old_piper_timeupdate = """ttsAudio.ontimeupdate=()=>{
          const seek=document.getElementById('ttsSeek');
          const time=document.getElementById('ttsTime');
          if(seek&&ttsAudio.duration){seek.value=Math.round((ttsAudio.currentTime/ttsAudio.duration)*100);
            time.textContent=fmtTime(Math.round(ttsAudio.currentTime))+' / '+fmtTime(Math.round(ttsAudio.duration))}
        };"""

new_piper_timeupdate = """ttsAudio.ontimeupdate=()=>{
          const seek=document.getElementById('ttsSeek');
          const time=document.getElementById('ttsTime');
          if(seek&&ttsAudio.duration){
            const pct=ttsAudio.currentTime/ttsAudio.duration;
            seek.value=Math.round(pct*100);
            time.textContent=fmtTime(Math.round(ttsAudio.currentTime))+' / '+fmtTime(Math.round(ttsAudio.duration));
            const chunkIdx=Math.floor(pct*Math.ceil(text.length/TTS_CHUNK_SIZE));
            highlightChunk(chunkIdx);
          }
        };"""

content = content.replace(old_piper_timeupdate, new_piper_timeupdate)

# 4. Clear highlights on stop
old_stop = """function stopLessonTTS(){
  if(ttsAudio){ttsAudio.pause();ttsAudio=null}
  speechSynthesis.cancel();clearInterval(ttsInterval);
  lessonTtsActive=false;
  const b=document.getElementById('lessonTtsBtn');if(b)b.innerHTML='&#x1F50A; Read Aloud';
  const prog=document.getElementById('ttsProgress');if(prog)prog.style.display='none';
}"""

new_stop = """function stopLessonTTS(){
  if(ttsAudio){ttsAudio.pause();ttsAudio=null}
  speechSynthesis.cancel();clearInterval(ttsInterval);
  lessonTtsActive=false;
  const b=document.getElementById('lessonTtsBtn');if(b)b.innerHTML='&#x1F50A; Read Aloud';
  const prog=document.getElementById('ttsProgress');if(prog)prog.style.display='none';
  const el=document.getElementById('lessonText');
  if(el){const hl=el.querySelectorAll('.tts-highlight');hl.forEach(s=>{s.outerHTML=s.textContent})}
}"""

content = content.replace(old_stop, new_stop)

with open(r'C:\Users\miikharo\lpi-study-app\app_template.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Added text highlighting during TTS playback")
print("  - Current chunk highlighted in yellow")
print("  - Auto-scrolls to highlighted section")
print("  - Highlights cleared on stop")
print("  - Works with both Piper and browser TTS")
