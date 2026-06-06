"""Patch: make TTS server discoverable from mobile (try localhost + LAN IP)."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\Users\miikharo\lpi-study-app\app_template.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    "const TTS_SERVER='http://localhost:5111/tts';",
    """const TTS_ENDPOINTS=['http://localhost:5111','http://'+location.hostname+':5111'];
let TTS_SERVER=null;"""
)

content = content.replace(
    "async function checkTTSServer(){try{const r=await fetch('http://localhost:5111/health');return r.ok}catch(e){return false}}",
    """async function checkTTSServer(){
  for(const ep of TTS_ENDPOINTS){try{const r=await fetch(ep+'/health',{signal:AbortSignal.timeout(1000)});if(r.ok){TTS_SERVER=ep+'/tts';return true}}catch(e){}}
  return false;
}"""
)

with open(r'C:\Users\miikharo\lpi-study-app\app_template.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Patched: TTS now tries localhost + LAN IP for mobile support")
