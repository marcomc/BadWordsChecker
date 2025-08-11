# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.2] - 2025-08-11

### Added
- A `run_badwordcheck_all.sh` script to automate testing on all MP3 files in a folder.

### Fixed
- Corrected the transcription logic to ensure the full text of the audio is processed and saved.
- Implemented a robust, manual progress indicator for the transcription process.
- Resolved an `AttributeError` in the `ffmpeg` error handling logic.

## [0.1.1] - 2025-08-11

### Fixed
- Correctly parse boolean values from the `.ini` configuration file.
- Ensured the default dictionary URL is used as a proper fallback.

### Changed
- **Refactored Configuration**: Centralized all configuration logic (CLI arguments and `.ini` file) into a new `badwordschecker.utils.config` module for improved maintainability.
- **Refactored Tests**: Reorganized the test suite for better separation of concerns, deleting the problematic `test_config_integration.py` and creating a more focused `test_config.py`.

## [0.1.0] - 2025-08-11

### Added
- **Initial Release**: Core functionality for scanning MP3 files for bad words.
- **Transcription**: Transcribes Italian MP3s to text using `ffmpeg` and `Vosk`.
- **Scanning**: Scans transcribed text for bad words using an editable dictionary. Supports `exact` and `substring` match modes.
- **Reporting**: Generates per-file and aggregated reports in the `parolacce` directory.
- **Dictionary Management**: CLI options to download, edit, or specify a custom bad words dictionary.
- **Configuration**: Support for persistent settings via a `badwordschecker.ini` file.
- **Dependency Checks**: Added startup checks for `ffmpeg` and the Vosk model.
- **Logging**: Implemented structured JSON logging via a `--log-format` flag.
- **Testing**: Initial suite of unit tests for all core modules.
- **Documentation**: `README.md`, `LICENSE`, and architecture documentation.
