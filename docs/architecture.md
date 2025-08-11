# Architecture

The MP3 BadWordsChecker is a Python-based CLI tool designed with a modular architecture to facilitate maintenance and extension.

## Core Modules

-   **`cli.py`**: The main entry point of the application. It uses `argparse` to handle command-line arguments and orchestrates the overall workflow.

-   **`dictionary.py`**: Manages the bad words dictionary. It includes functions for loading, downloading, and editing the dictionary file.

-   **`transcription.py`**: Handles the audio transcription process. It uses `ffmpeg` to convert MP3 files to WAV format and the `vosk` library to perform speech-to-text transcription.

-   **`scanning.py`**: Contains the logic for scanning the transcribed text for bad words. It supports both exact and substring matching.

-   **`reporting.py`**: Generates the output reports. It creates a per-file report for each MP3 containing bad words and an aggregated summary report.

-   **`utils/logging.py`**: Configures the application's logging.

-   **`utils/text_normalization.py`**: Provides functions for text normalization, including lowercasing, punctuation removal, and accent normalization.

## Data Flow

1.  The user runs the tool from the command line, providing a path to a folder of MP3 files.
2.  `cli.py` parses the arguments and initializes the logging.
3.  The bad words dictionary is loaded into memory by `dictionary.py`.
4.  The tool iterates through the MP3 files in the specified folder.
5.  For each MP3 file, `transcription.py` is called to:
    a.  Convert the MP3 to a temporary WAV file using `ffmpeg`.
    b.  Transcribe the WAV file to text using the Vosk model.
6.  The transcribed text is passed to `scanning.py`, which checks for bad words.
7.  If any bad words are found, `reporting.py` generates a per-file report.
8.  After all files have been processed, `reporting.py` generates an aggregated report.
9.  If the `--quarantine` option is used, any files containing bad words are moved to the specified folder.
