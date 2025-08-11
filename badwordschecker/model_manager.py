import logging
import requests
import zipfile
from pathlib import Path
from tqdm import tqdm

logger = logging.getLogger(__name__)

MODEL_URL = "https://alphacephei.com/vosk/models/vosk-model-it-0.22.zip"
DEFAULT_MODEL_DIR = Path.home() / ".config" / "BadWordsChecker"
DEFAULT_MODEL_PATH = DEFAULT_MODEL_DIR / "vosk-model-it-0.22"

def get_model_path(custom_path: Path = None) -> Path:
    """Determine the final model path based on configuration."""
    if custom_path:
        return custom_path
    return DEFAULT_MODEL_PATH

def handle_model_download(model_path: Path):
    """Check if the model exists, and if not, download and unzip it."""
    if model_path.exists():
        logger.info(f"Vosk model found at {model_path}")
        return

    logger.info(f"Vosk model not found. Attempting to download to {model_path}...")
    model_zip_path = model_path.parent / "vosk-model-it-0.22.zip"
    model_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        _download_model(model_zip_path)
        _unzip_model(model_zip_path, model_path.parent)
    finally:
        if model_zip_path.exists():
            model_zip_path.unlink()
            logger.debug("Cleaned up downloaded ZIP file.")

def _download_model(zip_path: Path):
    """Download the model zip file with a progress bar."""
    try:
        with requests.get(MODEL_URL, stream=True) as r:
            r.raise_for_status()
            total_size = int(r.headers.get('content-length', 0))
            with open(zip_path, 'wb') as f, tqdm(
                total=total_size, unit='iB', unit_scale=True, desc="Downloading Vosk Model"
            ) as pbar:
                for chunk in r.iter_content(chunk_size=8192):
                    pbar.update(len(chunk))
                    f.write(chunk)
        logger.info("Model downloaded successfully.")
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to download model: {e}")
        raise

def _unzip_model(zip_path: Path, extract_to: Path):
    """Unzip the model file."""
    logger.info(f"Unzipping model to {extract_to}...")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        logger.info("Model unzipped successfully.")
    except zipfile.BadZipFile as e:
        logger.error(f"Failed to unzip model: {e}")
        raise