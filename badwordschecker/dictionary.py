import logging
import os
import platform
import subprocess
import sys
from pathlib import Path
from typing import Set

import requests

DEFAULT_DICT_URL = "https://raw.githubusercontent.com/napolux/paroleitaliane/master/paroleitaliane/parole_proibite.txt"

logger = logging.getLogger(__name__)

DEFAULT_DICT_PATH = Path("badwords-it.txt")


def load_bad_words(dict_path: Path) -> Set[str]:
    """Loads bad words from a file into a set, ignoring comments and empty lines."""
    if not dict_path.exists():
        logger.error(f"Dictionary file not found at {dict_path}")
        return set()
    with open(dict_path, "r", encoding="utf-8") as f:
        words = {
            line.strip().lower()
            for line in f
            if line.strip() and not line.startswith("#")
        }
    if not words:
        logger.warning(f"Dictionary at {dict_path} is empty.")
    return words


def download_dictionary(url: str, dest_path: Path, force: bool = False) -> None:
    """Downloads the dictionary from a URL."""
    if dest_path.exists() and not force:
        logger.info(
            f"Dictionary already exists at {dest_path}. Use --force to overwrite."
        )
        return
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        dest_path.write_text(response.text, encoding="utf-8")
        logger.info(f"Dictionary downloaded successfully to {dest_path}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to download dictionary: {e}")
        sys.exit(1)


def edit_dictionary(dict_path: Path) -> None:
    """Opens the dictionary file in the default system editor."""
    if not dict_path.exists():
        logger.error(f"Dictionary file not found at {dict_path}")
        sys.exit(1)

    system = platform.system()
    if system == "Darwin":
        command = ["open", str(dict_path)]
    elif system == "Linux":
        command = ["xdg-open", str(dict_path)]
    elif system == "Windows":
        command = ["cmd", "/c", "start", str(dict_path)]
    else:
        logger.error(f"Unsupported operating system: {system}")
        sys.exit(1)

    try:
        subprocess.run(command, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logger.error(f"Failed to open editor: {e}")
        sys.exit(1)

