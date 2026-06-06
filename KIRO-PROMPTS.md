# Kiro Prompt Guide — LPI Study App Improvements

Copy-paste these prompts to Kiro one at a time. Wait for each phase to complete and validate before moving on.

---

## Phase 1: React + Vite Restructure

> **Start with this:**
>
> Read `KIRO-SPEC.md` in this project. It contains a 7-phase improvement plan for this LPI study app. Start with Phase 1 only — restructure the monolithic `index.html` into a React + Vite project. The spec has the full component structure, acceptance criteria, and design tokens to preserve. Read `index.html` to understand the current implementation before you begin.

**If Phase 1 is too large, break it down:**

> Step 1: Extract all embedded data (Q&A pairs, lessons, flashcards, terminal labs) from `index.html` into separate JSON files under `src/data/`. Read the `DATA = {...}` object and the `TERM_LABS` object carefully.

> Step 2: Initialize a Vite + React project and set up the component folder structure from the spec. Add React Router for navigation between modes.

> Step 3: Implement the Practice mode component — the spaced repetition card review with SM-2 algorithm. Port the SM-2 logic into `src/utils/sm2.js`.

> Step 4: Implement the Terminal simulator component with all 9 labs. Preserve the command parsing, task validation, and the filesystem simulation.

> Step 5: Implement the remaining modes: Learn (lesson viewer with TTS), Flashcards (flip cards with navigation), Exam, and Stats (progress dashboard with mastery rings).

> Step 6: Add dark mode context with system preference detection, localStorage migration (detect old data format and convert), streak tracking, and verify all 7 modes work with `npm run dev`.

**✅ Validate:** Run `npm run dev`, test all modes, confirm dark mode, check streak persists across reload.

---

## Phase 2: Keyboard Shortcuts

> Phase 1 is complete. Now implement Phase 2 from `KIRO-SPEC.md` — keyboard shortcuts. Create a `useKeyboard` hook and add all the key bindings listed in the spec. Make sure shortcuts don't fire when typing in the terminal input field. Add visual feedback when grading with number keys.

**✅ Validate:** Press `?` to see overlay, use Space to flip cards, 1-4 to grade, arrow keys in flashcards.

---

## Phase 3: Multiple-Choice Quiz Mode

> Implement Phase 3 from `KIRO-SPEC.md` — Multiple-Choice Quiz Mode. Generate MCQ data from the existing Q&A pairs (create plausible distractors from related content). Build both the exam simulation mode (timed, 20/40/60 questions) and the quick quiz mode (10 questions, immediate feedback). Follow the spec for UI details and keyboard support.

**✅ Validate:** Run a quick quiz, confirm correct/wrong highlighting, check exam mode timer, verify topic filtering.

---

## Phase 4: Weak Areas Review Mode

> Implement Phase 4 from `KIRO-SPEC.md` — Weak Areas Review Mode. Use the SM-2 data (ease factors, lapses, last grade) to identify struggling cards. Add the "Focus on Weak Areas" button, the weak areas dashboard on the Stats page, and recovery tracking.

**✅ Validate:** Grade some cards as "Wrong" a few times, confirm they appear in weak areas review, check Stats page shows weak topics.

---

## Phase 5: Q&A Data Quality

> Implement Phase 5 from `KIRO-SPEC.md` — Q&A Data Quality audit. Create `scripts/audit-qa.js` that flags mismatched answers, duplicates, and empty/too-long answers. Generate a report and a review helper HTML page. Show me the audit report before making any fixes.

**✅ Validate:** Review the audit report, approve fixes, run validation to confirm no regressions.

---

## Phase 6: PWA + Offline Support

> Implement Phase 6 from `KIRO-SPEC.md` — PWA + Offline Support. Use `vite-plugin-pwa` for service worker generation. Add the web app manifest, install prompt banner, offline indicator, and migrate storage from localStorage to IndexedDB with auto-migration of existing data.

**✅ Validate:** Build with `npm run build`, serve dist/ locally, test install prompt, disconnect network and confirm app works offline.

---

## Phase 7: TTS Migration to Kokoro

> Implement Phase 7 from `KIRO-SPEC.md` — migrate TTS from Piper to Kokoro. Create the `useTTS` hook that connects to Kokoro-FastAPI at localhost:8880 (OpenAI-compatible endpoint), falls back to Web Speech API. Add voice selector, speed control, and audio caching in IndexedDB. Remove old Piper server code (`tts_server.py`, `tts/` folder). Keep the text highlighting and seek bar behavior identical.

**✅ Validate:** Start Kokoro Docker (`docker run -p 8880:8880 ghcr.io/remsky/kokoro-fastapi`), test read-aloud in Learn mode, change voice, change speed, test fallback by stopping the Docker container.

---

## Tips

- **Always validate between phases** — don't stack unverified changes
- **If Kiro gets confused**, say: "Stop. Re-read `KIRO-SPEC.md` Phase X and follow it exactly."
- **If something breaks**, say: "The [feature] broke after your last change. Revert and try again."
- **For context on current behavior**, say: "Read `index.html` to see how [feature] currently works, then port it."
