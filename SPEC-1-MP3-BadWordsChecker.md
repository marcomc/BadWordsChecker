# SPEC-1-MP3-BadWordsChecker

## Background

Children’s audio stories in MP3 format can sometimes contain inappropriate language that is unsuitable for audiences aged six or under. Manually reviewing these files for unpolite or profane words is time-consuming and prone to human oversight.

This project aims to develop a Command-Line Interface (CLI) tool that automates this process for Italian-language stories. The tool will:
- Traverse a specified folder containing MP3 files of children’s stories.
- Use existing free command-line tools to transcribe audio into text.
- Scan the transcribed text against a downloadable and editable dictionary of Italian bad words.
- Generate per-file reports in a `parolacce` folder and a consolidated statistics file summarizing all detected words.

The primary goal is to allow educators, parents, and content curators to quickly verify that audio stories are safe for young audiences.

---

## Requirements


### Must Have
- Accept a folder path as input containing MP3 files.
- Use free, locally installable CLI tools to transcribe MP3 files to text in Italian.
- Provide CLI options to:
    - Download the default Italian bad words dictionary.
    - Specify a custom bad words dictionary file.
    - Open the dictionary file in the user’s default text editor for review/editing.
- Compare transcribed text with the chosen bad words dictionary.
- For each MP3 containing bad words, create a `.txt` report file in a `parolacce` folder with the same name as the MP3 file, listing all bad words found.
- Generate a `parolacce.txt` statistics file in the `parolacce` folder showing:
    - Bad word frequency counts across all files.
    - Which MP3s contain each bad word.
- Handle UTF-8 text encoding correctly (Italian accents and special characters).
- Work offline after dictionary and dependencies are downloaded.
- Provide a `--help`/`-h` CLI option that prints usage instructions and available options.
- Include a `README.md` file in the project root with clear usage instructions and example commands.
- Include development documentation (in the README or a separate file) so that future developers can understand, maintain, and extend the tool.

### Should Have
- Automatically install required CLI transcription tools if missing.
- Log all processing steps for debugging.
- Support MP3 filenames with spaces or special characters.

### Could Have
- Configurable minimum bad word match sensitivity (exact vs partial matches).
- Option to automatically move MP3s with bad words into a separate folder for review.

### Won’t Have (for now)
- Support for languages other than Italian.
- Real-time audio analysis while the MP3 is playing.

---

## Method

### Technical Approach
1. **Audio Transcription**
     - Use Vosk with the Italian acoustic model for offline speech recognition.
     - MP3 files are converted to WAV using ffmpeg before transcription.
2. **Bad Words Dictionary Management**
     - Download:
         - CLI option: `--download-dict` downloads the default Italian bad words dictionary from a known URL.
     - Review/Edit:
         - CLI option: `--edit-dict` opens the dictionary file in the system’s default text editor.
     - Custom Path:
         - CLI option: `--dict /path/to/custom_dict.txt` allows user to override the default dictionary.
     - Dictionary file stored as plain UTF-8 text, one word per line.
3. **Text Scanning**
     - Normalize text to lowercase, strip punctuation.
     - Match against dictionary (loaded into a set for O(1) lookups).
     - Count word occurrences per file.
4. **Report Generation**
     - Per-file reports stored in `parolacce` folder: `{filename}.txt` lists bad words and counts.
     - Aggregated `parolacce.txt` contains:
         - Word → Total count across all files
         - Word → Files where it appears

---

## Architecture Diagram (PlantUML)

