"""Patch ebook TTS with Piper support and Chrome workaround."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\Users\miikharo\lpi-study-app\ebook_template.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find TTS block
start = None
end = None
for i, line in enumerate(lines):
    if '// Text-to-speech' in line:
        start = i
    if start and "if(localStorage.getItem('lpi_ebook_dark')" in line:
        end = i
        break

new_tts = '''// Text-to-speech (Piper + browser fallback)
let ttsActive=false;
let ttsAudio=null;
let ebookChunks=[];
let ebookChunkIdx=0;
let ebookInterval=null;

async function toggleTTS(){
  if(ttsActive){stopTTS();return}
  const el=document.getElementById('content');if(!el)return;
  const text=(el.textContent||el.innerText).substring(0,5000).trim();
  if(!text)return;
  ttsActive=true;
  document.getElementById('ttsBtn').textContent='\\u23F9\\uFE0F';
  // Try Piper
  try{
    const r=await fetch('http://localhost:5111/health',{signal:AbortSignal.timeout(1000)});
    if(r.ok){
      const resp=await fetch('http://localhost:5111/tts',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text})});
      if(resp.ok){const blob=await resp.blob();ttsAudio=new Audio(URL.createObjectURL(blob));ttsAudio.onended=()=>stopTTS();ttsAudio.play();return}
    }
  }catch(e){}
  // Browser TTS
  const synth=window.speechSynthesis;synth.cancel();
  ebookChunks=text.match(/.{1,200}(?:[.!?]\\s|$)|.{1,200}(?:\\s|$)/g)||[text];
  ebookChunkIdx=0;
  speakEbookChunk();
}
function speakEbookChunk(){
  if(ebookChunkIdx>=ebookChunks.length){stopTTS();return}
  const synth=window.speechSynthesis;synth.cancel();
  const u=new SpeechSynthesisUtterance(ebookChunks[ebookChunkIdx]);
  u.lang='en-US';u.rate=0.9;
  u.onend=()=>{ebookChunkIdx++;if(ttsActive)speakEbookChunk()};
  u.onerror=()=>stopTTS();
  synth.speak(u);
  clearInterval(ebookInterval);
  ebookInterval=setInterval(()=>{if(synth.speaking)synth.resume()},8000);
}
function stopTTS(){
  if(ttsAudio){ttsAudio.pause();ttsAudio=null}
  speechSynthesis.cancel();clearInterval(ebookInterval);
  ttsActive=false;document.getElementById('ttsBtn').textContent='\\u{1F50A}';
}

'''

lines[start:end] = [new_tts]

with open(r'C:\Users\miikharo\lpi-study-app\ebook_template.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Ebook TTS patched with Piper + browser fallback + Chrome workaround")
