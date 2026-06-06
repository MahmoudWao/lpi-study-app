"""Kokoro TTS server - OpenAI-compatible API on port 8880"""
import io
import asyncio
from fastapi import FastAPI
from fastapi.responses import Response, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

kokoro = None

async def get_kokoro():
    global kokoro
    if kokoro is None:
        from kokoro_onnx import Kokoro
        kokoro = Kokoro("kokoro-v1.0.onnx", "voices-v1.0.bin")
    return kokoro

class SpeechRequest(BaseModel):
    model: str = "kokoro"
    input: str
    voice: str = "af_heart"
    speed: float = 1.0
    response_format: str = "wav"

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/v1/audio/voices")
async def voices():
    try:
        k = await get_kokoro()
        return k.get_voices()
    except Exception:
        return ["af_heart", "af_bella", "am_adam", "am_michael"]

@app.post("/v1/audio/speech")
async def speech(req: SpeechRequest):
    k = await get_kokoro()
    samples, sr = await asyncio.to_thread(k.create, req.input, voice=req.voice, speed=req.speed)
    
    buf = io.BytesIO()
    import soundfile as sf
    sf.write(buf, samples, sr, format="WAV")
    buf.seek(0)
    return Response(content=buf.read(), media_type="audio/wav")

if __name__ == "__main__":
    import uvicorn
    print("Starting Kokoro TTS server on http://localhost:8880")
    print("First request will download the model (~300MB)...")
    uvicorn.run(app, host="0.0.0.0", port=8880)
