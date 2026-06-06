"""Replace TTS code with Piper-enabled version."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\Users\miikharo\lpi-study-app\app_template.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find start and end of TTS block
start = None
end = None
for i, line in enumerate(lines):
    if '// Lesson TTS with progress' in line:
        start = i
    if start and 'updateStreak();render();' in line:
        end = i
        break

if not start or not end:
    print("ERROR: Could not find TTS block")
    sys.exit(1)

new_tts = '''// Lesson TTS (Piper neural voice with browser fallback)
let lessonTtsActive=false;
let ttsChunks=[];
let ttsChunkIdx=0;
let ttsInterval=null;
let ttsEstTotal=0;
let ttsAudio=null;
const TTS_CHUNK_SIZE=200;
const TTS_SERVER='http://localhost:5111/tts';

async function checkTTSServer(){try{const r=await fetch('http://localhost:5111/health');return r.ok}catch(e){return false}}

async function toggleLessonTTS(){
  if(lessonTtsActive){stopLessonTTS();return}
  const el=document.getElementById('lessonText');
  if(!el)return;
  const text=(el.textContent||el.innerText).substring(0,5000).trim();
  if(!text)return;
  lessonTtsActive=true;
  const b=document.getElementById('lessonTtsBtn');if(b)b.innerHTML='&#x23F9;&#xFE0F; Stop';
  const prog=document.getElementById('ttsProgress');if(prog)prog.style.display='flex';
  // Try Piper server first
  const serverUp=await checkTTSServer();
  if(serverUp){
    try{
      const resp=await fetch(TTS_SERVER,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text})});
      if(resp.ok){
        const blob=await resp.blob();
        const url=URL.createObjectURL(blob);
        ttsAudio=new Audio(url);
        ttsAudio.onended=()=>stopLessonTTS();
        ttsAudio.ontimeupdate=()=>{
          const seek=document.getElementById('ttsSeek');
          const time=document.getElementById('ttsTime');
          if(seek&&ttsAudio.duration){seek.value=Math.round((ttsAudio.currentTime/ttsAudio.duration)*100);
            time.textContent=fmtTime(Math.round(ttsAudio.currentTime))+' / '+fmtTime(Math.round(ttsAudio.duration))}
        };
        ttsAudio.play();
        return;
      }
    }catch(e){console.log('Piper unavailable, using browser TTS')}
  }
  // Fallback: browser TTS
  const synth=window.speechSynthesis;synth.cancel();
  ttsChunks=[];
  for(let i=0;i<text.length;i+=TTS_CHUNK_SIZE)ttsChunks.push(text.substring(i,i+TTS_CHUNK_SIZE));
  ttsChunkIdx=0;
  speakChunk();
}

function speakChunk(){
  if(ttsChunkIdx>=ttsChunks.length){stopLessonTTS();return}
  const synth=window.speechSynthesis;synth.cancel();
  const u=new SpeechSynthesisUtterance(ttsChunks[ttsChunkIdx]);
  u.lang='en-US';u.rate=0.9;
  u.onend=()=>{ttsChunkIdx++;updateTTSProgress();if(lessonTtsActive)speakChunk()};
  u.onerror=()=>stopLessonTTS();
  synth.speak(u);updateTTSProgress();
  clearInterval(ttsInterval);
  ttsInterval=setInterval(()=>{if(synth.speaking)synth.resume()},8000);
}

function updateTTSProgress(){
  const seek=document.getElementById('ttsSeek');const time=document.getElementById('ttsTime');
  if(!seek||!time)return;
  const pct=ttsChunks.length?Math.round((ttsChunkIdx/ttsChunks.length)*100):0;
  seek.value=pct;
  ttsEstTotal=Math.round(ttsChunks.length*TTS_CHUNK_SIZE/5/150*60/0.9);
  time.textContent=fmtTime(Math.round(ttsChunkIdx*TTS_CHUNK_SIZE/5/150*60/0.9))+' / '+fmtTime(ttsEstTotal);
}

function fmtTime(s){return Math.floor(s/60)+':'+String(Math.round(s)%60).padStart(2,'0')}

function seekTTS(val){
  if(ttsAudio){ttsAudio.currentTime=(parseInt(val)/100)*ttsAudio.duration;return}
  ttsChunkIdx=Math.floor((parseInt(val)/100)*ttsChunks.length);
  if(lessonTtsActive)speakChunk();
}

function stopLessonTTS(){
  if(ttsAudio){ttsAudio.pause();ttsAudio=null}
  speechSynthesis.cancel();clearInterval(ttsInterval);
  lessonTtsActive=false;
  const b=document.getElementById('lessonTtsBtn');if(b)b.innerHTML='&#x1F50A; Read Aloud';
  const prog=document.getElementById('ttsProgress');if(prog)prog.style.display='none';
}

'''

# Replace
lines[start:end] = [new_tts]

with open(r'C:\Users\miikharo\lpi-study-app\app_template.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f"Replaced TTS block (lines {start}-{end}) with Piper-enabled version")
