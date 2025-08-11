import logging
import shutil
import sys
import tempfile
from pathlib import Path
import argparse

from vosk import Model

from badwordschecker.dictionary import (
    DEFAULT_DICT_PATH,
    download_dictionary,
    edit_dictionary,
    load_bad_words,
)
from badwordschecker.reporting import (
    generate_aggregated_report,
    generate_per_file_report,
)
from badwordschecker.scanning import scan_text
from badwordschecker.transcription import process_mp3_file
from badwordschecker.utils.config import get_config
from badwordschecker.utils.system import command_exists
from badwordschecker.utils.logging import setup_logging
from badwordschecker.model_manager import get_model_path, handle_model_download

__version__ = "0.1.0"

logger = logging.getLogger(__name__)

def main():
    """Main entry point for the BadWordsChecker CLI."""
    parser = create_parser()
    args = parser.parse_args()
    config = get_config(args)

    setup_logging(config["verbose"], config["log_format"])

    if not command_exists("ffmpeg"):
        logger.error("ffmpeg not found. Please install it and ensure it's in your PATH.")
        sys.exit(1)

    if config["download_dict"]:
        download_dictionary(config["dict_url"], config["download_dict"], config["force"])
        sys.exit(0)

    if config["edit_dict"]:
        edit_dictionary(Path(config["dict"]))
        sys.exit(0)

    mp3_folder = Path(config["mp3_folder"])
    if not mp3_folder.is_dir():
        logger.error(f"MP3 folder not found at {mp3_folder}")
        sys.exit(1)

    bad_words = load_bad_words(Path(config["dict"]))
    if not bad_words:
        logger.error("No bad words loaded. Exiting.")
        sys.exit(1)

    model_path = get_model_path(config["model_path"])
    handle_model_download(model_path)

    try:
        model = Model(str(model_path))
    except Exception as e:
        logger.error(f"Failed to load Vosk model: {e}")
        sys.exit(1)

    mp3_files = (
        list(mp3_folder.rglob("*.mp3"))
        if config["recursive"]
        else list(mp3_folder.glob("*.mp3"))
    )

    if not mp3_files:
        logger.info("No MP3 files found in the specified folder.")
        sys.exit(0)

    all_matches = {}
    output_dir = Path("parolacce")
    output_dir.mkdir(exist_ok=True)

    for mp3_path in mp3_files:
        logger.debug(f"Starting transcription for {mp3_path.name}...")
        transcription = process_mp3_file(mp3_path, model)
        if transcription:
            matches = scan_text(transcription, bad_words, config["match_mode"])
            if matches:
                all_matches[mp3_path.name] = matches
                generate_per_file_report(mp3_path, matches, output_dir)
                if config["quarantine"]:
                    quarantine_path = Path(config["quarantine"])
                    quarantine_path.mkdir(exist_ok=True)
                    shutil.move(str(mp3_path), str(quarantine_path))
                    logger.info(f"Moved {mp3_path.name} to {quarantine_path}")

    generate_aggregated_report(all_matches, output_dir, len(mp3_files))
    logger.info("Processing complete.")

def create_parser():
    parser = argparse.ArgumentParser(
        description="Scan MP3 files for bad words.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("mp3_folder", nargs="?", type=Path, help="Path to the folder containing MP3 files.")
    parser.add_argument(
        "--download-dict",
        nargs="?",
        const=DEFAULT_DICT_PATH,
        type=Path,
        help="Download the default Italian bad words dictionary. Optionally specify a path.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force download, overwriting existing dictionary.",
    )
    parser.add_argument(
        "--dict",
        type=Path,
        help="Path to a custom dictionary file.",
    )
    parser.add_argument(
        "--edit-dict", action="store_true", help="Open the dictionary in the default editor."
    )
    parser.add_argument(
        "--match-mode",
        choices=["exact", "substring"],
        help="Matching mode: exact or substring.",
    )
    parser.add_argument(
        "--quarantine",
        type=Path,
        help="Move offending MP3s to this folder.",
    )
    parser.add_argument(
        "--recursive", action="store_true", help="Scan for MP3 files recursively."
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Enable verbose logging."
    )
    parser.add_argument(
        "--log-format",
        choices=["text", "json"],
        help="Set the log output format.",
    )
    parser.add_argument(
        "--dict-url",
        type=str,
        help="URL to download the dictionary from.",
    )
    parser.add_argument(
        "--model-path",
        type=Path,
        help="Path to the Vosk model directory.",
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    return parser

if __name__ == "__main__":
    main()