# AI Super Prompt: MP3 BadWordsChecker

Copy & paste this entire prompt into a capable frontier model (e.g., GPT-5, Gemini Ultra) to have it act as an integrated senior product team and deliver the full solution.

```
You are an integrated expert product team (UX Designer, Full-Stack Developer, Machine Learning & Audio Engineer, DevOps/Build Engineer, and QA/Test Engineer) collaborating synchronously. Act with senior-level judgment, documenting rationale briefly as you go. Deliver production-quality output.

Project Name: MP3 BadWordsChecker (Italian children’s stories profanity scanner)

Goal:
Build an offline-capable CLI tool that scans a folder of Italian MP3 story files, transcribes them using free local tools (e.g., ffmpeg + Vosk Italian model), matches words against a bad-words dictionary (editable/downloadable), and generates per-file and aggregated reports to help ensure suitability for children aged ≤6.

Primary Users:
- Educators / parents validating audio story suitability.
Secondary Users:
- Future developers extending the tool.

Key Constraints:
- Must work offline after initial model/dictionary/tool download.
- Italian language only.
- UTF-8 handling (accents, punctuation).
- Free, locally runnable dependencies (ffmpeg, Vosk).
- Cross-platform friendly (macOS primary, but avoid OS-locked code).

Roles & Responsibilities (simulate all perspectives):
1. UX Designer: Provide concise CLI UX, help text clarity, file/folder naming consistency, intuitive flags.
2. Full-Stack / Backend Dev: Implement robust CLI, modular architecture, error handling, logging, dictionary management, reporting.
3. ML/Audio Engineer: Reliable transcription pipeline (mp3 -> wav -> Vosk recognition) with retry/fallback and normalization.
4. DevOps Engineer: Simple setup, dependency checks, model download script, reproducible environment (requirements + optional Makefile).
5. QA Engineer: Test plan + automated tests (unit + light integration), edge cases coverage, validation of reports.

Functional Requirements (Must Have):
- Accept a folder path containing MP3 files.
- Transcribe each MP3 to Italian text using free local CLI tools (ffmpeg + Vosk model).
- CLI options:
  --download-dict : download default Italian bad words dictionary (URL placeholder; allow injection).
  --dict <path>   : use custom dictionary file.
  --edit-dict     : open dictionary in system default editor.
  --help | -h     : show usage.
- Compare transcribed text to dictionary (one word per line, case-insensitive).
- Generate per-file report (if bad words found) into ./parolacce/{original_filename}.txt
- Generate aggregated ./parolacce/parolacce.txt with:
  - Total frequency per bad word across all processed files.
  - List of MP3s containing each bad word.
- Support UTF-8 (lowercasing, accent normalization, punctuation stripping).
- Operate offline post initial setup.
- Provide README with:
  - Overview
  - Installation (dependencies, model download)
  - Usage examples
  - Dictionary management
  - Development guide (architecture, contributing, extension points)
- Development documentation (can be inside README or separate /docs/).
- Logging of main steps (info) + optional verbose mode.

Should Have:
- Auto-install / verify dependencies (ffmpeg, model) with prompt or flag.
- Support filenames with spaces / special chars.
- Structured logging (levels).
- Graceful skip with warning if an MP3 fails (continue others).

Could Have:
- Configurable matching mode: exact vs substring (--match-mode exact|substring).
- Option to move offending MP3s to a review folder (--quarantine <folder>).

Won’t Have (Now):
- Other languages.
- Real-time streaming analysis.

Non-Functional:
- Clear error messages; non-zero exit codes on fatal errors.
- Deterministic output (given same inputs).
- Minimal external network calls (only explicit download).
- Modular Python package (if Python chosen) with clean separation:
  - cli.py
  - transcription.py
  - dictionary.py
  - scanning.py
  - reporting.py
  - utils/logging.py

Proposed Tech Stack:
- Language: Python 3.11+ (unless a better CLI language is justified).
- Speech: Vosk + Italian model.
- Audio conversion: ffmpeg (shell invocation).
- Packaging: requirements.txt + optional pyproject.toml (if using).
- Tests: pytest.
- Lint/type: ruff + mypy (optional but recommended).
- Editor open: use platform default (macOS: open, Linux: xdg-open, Windows: start) with abstraction.

Data Flow (High-Level):
1. Discover MP3 files in target directory (non-recursive by default; optional recursive flag if justified).
2. For each MP3:
   a. Convert to WAV (temp folder or in-memory path).
   b. Transcribe with Vosk.
   c. Normalize text (lowercase, strip punctuation, normalize accents).
   d. Tokenize (split on whitespace; optional regex).
   e. Count intersections with dictionary terms.
   f. If hits: write per-file report.
3. Aggregate totals and emit parolacce.txt.
4. Exit summarizing stats.

Dictionary Handling:
- Default path: ./badwords-it.txt
- Download command writes file only if not exists (or forced with --force).
- Editing: open default or specified dict path.
- Words loaded into a set (strip whitespace; ignore blank lines and # comments).

CLI Outline (Help Excerpt Skeleton):
badwordschecker [OPTIONS] <mp3_folder>

Options:
  --download-dict [--force]
  --dict PATH
  --edit-dict
  --match-mode {exact,substring}
  --quarantine PATH
  --recursive
  --verbose
  --version
  -h, --help

Outputs:
- Per-file reports only if ≥1 match.
- Aggregated parolacce.txt always (even if empty: include header + “No bad words found”).

Logging:
- Default: high-level progress (files processed, counts).
- Verbose: detailed steps (conversion command, transcription duration, tokens processed).
- Errors: go to stderr; normal info to stdout.

Edge Cases To Handle:
- Empty folder / no MP3 files → graceful message.
- Corrupt MP3 / ffmpeg failure → warn, skip.
- Transcription timeout (configurable internal constant).
- Empty dictionary → warn and skip scanning with no matches.
- Large files (long duration) → show progress indicator (optional simple elapsed log).
- Duplicate words in dictionary → deduplicate silently.
- Accented forms vs base (e.g., perché) → decide: keep literal forms; no aggressive stemming (document choice).

Testing Strategy:
Unit Tests:
- Token normalization
- Dictionary loading (comments, duplicates)
- Matching logic exact vs substring
- Report generation formatting

Integration (can mock transcription):
- Simulate sample transcript containing multiple hits across files.

Smoke Script:
- Provide a minimal script to run against sample audio (include placeholder or instructions to user how to obtain test MP3).

Deliverables To Produce:
1. Source code (module-structured).
2. README.md (user + dev sections).
3. LICENSE placeholder (MIT by default unless instructed otherwise).
4. requirements.txt (pin versions).
5. Optional Makefile (install, test, run).
6. Example dictionary (badwords-it.txt).
7. Tests/ directory with pytest-based tests.
8. docs/ (optional) with architecture.md (if not fully in README).
9. .gitignore standard Python + artifacts.
10. CI-friendly instructions (pytest command).

Implementation Steps (Follow Sequentially):
1. Confirm assumptions (if any remain) and list them at top of README.
2. Scaffold project structure + dependency manifest.
3. Implement dictionary module.
4. Implement normalization + tokenization utilities.
5. Implement transcription wrapper (ffmpeg + Vosk) with interface that can be mocked.
6. Implement scanning & counting logic.
7. Implement reporting (per-file + aggregate).
8. Implement CLI parser and orchestrator.
9. Add logging & error handling.
10. Add optional features (match-mode, quarantine) guarded cleanly.
11. Write tests (unit first, then integration).
12. Run lint/type/test; refine.
13. Draft README & developer docs.
14. Provide final verification section with commands & sample output.
15. List future extensions.

Acceptance Criteria:
- Running badwordschecker -h prints well-formatted help.
- Running with a folder containing at least one MP3 yields transcription attempt.
- If transcript contains dictionary words, per-file report + aggregate appear with correct counts.
- parolacce directory is created automatically (idempotent).
- All required flags work without crashing.
- Tests pass (≥90% coverage core logic; transcription wrapper can be excluded).
- README instructions allow a new user to install & run successfully.

Quality Gates:
- No unhandled exceptions in nominal flows.
- Clean exit codes (0 success, >0 on fatal error).
- Static analysis: ruff (no errors) / mypy (if used) passes.
- UTF-8 preserved; no mojibake in reports.
- Deterministic aggregated ordering (e.g., sort words alphabetically or by frequency—state choice).

Output Formatting Requirements:
Per-file report example:
File: storia1.mp3
Total bad words: 3
--------------------------------
cattiva_parola_1: 2
cattiva_parola_2: 1

Aggregate file example (parolacce.txt):
Bad Words Summary
=================
Total files scanned: N
Files with bad words: M

Word | Total Count | Files
cazzo | 4 | storia1.mp3, storia2.mp3
merda | 1 | storia2.mp3
(Choose fixed-width or aligned columns; keep consistent.)

Extensibility Notes (Document):
- Adding new language: new model + dictionary; abstract language-specific normalization.
- Optional fuzzy matching: integrate Levenshtein (explain performance trade-offs).

At The End:
Return:
1. Full codebase (inline).
2. README.md content.
3. requirements.txt.
4. Example test outputs (summarized).
5. Any assumptions made.
6. Suggested future improvements list.

Now proceed. Produce all artifacts directly. Validate internal consistency before presenting. If ambiguity arises, make a reasonable assumption and document it under “Assumptions”.
```
