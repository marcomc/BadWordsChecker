# TODO List for MP3 BadWordsChecker

This document outlines planned tasks, feature enhancements, and technical debt to be addressed.

## High Priority
- [ ] **Fix Verbose Mode / Stderr Redirection**: The application currently shows all `VoskAPI` logs by default. The attempts to redirect `stderr` to hide these logs in non-verbose mode have been unsuccessful and are currently reverted. This needs to be fixed to provide a clean default user experience.
- [ ] **Fix Full Transcription Logic**: The transcription process is not correctly assembling the full text from the audio. The output `.txt` file often contains only a partial or incomplete transcript. This is a critical bug in the core functionality.
- [ ] **Fix INI file test**: The test `test_config.py::TestConfig::test_ini_provides_value` was disabled because of difficulties in mocking the file system interaction. This needs to be revisited to ensure reliable testing of configuration loading from `.ini` files.
- [ ] **Robust Filename Handling**: Although basic tests with special characters passed, the system needs more rigorous testing across different operating systems (Windows, Linux) to ensure filenames with spaces, non-ASCII characters, and other symbols are handled correctly in all modules (transcription, reporting, quarantine).

## Medium Priority
- [ ] **Improve Error Handling**: Refine error handling across all modules to provide more specific and user-friendly feedback. For example, distinguish between a corrupt MP3 file and a failed transcription.

## Future Enhancements & Low Priority
- [ ] **Fuzzy Matching**: Implement fuzzy matching (e.g., Levenshtein distance) as an alternative `match-mode` to catch misspellings or variations of bad words.
- [ ] **Support for Other Languages**: Refactor the language-specific parts (model, dictionary, normalization) to allow for easier integration of other languages in the future.
- [ ] **GUI**: Develop a simple graphical user interface (GUI) for users who are not comfortable with the command line.
- [ ] **Advanced Dictionary Features**:
  - [ ] Support for regular expressions in the dictionary.
  - [ ] Add word stemming to catch different forms of a word (e.g., "run", "running").
- [ ] **CI/CD Pipeline**: Set up a continuous integration and continuous delivery (CI/CD) pipeline using GitHub Actions to automate testing and releases.
- [ ] **Report Export Formats**: Add options to export the aggregated report to different formats like CSV or JSON.
- [ ] **Parallel Processing**: Utilize multiprocessing to scan multiple MP3 files in parallel, which would significantly speed up processing for large folders.