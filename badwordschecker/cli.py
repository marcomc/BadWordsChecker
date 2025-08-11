import argparse
import logging
import shutil
import sys
import tempfile
from pathlib import Path

from vosk import Model

from badwordschecker.dictionary import (
    DEFAULT_DICT_PATH,
    DEFAULT_DICT_URL,
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
from badwordschecker.utils.system import command_exists
from badwordschecker.utils.logging import setup_logging

__version__ = "0.1.0"

logger = logging.getLogger(__name__)


def main():
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
        default=None,  # allow config to supply value when flag absent
        help="Force download, overwriting existing dictionary.",
    )
    parser.add_argument(
        "--dict",
        type=Path,
        default=DEFAULT_DICT_PATH,
        help="Path to a custom dictionary file.",
    )
    parser.add_argument(
        "--edit-dict", action="store_true", help="Open the dictionary in the default editor."
    )
    parser.add_argument(
        "--match-mode",
        choices=["exact", "substring"],
        default="exact",
        help="Matching mode: exact or substring.",
    )
    parser.add_argument(
        "--quarantine",
        type=Path,
        help="Move offending MP3s to this folder.",
    )
    parser.add_argument(
        "--recursive", action="store_true", default=None, help="Scan for MP3 files recursively."
    )
    parser.add_argument(
        "--verbose", action="store_true", default=None, help="Enable verbose logging."
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )

    args = parser.parse_args()

    setup_logging(args.verbose)

    if not command_exists("ffmpeg"):
        logger.error("ffmpeg not found. Please install it and ensure it's in your PATH.")
        sys.exit(1)

    if args.download_dict:
        dest_path = args.download_dict if isinstance(args.download_dict, Path) else DEFAULT_DICT_PATH
        download_dictionary(DEFAULT_DICT_URL, dest_path, args.force)
        sys.exit(0)

    if args.edit_dict:
        edit_dictionary(args.dict)
        sys.exit(0)

    

    

    # If no mp3_folder is provided, assume current working directory
    if args.mp3_folder is None:
        args.mp3_folder = Path.cwd()

    if not args.mp3_folder.is_dir():
        logger.error(f"MP3 folder not found at {args.mp3_folder}")
        sys.exit(1)

    bad_words = load_bad_words(args.dict)
    if not bad_words:
        logger.error("No bad words loaded. Exiting.")
        sys.exit(1)

    model_path = Path("vosk-model-it-0.22")
    if not model_path.exists():
        logger.error(
            f"Vosk model not found at {model_path}. "
            "Please download it from https://alphacephei.com/vosk/models and unzip it in the project root."
        )
        sys.exit(1)

    try:
        model = Model(str(model_path))
    except Exception as e:
        logger.error(f"Failed to load Vosk model: {e}")
        sys.exit(1)

    mp3_files = (
        list(args.mp3_folder.rglob("*.mp3"))
        if args.recursive
        else list(args.mp3_folder.glob("*.mp3"))
    )

    if not mp3_files:
        logger.info("No MP3 files found in the specified folder.")
        sys.exit(0)

    all_matches = {}
    output_dir = Path("parolacce")
    output_dir.mkdir(exist_ok=True)

    with tempfile.TemporaryDirectory() as temp_dir_str:
        temp_dir = Path(temp_dir_str)
        for mp3_path in mp3_files:
            logger.info(f"Processing {mp3_path.name}...")
            transcription = process_mp3_file(mp3_path, model, temp_dir)
            if transcription:
                matches = scan_text(transcription, bad_words, args.match_mode)
                if matches:
                    all_matches[mp3_path.name] = matches
                    generate_per_file_report(mp3_path, matches, output_dir)
                    if args.quarantine:
                        args.quarantine.mkdir(exist_ok=True)
                        shutil.move(str(mp3_path), str(args.quarantine))
                        logger.info(f"Moved {mp3_path.name} to {args.quarantine}")

    generate_aggregated_report(all_matches, output_dir, len(mp3_files))

    logger.info("Processing complete.")


if __name__ == "__main__":
    main()