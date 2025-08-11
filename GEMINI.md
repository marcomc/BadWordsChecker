# Project Overview
**Purpose**: To provide an offline-capable CLI tool for scanning Italian MP3 story files for profanity.
**Elevator Pitch**: MP3 BadWordsChecker helps parents and educators quickly validate audio story suitability for young children by transcribing and scanning for inappropriate language, with flexible configuration options.
**Primary Users**: Educators, parents.
**High-level Scope Boundaries**:
-   **In**: Italian language support, MP3 transcription, customizable bad words dictionary, per-file and aggregated reporting, offline capability, configuration file support.
-   **Out**: Real-time streaming analysis, support for other languages (initially), graphical user interface.

# Objectives & Non-Goals
**Objectives**:
-   Build a robust, cross-platform CLI tool.
-   Ensure accurate transcription of Italian audio.
-   Provide flexible dictionary management (download, custom, edit).
-   Generate clear, actionable reports.
-   Maintain offline functionality after initial setup.
-   Allow configuration via file with clear precedence rules.

**Non-Goals**:
-   Become a general-purpose audio analysis tool.
-   Support real-time audio processing.
-   Offer multi-language support in the first iteration.
-   Develop a complex UI/UX beyond CLI.

# Current Feature Set (Implemented vs Planned)
**Implemented Features**:
-   **MP3 Folder Scanning**: Accepts a folder path and discovers MP3 files (non-recursive by default, recursive option available).
-   **Audio Transcription**: Converts MP3 to WAV using `ffmpeg` and transcribes WAV to text using `Vosk` (Italian model).
-   **Dictionary Management**:
    -   Download default Italian bad words dictionary (`--download-dict [path]`).
    -   Use custom dictionary file (`--dict <path>`).
    -   Open dictionary in system default editor (`--edit-dict`).
-   **Text Scanning**: Compares transcribed text against dictionary words (case-insensitive, exact match).
-   **Reporting**:
    -   Generates per-file reports (`./parolacce/{original_filename}.txt`) if bad words are found.
    -   Generates aggregated report (`./parolacce/parolacce.txt`) with total frequency per bad word and list of containing MP3s.
-   **Text Normalization**: Handles UTF-8, lowercasing, accent normalization, punctuation stripping.
-   **Offline Operation**: Works offline post initial setup (model and dictionary download).
-   **Quarantine**: Option to move offending MP3s to a specified review folder (`--quarantine <folder>`).
-   **Logging**: High-level progress logging, optional verbose mode.
-   **Configuration File Support**: Reads parameters from `badwordschecker.ini`.
-   **Config Precedence**: CLI arguments override INI file settings, which override default values.

**Planned Features**:
-   Configurable matching mode: `substring` (currently only `exact` is fully implemented).
-   Auto-install/verify dependencies (ffmpeg, Vosk model).
-   Support for filenames with spaces/special characters (partially handled, needs robust testing).
-   Structured logging (levels).

# Architecture Summary
**Key Components**:
-   **`cli.py`**: Main entry point, argument parsing, workflow orchestration, integrates with config module.
-   **`dictionary.py`**: Handles dictionary loading, downloading, and editing.
-   **`transcription.py`**: Manages MP3 to WAV conversion (`ffmpeg`) and speech-to-text (`Vosk`).
-   **`scanning.py`**: Contains the core logic for comparing transcribed text against the bad words dictionary.
-   **`reporting.py`**: Generates per-file and aggregated reports.
-   **`utils/logging.py`**: Centralized logging configuration.
-   **`utils/text_normalization.py`**: Utility functions for text preprocessing.
-   **`utils/config.py`**: New module responsible for reading and providing configuration options from `badwordschecker.ini` with precedence logic.

**Data/Control Flow**:
1.  User invokes `cli.py` with MP3 folder path and options.
2.  `cli.py` reads configuration from `badwordschecker.ini` via `utils/config.py`, applying precedence with CLI arguments.
3.  `cli.py` loads the bad words dictionary via `dictionary.py` (using potentially configured path/URL).
4.  `cli.py` discovers MP3 files in the target directory.
5.  For each MP3:
    a.  `transcription.py` converts MP3 to a temporary WAV.
    b.  `transcription.py` transcribes WAV to text using the Vosk model.
    c.  Text is normalized by `utils/text_normalization.py`.
    d.  `scanning.py` identifies bad words in the normalized text (using configured match mode).
    e.  If bad words are found, `reporting.py` generates a per-file report.
    f.  If `--quarantine` (or configured quarantine) is used, `cli.py` moves the MP3.
6.  After all MP3s are processed, `reporting.py` generates an aggregated report.

**External Services**:
-   GitHub (for default dictionary download URL).

**Deployment/Runtime Model**:
-   Local execution as a Python CLI tool. Requires `ffmpeg` and Vosk model to be present on the user's system.

**Diagrams (Mermaid)**:
```mermaid
graph TD
    A[User] --> B(badwordschecker CLI)
    B -- CLI Args --> C{cli.py: Parse Args & Load Config}
    C -- Reads --> D[badwordschecker.ini]
    C -- Configured Options --> E{cli.py: Orchestrate Operations}

    E -- (if --download-dict) --> F(dictionary.py: Download Dictionary)
    E -- (if --edit-dict) --> G(dictionary.py: Edit Dictionary)

    E --> H[MP3 Folder Path]
    H --> I(cli.py: Discover MP3s)
    I --> J{For each MP3}
    J --> K(transcription.py: Convert MP3 to WAV)
    K --> L(transcription.py: Transcribe WAV with Vosk)
    L --> M(utils/text_normalization.py: Normalize Text)
    M --> N(scanning.py: Scan for Bad Words)
    N -- Matches Found --> O(reporting.py: Generate Per-File Report)
    O --> P(cli.py: (Optional) Quarantine MP3)
    J --> Q(reporting.py: Generate Aggregated Report)
    Q --> R[Output: parolacce/ Reports]
```

# Technology & Stack Choices (with rationale)
-   **Language**: Python 3.11+
    -   **Rationale**: Widely adopted for CLI tools, rich ecosystem for audio processing and text manipulation, good cross-platform compatibility.
    -   **Trade-offs**: Performance can be slower than compiled languages for CPU-intensive tasks (mitigated by offloading to `ffmpeg` and `Vosk`'s C backend).
-   **Speech Recognition**: Vosk
    -   **Rationale**: Free, open-source, offline-capable, provides pre-trained Italian models, Python bindings available.
    -   **Trade-offs**: Model size can be large, requires separate download and placement.
-   **Audio Conversion**: `ffmpeg` (shell invocation)
    -   **Rationale**: Industry standard, highly optimized, supports a vast array of audio formats, reliable.
    -   **Trade-offs**: External dependency, requires user installation and correct PATH configuration.
-   **CLI Framework**: `argparse` (Python standard library)
    -   **Rationale**: Built-in, no external dependencies, sufficient for the current CLI complexity.
    -   **Trade-offs**: Less feature-rich than third-party libraries like Click or Typer, but simpler for this scope.
-   **Dependency Management**: `requirements.txt`
    -   **Rationale**: Simple, widely understood, ensures reproducible environments.
    -   **Trade-offs**: Less advanced features than Poetry or PDM (e.g., dependency resolution for complex graphs).
-   **Testing Framework**: `pytest`
    -   **Rationale**: Powerful, flexible, easy to write tests, extensive plugin ecosystem.
    -   **Trade-offs**: None significant for this project.
-   **Linting/Formatting**: `ruff`
    -   **Rationale**: Extremely fast, combines multiple linters (Flake8, isort, Black-like formatting), simplifies development workflow.
    -   **Trade-offs**: Relatively new, might have minor breaking changes in future versions.
-   **Type Checking**: `mypy`
    -   **Rationale**: Improves code quality, catches potential bugs early, enhances readability and maintainability.
    -   **Trade-offs**: Can add overhead to development (requires writing type hints), might have occasional false positives.
-   **Configuration Parsing**: `configparser` (Python standard library)
    -   **Rationale**: Standard library module for handling INI-style configuration files, simple to use.
    -   **Trade-offs**: Less flexible than YAML or JSON for complex configurations, but sufficient for this project's needs.

# Key Design Decisions (table: Decision | Rationale | Status | Notes)
| Decision | Rationale | Status | Notes |
| :--- | :--- | :--- | :--- |
| Offline-first | Primary user (parents/educators) may have limited internet access. | Implemented | Requires initial download of Vosk model and dictionary. |
| External `ffmpeg` dependency | Leverage highly optimized, battle-tested audio processing. | Implemented | User must install `ffmpeg` separately. |
| Vosk for ASR | Free, open-source, offline, good Italian model. | Implemented | Vosk model needs to be downloaded and placed manually. |
| Modular Python structure | Enhances maintainability, testability, and future extensibility. | Implemented | Clear separation of concerns (e.g., `dictionary.py`, `transcription.py`). |
| Dictionary as plain text file | Simple for users to inspect and edit manually. | Implemented | One word per line, supports comments. |
| `parolacce` output directory | Centralized, predictable location for all reports. | Implemented | Created automatically if it doesn't exist. |
| `--download-dict [path]` | Provides flexibility for users to specify download location. | Implemented | Defaults to current directory if no path is given. |
| Configuration via `badwordschecker.ini` | Allows persistent settings and easier management of default options without CLI flags. | Implemented | Supports `[dictionary]` and `[options]` sections. |
| CLI arguments override config file | Standard and expected behavior for CLI tools, providing immediate control. | Implemented | Ensures user's explicit command takes precedence. |

# Implementation Details (modules, patterns, conventions)
-   **Modules**:
    -   `badwordschecker/cli.py`: Orchestrates the main application flow, handles argument parsing, and calls other modules. Now integrates with `utils/config.py` to load options.
    -   `badwordschecker/dictionary.py`: Manages loading, downloading (from a hardcoded URL), and opening the dictionary file. `DEFAULT_DICT_URL` is now defined here.
    -   `badwordschecker/transcription.py`: Contains `convert_mp3_to_wav` (uses `subprocess` to call `ffmpeg`) and `transcribe_audio` (uses `vosk` library).
    -   `badwordschecker/scanning.py`: Implements `scan_text` function, which uses `utils.text_normalization` and `collections.Counter`.
    -   `badwordschecker/reporting.py`: Contains `generate_per_file_report` and `generate_aggregated_report` functions, handling file writing and formatting.
    -   `badwordschecker/utils/logging.py`: Sets up basic `logging` configuration (INFO/DEBUG levels).
    -   `badwordschecker/utils/text_normalization.py`: Provides `normalize_text` (lowercasing, accent removal, punctuation stripping) and `tokenize_text`.
    -   **`badwordschecker/utils/config.py`**: New module. Reads `badwordschecker.ini` from current directory, home directory, or package root. Provides `get_config_option` and specific `get_config_*` functions to retrieve typed configuration values with fallbacks and CLI overrides.
-   **Notable Patterns**:
    -   **Dependency Injection (Implicit)**: Modules often receive dependencies (like `Path` objects or `Vosk` models) as arguments, making them more testable.
    -   **Command Pattern**: The CLI acts as a command dispatcher, invoking specific functions based on user arguments.
    -   **Configuration Precedence**: Implemented by `utils/config.py` where CLI arguments take highest precedence, followed by INI file settings, then hardcoded defaults.
-   **Conventions**:
    -   **Naming**: Snake_case for variables and functions, PascalCase for classes.
    -   **Error Handling**: Uses `try-except` blocks for external calls (`ffmpeg`, `requests`, `vosk`) and `sys.exit(1)` for fatal errors. Logs errors using the `logging` module.
    -   **Logging**: Uses Python's standard `logging` module. Configured in `utils/logging.py`.
    -   **Configuration**: Now supports `badwordschecker.ini` for persistent settings, in addition to CLI arguments.

# Environment & Setup Notes
**Prerequisites**:
-   Python 3.11+
-   `ffmpeg` (installed and accessible in system PATH)
-   Vosk Italian model (e.g., `vosk-model-it-0.22`, downloaded and placed in project root)

**Build/Run/Test Commands**:
-   **Clone repository**: `git clone <repo_url>`
-   **Navigate to project**: `cd BadWordsChecker`
-   **Create virtual environment**: `make venv`
-   **Install Python dependencies**: `make install`
-   **Download default dictionary**: `make run ARGS="--download-dict"`
-   **Run tests**: `make test`
-   **Run linting**: `make lint`
-   **Run the tool**: `make run ARGS="/path/to/your/mp3/folder"`

**Configuration File (`badwordschecker.ini`)**:
-   Place `badwordschecker.ini` in the current working directory, your home directory, or the package root.
-   Example content:
    ```ini
    ; BadWordsChecker configuration file
    [dictionary]
    url = https://raw.githubusercontent.com/napolux/paroleitaliane/main/paroleitaliane/lista_badwords.txt
    path = badwords-it.txt

    [options]
    force = false
    match_mode = exact
    quarantine =
    recursive = false
    verbose = false
    ```

**Dev vs Prod Differences**:
-   No explicit "production" environment. The tool is designed for local execution.
-   Development involves running tests, linting, and manual testing.

**Secrets/Config Handling**:
-   No secrets are handled. Configuration is via CLI arguments and `badwordschecker.ini`.

# Progress Status
-   **Project Scaffolding**: 100%
-   **Core Modules (Dictionary, Transcription, Scanning, Reporting)**: 100%
-   **CLI Implementation**: 100% (including config integration)
-   **Unit Tests**: 100% (for original features)
-   **Integration Tests (Config)**: In progress (new file `test_config_integration.py` added).
-   **Documentation (README, Architecture)**: 95% (updated with config details).
-   **Dependency Management**: 100% (pinned `requirements.txt`)
-   **Makefile**: 100% (for common tasks)

# Open Tasks / Backlog (table: Item | Priority | Type | Status)
| Item | Priority | Type | Status |
| :--- | :--- | :--- | :--- |
| Fix `test_config_integration.py` indentation | High | tech-debt | Broken |
| Implement `substring` match mode | High | feat | Planned |
| Auto-install/verify `ffmpeg` and Vosk model | Medium | feat | Planned |
| Robust filename handling (spaces, special chars) | Medium | tech-debt | Planned |
| Structured logging (e.g., JSON output) | Low | tech-debt | Planned |
| Add fuzzy matching (Levenshtein) | Low | feat | Planned |
| Support for other languages | Low | feat | Planned |

# Missing / Partial Implementations
-   The `substring` match mode in `scanning.py` is currently a placeholder and needs full implementation.
-   Automatic installation/verification of `ffmpeg` and Vosk model is not implemented; users must install/download manually.
-   Comprehensive handling of filenames with spaces or special characters across all modules needs further testing and potential refinement.
-   The `test_config_integration.py` file has malformed indentation and is currently not runnable.

# Known Issues (table: Issue | Impact | Suspected Cause | Workaround | Severity)
| Issue | Impact | Suspected Cause | Workaround | Severity |
| :--- | :--- | :--- | :--- | :--- |
| `make test` skips transcription test if Vosk model not present | Test suite doesn't fully validate transcription without manual model download. | `vosk` library requires a valid model path for `Model` instantiation. | User must download and place the Vosk model manually for full test coverage. | Low |
| Potential issues with non-ASCII characters in MP3 filenames | Files might be skipped or reports might have garbled names. | Path handling might not be fully robust for all UTF-8 characters across OS. | Rename files to use only ASCII characters (temporary). | Medium |
| `ffmpeg` not found error | Tool fails to convert MP3s. | `ffmpeg` not installed or not in system PATH. | User must manually install `ffmpeg` and ensure it's in PATH. | High |
| Malformed indentation in `test_config_integration.py` | Integration tests for config precedence cannot be run. | Manual error during test file creation/editing. | Fix indentation manually. | High |

# Risks & Mitigations
-   **Risk**: External dependencies (`ffmpeg`, Vosk model) become unavailable or change APIs.
    -   **Mitigation**: Modular design allows for easier swapping of components. Documentation emphasizes manual installation.
-   **Risk**: Performance degradation for very large MP3 collections.
    -   **Mitigation**: Current scope is small collections. Future enhancement: parallel processing.
-   **Risk**: Dictionary URL becomes invalid.
    -   **Mitigation**: Users can provide custom dictionary files and configure URL in `badwordschecker.ini`.

# Testing & Quality
-   **Unit Testing**: Comprehensive unit tests for `dictionary`, `text_normalization`, `scanning`, `reporting`, and `cli` modules using `pytest`.
-   **Integration Testing**: `test_transcription.py` uses a real WAV file with Vosk. New `test_config_integration.py` added for config precedence (currently broken).
-   **Test Coverage**: Good coverage for core logic.
-   **Test Strategy**: Focus on mocking external calls (`subprocess`, `requests`) to isolate unit tests.
-   **Code Quality**: Enforced by `ruff` (linting, formatting) and `mypy` (type checking).

# Performance & Scalability
-   **Current Performance**: Dependent on `ffmpeg` and `Vosk` speed. Single-threaded processing.
-   **Scalability Limits**: Not designed for large-scale, high-throughput processing. Sequential file processing limits scalability.
-   **Future Considerations**: Parallel processing for MP3s, optimized I/O.

# Security & Compliance
-   **Security**:
    -   Runs locally, minimizing network attack surface.
    -   Connects to configured URL for dictionary download.
    -   No sensitive data is processed or stored by the tool itself.
-   **Compliance**: No specific compliance requirements identified.

# Operations & Monitoring
-   **Operations**: Simple CLI tool, no continuous operation required.
-   **Monitoring**: Basic logging to console (stdout/stderr). Verbose mode provides more detailed output.
-   **Alerts**: None implemented; errors are logged and cause non-zero exit codes.

# Future Enhancements
-   **Parallel Processing**: Utilize multiprocessing to speed up scanning of multiple MP3s.
-   **Alternative ASR Backends**: Allow integration with other speech-to-text services (e.g., Google Cloud Speech-to-Text, AWS Transcribe).
-   **GUI**: Develop a user-friendly graphical interface.
-   **Advanced Dictionary Features**: Support for regular expressions in dictionary, word stemming.
-   **Report Export Formats**: Export reports to CSV, JSON, or HTML.
-   **CI/CD Pipeline**: Set up automated testing and deployment.

# Glossary
-   **ASR**: Automatic Speech Recognition.
-   **CLI**: Command-Line Interface.
-   **ffmpeg**: A powerful open-source multimedia framework used for converting audio/video.
-   **Vosk**: An open-source, offline speech recognition toolkit.
-   **WAV**: A standard audio file format.
-   **MP3**: A common digital audio encoding format.
-   **UTF-8**: A variable-width character encoding capable of encoding all Unicode characters.
-   **INI file**: A simple configuration file format, used here for `badwordschecker.ini`.

# Next Immediate Steps (top 3–7)
1.  **Fix `test_config_integration.py` indentation** (High priority).
2.  Implement the `substring` match mode in `scanning.py`.
3.  Refine error handling across modules for more specific user feedback.
4.  Add more comprehensive examples to the `README.md` for various use cases.
5.  Investigate and fix robust handling of non-ASCII characters in filenames.

# Quick Start to Resume (checklist)
-   [ ] `git pull` (if applicable)
-   [ ] `make venv` (if virtual environment is not set up)
-   [ ] `make install` (to install/update dependencies)
-   [ ] Ensure Vosk Italian model is in project root.
-   [ ] `make run ARGS="--download-dict"` (to get the dictionary)
-   [ ] `make test` (to verify setup)
-   [ ] Begin working on the next task from "Next Immediate Steps".

# Changelog Pointer
TODO – needs input