# 🐧 LPI Linux Essentials 010 — Study App

A **Brilliant-inspired** study app for the [LPI Linux Essentials Version 1.6 (Exam 010)](https://www.lpi.org/our-certifications/linux-essentials-overview/).

Built with guided discovery pedagogy: problem-first learning, spaced repetition, and hands-on practice.

## Features

| Mode | Description |
|------|-------------|
| ⚡ **Challenge** | Problem-first mode — face questions before seeing theory. Self-grade with SM-2 spaced repetition. |
| 📖 **Learn** | Full lesson text, key concepts, command reference, and guided exercises from the curriculum. |
| 💻 **Terminal** | 9 interactive labs with a simulated Linux shell. Practice real commands with task validation. |
| 🃏 **Review** | 561 flashcards with adaptive scheduling. Filter by topic or due date. |
| 📊 **Progress** | Mastery levels per section, streak tracking, and completion stats. |

## Pedagogical Model

Inspired by [Brilliant.org](https://brilliant.org)'s guided discovery approach:

- **Problem-First** — Questions before theory to identify knowledge gaps
- **Active Learning** — Self-grade every card (Wrong → Hard → Good → Easy)
- **Immediate Feedback** — Hints from lesson material, step-by-step answers
- **Spaced Repetition** — SM-2 algorithm adapts review intervals to your performance
- **Mistakes Encouraged** — Wrong answers schedule sooner review, not punishment

## Usage

Just open `index.html` in any browser. No server, no dependencies, no internet required.

All progress is saved to browser localStorage and persists across sessions.

## Terminal Labs

| Lab | Exam Section | Skills |
|-----|-------------|--------|
| Filesystem Navigation | 2.3 | `pwd`, `ls`, `cd` |
| Creating & Managing Files | 2.4 | `mkdir`, `touch`, `cp`, `mv`, `rm` |
| File Permissions | 5.3 | `chmod`, `ls -l`, ownership |
| Archiving & Compression | 3.1 | `tar`, `gzip` |
| Searching & Filtering | 3.2 | `grep`, `wc`, `head`, `find`, pipes |
| Basic Scripting | 3.3 | `echo`, variables, `$PATH` |
| Users & Groups | 5.1 | `whoami`, `groups`, `/etc/passwd` |
| Networking Basics | 4.4 | `ip addr`, `ping`, `route`, `dig` |
| Getting Help | 2.2 | `man`, `apropos`, `type` |

## Exam Topics Covered

1. The Linux Community and a Career in Open Source (1.1–1.4)
2. Finding Your Way on a Linux System (2.1–2.4)
3. The Power of the Command Line (3.1–3.3)
4. The Linux Operating System (4.1–4.4)
5. Security and File Permissions (5.1–5.4)

## Building from Source

If you modify the source PDF extraction:

```bash
python extract_deep.py        # Extract content from PDF
python build_structured.py    # Build structured learning data
python build_final.py         # Inject data into HTML template
```

## License

Study content based on [LPI Learning Materials](https://learning.lpi.org/) (CC BY-NC-ND 4.0).
