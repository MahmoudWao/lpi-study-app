"""Local Piper TTS server for the LPI study app."""
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import subprocess, tempfile, os, io

app = Flask(__name__)
CORS(app)

MODEL = os.path.join(os.path.dirname(__file__), "tts", "en_US-amy-medium.onnx")

@app.route("/tts", methods=["POST"])
def synthesize():
    text = request.json.get("text", "")
    if not text:
        return jsonify({"error": "no text"}), 400
    # Limit to prevent huge requests
    text = text[:5000]
    # Run piper
    proc = subprocess.run(
        ["piper", "--model", MODEL, "--output-raw"],
        input=text.encode("utf-8"),
        capture_output=True
    )
    if proc.returncode != 0:
        return jsonify({"error": proc.stderr.decode()[:200]}), 500
    # Convert raw PCM to WAV
    import wave
    buf = io.BytesIO()
    with wave.open(buf, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(22050)
        wf.writeframes(proc.stdout)
    buf.seek(0)
    return send_file(buf, mimetype="audio/wav")

@app.route("/health")
def health():
    return jsonify({"status": "ok", "model": "en_US-amy-medium"})

if __name__ == "__main__":
    import socket
    ip = socket.gethostbyname(socket.gethostname())
    print(f"🔊 Piper TTS server starting on http://{ip}:5111")
    print(f"   Also available at http://localhost:5111")
    print(f"   Model: {MODEL}")
    app.run(host="0.0.0.0", port=5111)
