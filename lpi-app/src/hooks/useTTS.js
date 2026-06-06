import { useState, useRef, useEffect, useCallback } from 'react';

const KOKORO_BASE = 'http://localhost:8880';
const CACHE_DB = 'lpi_tts_cache';
const MAX_CACHE_MB = 500;

async function openCache() {
  return new Promise((resolve, reject) => {
    const req = indexedDB.open(CACHE_DB, 1);
    req.onupgradeneeded = () => { const db = req.result; if (!db.objectStoreNames.contains('audio')) db.createObjectStore('audio', { keyPath: 'key' }); };
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}

async function getCached(key) {
  try {
    const db = await openCache();
    return new Promise((resolve) => {
      const tx = db.transaction('audio', 'readonly');
      const req = tx.objectStore('audio').get(key);
      req.onsuccess = () => resolve(req.result?.blob);
      req.onerror = () => resolve(null);
    });
  } catch { return null; }
}

async function putCache(key, blob) {
  try {
    const db = await openCache();
    const tx = db.transaction('audio', 'readwrite');
    const store = tx.objectStore('audio');
    store.put({ key, blob, ts: Date.now(), size: blob.size });
    // LRU eviction
    const all = [];
    const cursor = store.openCursor();
    cursor.onsuccess = () => {
      const c = cursor.result;
      if (c) { all.push(c.value); c.continue(); }
      else {
        let total = all.reduce((s, e) => s + e.size, 0);
        if (total > MAX_CACHE_MB * 1024 * 1024) {
          all.sort((a, b) => a.ts - b.ts);
          while (total > MAX_CACHE_MB * 1024 * 1024 * 0.8 && all.length) {
            const old = all.shift();
            store.delete(old.key);
            total -= old.size;
          }
        }
      }
    };
  } catch {}
}

export async function clearTTSCache() {
  try { const db = await openCache(); db.transaction('audio', 'readwrite').objectStore('audio').clear(); } catch {}
}

function hashText(text, voice, speed) {
  let h = 0;
  const s = `${text}|${voice}|${speed}`;
  for (let i = 0; i < s.length; i++) { h = ((h << 5) - h + s.charCodeAt(i)) | 0; }
  return 'tts_' + Math.abs(h).toString(36);
}

export function useTTS() {
  const [isPlaying, setIsPlaying] = useState(false);
  const [progress, setProgress] = useState(0);
  const [duration, setDuration] = useState(0);
  const [serverAvailable, setServerAvailable] = useState(null);
  const [voices, setVoices] = useState([]);
  const [voice, setVoice] = useState(() => localStorage.getItem('lpi_tts_voice') || 'af_heart');
  const [speed, setSpeed] = useState(() => parseFloat(localStorage.getItem('lpi_tts_speed') || '1'));
  const audioRef = useRef(null);
  const synthRef = useRef({ chunks: [], idx: 0, interval: null });
  const onChunkRef = useRef(null);

  // Health check on mount
  useEffect(() => {
    (async () => {
      try {
        const r = await fetch(KOKORO_BASE + '/health', { signal: AbortSignal.timeout(2000) });
        setServerAvailable(r.ok);
        if (r.ok) {
          try {
            const vr = await fetch(KOKORO_BASE + '/v1/audio/voices');
            if (vr.ok) { const data = await vr.json(); setVoices(Array.isArray(data) ? data : data.voices || []); }
          } catch {}
        }
      } catch { setServerAvailable(false); }
    })();
  }, []);

  // Persist preferences
  useEffect(() => { localStorage.setItem('lpi_tts_voice', voice); }, [voice]);
  useEffect(() => { localStorage.setItem('lpi_tts_speed', speed.toString()); }, [speed]);

  const speak = useCallback(async (text, onChunk) => {
    stop();
    onChunkRef.current = onChunk;

    if (serverAvailable) {
      const key = hashText(text, voice, speed);
      let blob = await getCached(key);
      if (!blob) {
        try {
          const resp = await fetch(KOKORO_BASE + '/v1/audio/speech', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ model: 'kokoro', input: text, voice, speed, response_format: 'mp3' })
          });
          if (resp.ok) { blob = await resp.blob(); putCache(key, blob); }
        } catch {}
      }
      if (blob) {
        const url = URL.createObjectURL(blob);
        const audio = new Audio(url);
        audioRef.current = audio;
        audio.onended = () => { setIsPlaying(false); setProgress(0); };
        audio.ontimeupdate = () => {
          if (audio.duration) {
            const pct = audio.currentTime / audio.duration;
            setProgress(pct);
            setDuration(audio.duration);
            if (onChunkRef.current) {
              const totalChunks = document.querySelectorAll('[data-chunk]').length || 1;
              onChunkRef.current(Math.floor(pct * totalChunks));
            }
          }
        };
        audio.playbackRate = 1; // speed already applied server-side
        audio.play();
        setIsPlaying(true);
        return;
      }
    }

    // Fallback: Web Speech
    const synth = window.speechSynthesis;
    synth.cancel();
    const chunks = text.match(/.{1,200}(?:[.!?]\s|$)|.{1,200}(?:\s|$)/g) || [text];
    synthRef.current = { chunks, idx: 0, interval: null };
    setIsPlaying(true);
    speakChunk();
  }, [serverAvailable, voice, speed]);

  function speakChunk() {
    const { chunks, idx } = synthRef.current;
    if (idx >= chunks.length) { stop(); return; }
    const synth = window.speechSynthesis;
    synth.cancel();
    if (onChunkRef.current) onChunkRef.current(idx);
    setProgress(chunks.length ? idx / chunks.length : 0);
    const u = new SpeechSynthesisUtterance(chunks[idx]);
    u.lang = 'en-US';
    u.rate = speed;
    u.onend = () => { synthRef.current.idx++; if (isPlaying) speakChunk(); };
    u.onerror = () => stop();
    synth.speak(u);
    clearInterval(synthRef.current.interval);
    synthRef.current.interval = setInterval(() => { if (synth.speaking) synth.resume(); }, 8000);
  }

  const pause = useCallback(() => {
    if (audioRef.current) audioRef.current.pause();
    else window.speechSynthesis.pause();
    setIsPlaying(false);
  }, []);

  const resume = useCallback(() => {
    if (audioRef.current) audioRef.current.play();
    else window.speechSynthesis.resume();
    setIsPlaying(true);
  }, []);

  const stop = useCallback(() => {
    if (audioRef.current) { audioRef.current.pause(); audioRef.current = null; }
    window.speechSynthesis.cancel();
    clearInterval(synthRef.current.interval);
    setIsPlaying(false);
    setProgress(0);
  }, []);

  const seek = useCallback((pct) => {
    if (audioRef.current && audioRef.current.duration) {
      audioRef.current.currentTime = pct * audioRef.current.duration;
    } else {
      synthRef.current.idx = Math.floor(pct * synthRef.current.chunks.length);
      if (isPlaying) speakChunk();
    }
  }, [isPlaying]);

  return { speak, pause, resume, stop, seek, isPlaying, progress, duration, serverAvailable, voices, voice, setVoice, speed, setSpeed };
}
