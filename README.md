# MP3 BadWordsChecker

An offline-capable CLI tool that scans a folder of Italian MP3 story files for profanity.

## Overview

This tool transcribes Italian MP3 files using the Vosk speech recognition toolkit and checks the transcribed text against a list of bad words. It generates reports to help educators and parents validate the suitability of audio stories for children.

## Features

-   **Offline First**: Works without an internet connection after initial setup.
-   **Italian Language**: Specifically tailored for Italian language transcription.
-   **Customizable Dictionary**: Use the default bad words dictionary or provide your own.
-   **Flexible Matching**: Choose between exact word matching or substring matching.
-   **Reporting**: Generates both per-file and aggregated reports of bad words found.
-   **Quarantine**: Automatically move files containing bad words to a separate folder.

## Installation

### Dependencies

-   Python 3.11+
-   ffmpeg
-   Vosk Italian Model

#### 1. Install Python

Make sure you have Python 3.11 or newer installed.

#### 2. Install ffmpeg

-   **macOS (using Homebrew)**:
    ```bash
    brew install ffmpeg
    ```
-   **Linux (using apt)**:
    ```bash
    sudo apt update && sudo apt install ffmpeg
    ```
-   **Windows**:
    Download the latest build from the [official website](https://ffmpeg.org/download.html) and add the `bin` directory to your system's PATH.

#### 3. Install Python Packages

```bash
make install
# or
pip install -r requirements.txt
```

#### 4. Download the Vosk Italian Model

Download the Vosk Italian model from the [official website](https://alphacephei.com/vosk/models) and unzip it. Place the model folder (e.g., `vosk-model-it-0.22`) in the root of the project directory.

#### 5. Download the Bad Words Dictionary

```bash
badwordschecker --download-dict
```

This will download the default `badwords-it.txt` file into the project directory.

## Usage

### Quick Start Example

1.  **Download the Vosk Model**: Download the Italian model from the [Vosk website](https://alphacephei.com/vosk/models) and place the unzipped model folder (e.g., `vosk-model-it-0.22`) in the root of this project.

2.  **Download the Dictionary**:
    ```bash
    make run ARGS="--download-dict"
    ```

3.  **Run the Checker**:
    ```bash
    make run ARGS="/path/to/your/mp3/folder"
    ```

    Replace `/path/to/your/mp3/folder` with the actual path to your MP3s. Reports will be generated in the `parolacce` directory.

### Basic Usage

```bash
badwordschecker /path/to/your/mp3/folder
```

### Options

-   `--download-dict [path]`: Download the default Italian bad words dictionary. Optionally specify a path.
-   `--dict <path>`: Use a custom dictionary file.
 -   `--edit-dict`: Open the dictionary in the system default editor.
 -   `--model-path <path>`: Specify a custom path for the Vosk model directory. If not provided, the model will be stored in a default user configuration directory.
 -   `--match-mode {exact,substring}`: Set the matching mode (default: `exact`).
 -   `--quarantine <folder>`: Move offending MP3s to a review folder.
 -   `--recursive`: Scan for MP3 files recursively.
-   `--verbose`: Enable verbose logging.
-   `--version`: Show the version number.
-   `-h, --help`: Show the help message.

## Development

### Project Structure

```
.
├── badwordschecker
│   ├── __init__.py
│   ├── cli.py
│   ├── dictionary.py
│   ├── reporting.py
│   ├── scanning.py
│   ├── transcription.py
│   └── utils
│       ├── __init__.py
│       ├── logging.py
│       └── text_normalization.py
├── docs
│   └── architecture.md
├── tests
│   ├── __init__.py
│   ├── test_cli.py
│   ├── test_dictionary.py
│   ├── test_reporting.py
│   ├── test_scanning.py
│   └── test_transcription.py
├── .gitignore
├── LICENSE
├── Makefile
├── README.md
└── requirements.txt
```

### Running Tests

```bash
make test
# or
pytest
```

### Linting and Type Checking

```bash
make lint
# or
ruff check .
mypy .
```

### Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## Future Extensions

-   Support for more languages.
-   Fuzzy matching for bad words.
-   A graphical user interface (GUI).
