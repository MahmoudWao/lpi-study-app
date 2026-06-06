# LPI Study App — Kiro Improvement Spec

## Project Overview
**Source**: `C:\Users\miikharo\lpi-study-app\index.html` (363KB single-file HTML app)
**Purpose**: Study app for LPI Linux Essentials 010 exam
**Current stack**: Vanilla HTML/CSS/JS, no frameworks, localStorage for persistence
**Features**: Spaced repetition (SM-2), terminal simulator, flashcards, lessons, dark mode, TTS

---

## Phase 1: Project Restructure → React + Vite

### Goal
Migrate the monolithic `index.html` into a maintainable React + Vite project while preserving ALL existing functionality and user data.

### Requirements
1. **Initialize** with `npm create vite@latest lpi-study-app -- --template react`
2. **Extract data** — all Q&A pairs, lessons, terminal labs, and flashcard content into separate JSON files under `src/data/`
3. **Component structure**:
   ```
   src/
   ├── components/
   │   ├── Header.jsx
   │   ├── Nav.jsx
   │   ├── Practice/         (spaced repetition mode)
   │   ├── Learn/            (lesson viewer)
   │   ├── Terminal/          (shell simulator)
   │   ├── Flashcards/        (flip cards)
   │   ├── Exam/             (exam mode — will become MCQ)
   │   ├── Stats/            (progress dashboard)
   │   └── shared/           (buttons, cards, progress bars)
   ├── hooks/
   │   ├── useSpacedRepetition.js   (SM-2 algorithm)
   │   ├── useLocalStorage.js
   │   └── useKeyboard.js
   ├── data/
   │   ├── questions.json
   │   ├── lessons.json
   │   ├── flashcards.json
   │   └── terminal-labs.json
   ├── styles/
   │   └── theme.css          (CSS variables from current :root)
   └── utils/
       ├── sm2.js             (SM-2 scheduling logic)
       └── storage.js         (localStorage/IndexedDB wrapper)
   ```
4. **Preserve the design system** — keep ALL current CSS variables, colors, animations, and visual feel
5. **Data migration** — on first load, detect existing localStorage data and migrate it seamlessly
6. **Dark mode** — implement with React context + CSS variables (already has dark mode CSS)
7. **Routing** — use React Router for modes (Practice, Learn, Terminal, Flashcards, Exam, Stats)

### Acceptance Criteria
- All 7 study modes work identically to current app
- Existing localStorage progress is auto-migrated
- `npm run dev` starts hot-reload dev server
- `npm run build` produces a static dist/ that works offline (like the current HTML)
- Terminal simulator retains all 9 labs with command parsing
- Dark mode toggle works
- Streak tracking persists

---

## Phase 2: Keyboard Shortcuts

### Goal
Add comprehensive keyboard navigation for power-user studying.

### Key Bindings
| Key | Context | Action |
|-----|---------|--------|
| `Space` | Flashcard / Practice | Flip card / Show answer |
| `1` | After answer shown | Grade: Wrong (Again) |
| `2` | After answer shown | Grade: Hard |
| `3` | After answer shown | Grade: Good |
| `4` | After answer shown | Grade: Easy |
| `←` / `→` | Flashcards | Previous / Next card |
| `Enter` | MCQ mode | Submit selected answer |
| `A/B/C/D` | MCQ mode | Select answer option |
| `D` | Global | Toggle dark mode |
| `?` | Global | Show keyboard shortcut overlay |
| `Esc` | Any modal/overlay | Close |

### Requirements
- Show a small `?` icon in the header that opens a shortcut cheat sheet
- Shortcuts should NOT fire when user is typing in terminal simulator input
- Visual feedback — briefly highlight the grade button when pressing 1-4
- Implement as a `useKeyboard` hook that modes can subscribe to

---

## Phase 3: Multiple-Choice Quiz Mode

### Goal
Add an exam-simulation mode with multiple-choice questions matching the LPI exam format (the real exam is multiple choice).

### Requirements
1. **Question format**: Each question has 4 options (A-D), one correct answer, and an explanation
2. **Generate MCQ data** from existing Q&A pairs:
   - Correct answer = current answer
   - Generate 3 plausible distractors from related content in the same topic
   - Store in `src/data/mcq-questions.json`
3. **Exam simulation mode**:
   - Configurable: 20, 40, or 60 questions
   - 60-minute timer (toggleable)
   - Can filter by topic or "all topics"
   - Shows question number, progress bar, time remaining
   - Flag questions for review before submitting
   - Results screen: score, pass/fail (65% threshold), breakdown by topic
4. **Quick quiz mode**:
   - 10 questions, no timer
   - Immediate feedback after each answer (show correct + explanation)
   - Integrates with spaced repetition — wrong answers reduce card interval
5. **UI**:
   - Radio button style options (A/B/C/D labels)
   - Green highlight on correct after submit, red on wrong
   - Keyboard support: A/B/C/D to select, Enter to confirm

---

## Phase 4: Weak Areas Review Mode

### Goal
Smart study mode that prioritizes cards the user struggles with most.

### Requirements
1. **Identify weak cards** using SM-2 data:
   - Cards with `easeFactor < 2.0` (struggling)
   - Cards with `lapses >= 3` (frequently forgotten)
   - Cards last graded "Wrong" or "Hard"
   - Cards overdue by more than 2x their interval
2. **Weak Areas Dashboard**:
   - Show number of weak cards per topic/section
   - Visual indicator (red/amber) on section cards showing weakness
   - "Weakest Topics" summary at top of Stats page
3. **Targeted Review Session**:
   - "Focus on Weak Areas" button on Practice page
   - Presents ONLY weak cards, ordered by worst-performing first
   - After reviewing all weak cards, show encouragement + suggest next study action
4. **Recovery tracking**:
   - Track when cards "recover" (ease factor improves above threshold)
   - Show "Cards Recovered This Week" stat

---

## Phase 5: Fix Q&A Data Quality

### Goal
Audit and fix mismatched question-answer pairs in the study data.

### Requirements
1. **Automated audit script** (`scripts/audit-qa.js`):
   - Flag answers that don't semantically match their question
   - Flag duplicate questions
   - Flag questions with empty or single-word answers
   - Flag extremely long answers (>500 chars) that should be shortened
   - Output a report: `qa-audit-report.json`
2. **Manual review helper**:
   - Generate a simple HTML page showing flagged items for human review
   - Allow marking as "fixed", "needs edit", or "delete"
3. **Common issues to fix**:
   - Answers that describe a different concept than the question asks
   - Terminal command answers that are missing the actual command
   - Duplicate cards across sections
4. **Validation on build**:
   - Add a validation step that catches obvious mismatches before building

---

## Phase 6: PWA + Offline Support

### Goal
Make the app installable on mobile/desktop and fully functional offline.

### Requirements
1. **Service Worker** (`public/sw.js`):
   - Cache all static assets on install
   - Cache-first strategy for app shell
   - Network-first for any future API calls
   - Background sync for potential future cloud backup
2. **Web App Manifest** (`public/manifest.json`):
   ```json
   {
     "name": "LPI Linux Essentials Study",
     "short_name": "LPI Study",
     "start_url": "/",
     "display": "standalone",
     "theme_color": "#6366f1",
     "background_color": "#f8fafc",
     "icons": [/* 192x192 and 512x512 PNG icons */]
   }
   ```
3. **Install prompt**: Show a subtle "Install App" banner on first visit (dismissible)
4. **Offline indicator**: Small badge when offline (but app works fine)
5. **Vite PWA plugin**: Use `vite-plugin-pwa` for automatic SW generation
6. **Data persistence upgrade**:
   - Migrate from localStorage to IndexedDB (using `idb` library)
   - localStorage as fallback for older browsers
   - Auto-migrate existing localStorage data to IndexedDB on first load

---

## Implementation Notes

### Preserve These Critical Features
- SM-2 spaced repetition algorithm (intervals, ease factors, due dates)
- All 561 flashcards with their scheduling state
- 9 terminal labs with command parsing and task validation
- Dark mode with system preference detection
- Streak tracking (current streak, longest streak)
- Section-level mastery rings (amber → indigo → green)

### Design Tokens (keep exact values)
```css
--primary: #6366f1    --green: #10b981
--amber: #f59e0b      --red: #ef4444
--bg: #f8fafc         --surface: #ffffff
--text: #1e293b       --muted: #64748b
```

### Browser Support
- Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- Mobile: iOS Safari 14+, Chrome Android 90+

---

## Phase 7: TTS Migration — Piper → Kokoro

### Goal
Replace the current Piper TTS server with Kokoro-82M for dramatically improved voice quality while maintaining the same user experience (read-aloud with text highlighting, seek bar, play/pause).

### Architecture
```
useTTS hook (React)
  → try: Kokoro-FastAPI at localhost:8880 (OpenAI-compatible API)
  → fallback: Web Speech API (SpeechSynthesis)
```

### Server Setup (Kokoro-FastAPI)
- GitHub: https://github.com/remsky/Kokoro-FastAPI
- Docker: `docker run -p 8880:8880 ghcr.io/remsky/kokoro-fastapi`
- Or Python: `pip install kokoro-onnx` with FastAPI wrapper
- Endpoint: `POST /v1/audio/speech` (OpenAI-compatible)
- Request body: `{ "model": "kokoro", "input": "text here", "voice": "af_heart" }`
- Response: audio/wav or audio/mp3 blob

### Requirements

1. **`src/hooks/useTTS.js`** — React hook that manages TTS state:
   - `speak(text)` — sends text to Kokoro server, plays returned audio
   - `pause()` / `resume()` / `stop()`
   - `seek(position)` — seek within audio
   - `isPlaying`, `progress`, `duration` — reactive state
   - Falls back to Web Speech API if server unreachable
   - Health check on mount: `GET localhost:8880/health`

2. **Voice selector UI**:
   - Dropdown in Learn mode toolbar showing available Kokoro voices
   - Fetch voice list from `GET /v1/audio/voices` on app load
   - Persist selected voice to localStorage
   - Default voice: `af_heart` (female, natural)

3. **Speed control**:
   - Slider: 0.5x → 1.0x → 1.5x → 2.0x
   - Pass `speed` parameter to Kokoro API
   - Persist preference to localStorage

4. **Text highlighting** (preserve current behavior):
   - Split lesson text into sentences/chunks
   - Track audio progress → highlight corresponding chunk
   - Auto-scroll to highlighted section
   - Use `data-chunk` attributes on spans (same as current implementation)

5. **Audio caching** (new feature):
   - Cache generated audio in IndexedDB keyed by (text_hash + voice + speed)
   - On repeat listens, serve from cache instantly
   - Add "Clear TTS Cache" button in Settings
   - Max cache size: 500MB, LRU eviction

6. **Startup helper**:
   - If Kokoro server not detected, show a non-intrusive banner:
     "🔊 For best audio quality, start Kokoro: `docker run -p 8880:8880 ghcr.io/remsky/kokoro-fastapi`"
   - Link to one-click setup script in project README
   - App still works fine with Web Speech fallback

7. **Remove old Piper code**:
   - Delete `tts_server.py`
   - Delete `tts/en_US-amy-medium.onnx` and `.onnx.json`
   - Remove Piper-specific endpoint scanning logic
   - Update README with Kokoro setup instructions

### Migration Notes
- The Kokoro-FastAPI server handles text chunking/stitching internally — no need to chunk in the client
- Audio format: request `response_format: "wav"` for lowest latency, `"mp3"` for smaller cache size
- The current `tts-highlight` CSS class and scroll behavior should be preserved exactly
- Model files (~300MB) are downloaded automatically by the Docker image on first run
- For non-Docker users, add a `scripts/setup-kokoro.py` that downloads the ONNX model and voices to a local `tts/` folder and starts a simple FastAPI server

---

## Phase 8: Mascot Integration — "Nix" the Scholar Penguin

### Goal
Integrate the Nix mascot throughout the app to add personality, encourage the user, and make the study experience more engaging (Duolingo-style).

### Assets
Pre-made transparent PNG assets are in `public/mascot/`:
- `mascot-happy.png` — greeting, default/idle state
- `mascot-celebrating.png` — correct answer, streak milestone, mastery upgrade
- `mascot-thinking.png` — new question presented, loading
- `mascot-worried.png` — streak at risk, long absence
- `mascot-studying.png` — during review sessions, weak areas mode
- `mascot-sleeping.png` — all cards reviewed, nothing due today

### Requirements

1. **`src/components/shared/Mascot.jsx`**:
   - Props: `mood` ('happy' | 'celebrating' | 'thinking' | 'worried' | 'studying' | 'sleeping'), `size` ('sm' | 'md' | 'lg')
   - Sizes: sm = 32px, md = 64px, lg = 128px
   - Smooth crossfade transition when mood changes
   - Optional `message` prop — shows a speech bubble with text next to Nix

2. **Where Nix appears**:
   | Location | Mood | Message |
   |----------|------|---------|
   | Header (small, beside title) | happy | — |
   | Practice — showing a card | thinking | — |
   | Practice — correct (Good/Easy) | celebrating | Random encouraging phrase |
   | Practice — wrong | worried | "Let's try again later!" |
   | Stats page — has weak areas | studying | "Let's focus on these!" |
   | Stats page — all mastered | celebrating | "You're crushing it!" |
   | Flashcards — session complete | sleeping | "All done for now!" |
   | Streak milestone (7, 14, 30 days) | celebrating | "X day streak! 🔥" |
   | Streak = 0 / long absence | worried | "Welcome back! Let's study!" |

3. **Encouraging phrases** (rotate randomly):
   - "Nice one!", "You've got this!", "Keep going!", "Great recall!"
   - "Almost there!", "Nix believes in you!", "💪 Strong work!"

4. **Animation** (optional enhancement):
   - Subtle idle bounce (CSS keyframe, 2s loop)
   - Pop-in animation when mood changes
   - Confetti particles behind celebrating Nix on streak milestones

5. **Settings**:
   - Toggle to hide mascot (some users may prefer minimal UI)
   - Persist preference to localStorage

### Design Notes
- Keep Nix small and non-intrusive — it should enhance, not distract
- On mobile, reduce to `sm` size or hide in some contexts
- Speech bubbles should auto-dismiss after 3 seconds
- The mascot should feel like a study buddy, not a nag

### Rive Animation Roadmap (Progressive Enhancement)

The mascot will evolve from static PNGs → CSS animations → full Rive interactive animation.

#### Stage 1: Static PNGs + CSS (implement now)
- Use the existing PNG assets in `public/mascot/`
- Add CSS keyframe idle bounce (subtle 2s loop float)
- Crossfade transition between mood states (opacity + scale)
- This is the MVP — functional and delightful without dependencies

#### Stage 2: Rive Integration (future upgrade)

**What**: Replace static PNGs with a single interactive `.riv` file (~10-30KB) that smoothly transitions between moods with real animation (blinking, breathing, bouncy movements).

**Package**: `@rive-app/react-canvas`

**Install**: `npm install @rive-app/react-canvas`

**State Machine Design** (to be built in Rive Editor):
```
State Machine: "NixMoods"
├── Input: mood (number) — 0=happy, 1=celebrating, 2=thinking, 3=worried, 4=studying, 5=sleeping
├── States:
│   ├── Idle/Happy → subtle bob + blink loop
│   ├── Celebrating → jump + wing raise + confetti particles
│   ├── Thinking → head tilt + wing on chin + floating "?"
│   ├── Worried → shrink + sweat drop + nervous shake
│   ├── Studying → reading pose + page turn loop
│   └── Sleeping → curl up + breathing + floating Z's
└── Transitions: smooth blend between all states (0.3s)
```

**React Component (Stage 2)**:
```jsx
import { useRive, useStateMachineInput } from '@rive-app/react-canvas';

const MOOD_MAP = { happy: 0, celebrating: 1, thinking: 2, worried: 3, studying: 4, sleeping: 5 };

export function Mascot({ mood = 'happy', size = 'md' }) {
  const sizes = { sm: 32, md: 64, lg: 128 };
  const { rive, RiveComponent } = useRive({
    src: '/mascot/nix.riv',
    stateMachines: 'NixMoods',
    autoplay: true,
  });
  const moodInput = useStateMachineInput(rive, 'NixMoods', 'mood');

  useEffect(() => {
    if (moodInput) moodInput.value = MOOD_MAP[mood];
  }, [mood, moodInput]);

  return <RiveComponent style={{ width: sizes[size], height: sizes[size] }} />;
}
```

**Resources for creating the .riv file**:
- Rive Editor (free): https://rive.app
- Community example — Duolingo-style mascot: https://rive.app/marketplace/25118-49270-meet-kell-in-the-duolingo-style/
- Robot with 5 expressions: https://rive.app/community/files/18720-35184-robot-expressions/
- Rive React state machine docs: https://rive.app/docs/runtimes/react/state-machines
- Duolingo's own Rive usage: https://blog.duolingo.com/world-character-visemes/

**Note**: The `.riv` file must be designed in the Rive Editor by hand (rigging, bones, animation keyframes). Use the current PNG assets as reference art for the character design. The Rive Editor is free and browser-based — no install needed.

---

## Phase 9: Mobile-First Responsive Design

### Goal
Ensure the app is fully functional and comfortable to use on mobile devices (phones and tablets). Study apps are primarily used on mobile — this must be a great experience.

### Requirements

1. **Responsive Layout**:
   - All components must work at 320px–428px viewport width (iPhone SE → iPhone Pro Max)
   - Tablet breakpoint: 768px+ (iPad)
   - Desktop: 1024px+
   - Use CSS `clamp()` for fluid typography and spacing
   - Nav pills should scroll horizontally on small screens (no wrapping to 2 rows)

2. **Touch Interactions**:
   - Flashcard flip: swipe left/right to navigate, tap to flip
   - Practice mode: swipe-based grading (swipe right = Good, swipe left = Again) as alternative to buttons
   - Touch targets: minimum 44x44px for all interactive elements (Apple HIG standard)
   - No hover-dependent interactions — all hover states must have tap equivalents
   - Pull-to-refresh gesture on main study views

3. **Mobile Navigation**:
   - Bottom tab bar on mobile (instead of top nav pills)
   - 5 tabs: Practice, Learn, Terminal, Cards, Stats
   - Active tab indicator with app primary color
   - Exam mode accessible via Stats or a "more" menu
   - Smooth tab transitions (no full page reload feel)

4. **Terminal Simulator on Mobile**:
   - Virtual keyboard should not obscure the terminal output
   - Auto-scroll terminal output when new lines appear
   - Larger font size for readability on small screens
   - Quick-insert buttons for common characters: `|`, `/`, `-`, `~`, `$`
   - Consider a custom mini-keyboard row above the system keyboard

5. **Reading/Learn Mode on Mobile**:
   - Comfortable reading width with proper margins
   - Adjustable font size (A- / A+)
   - TTS play/pause button always visible (sticky at bottom)
   - Swipe between lesson sections

6. **Performance**:
   - Lazy-load modes/routes not currently active
   - Optimize images (mascot PNGs → WebP with PNG fallback)
   - Target: < 3s first meaningful paint on 4G
   - Minimize layout shifts (set explicit dimensions on images/cards)

7. **Safe Areas & Notches**:
   - Use `env(safe-area-inset-*)` for notched devices (iPhone)
   - Bottom tab bar must respect `safe-area-inset-bottom`
   - Content must not be hidden behind status bar

8. **Dark Mode on Mobile**:
   - Respect `prefers-color-scheme` system setting
   - OLED-friendly true black option (`--bg: #000000`) for battery savings
   - Status bar color matches app theme (via `theme-color` meta tag)

9. **Orientation**:
   - Portrait: primary layout (optimized for one-hand use)
   - Landscape: allow but don't force — useful for terminal simulator
   - Lock orientation option in settings

### Breakpoint Strategy
```css
/* Mobile-first approach */
:root { /* Base: mobile (320-767px) */ }

@media (min-width: 768px) { /* Tablet */ }
@media (min-width: 1024px) { /* Desktop */ }
```

### Testing
- Test on: iPhone SE (375px), iPhone 14 (390px), iPhone Pro Max (428px), iPad (768px)
- Chrome DevTools device emulation for initial development
- Real device testing before shipping (especially iOS Safari quirks)
