import json
import logging
import subprocess
import tempfile
import wave
from pathlib import Path
from typing import Optional

from vosk import KaldiRecognizer, Model

logger = logging.getLogger(__name__)


def convert_mp3_to_wav(mp3_path: Path, wav_path: Path) -> bool:
    """Converts an MP3 file to a WAV file using ffmpeg."""
    command = [
        "ffmpeg",
        "-i",
        str(mp3_path),
        "-ac",
        "1",
        "-ar",
        "16000",
        "-f",
        "wav",
        str(wav_path),
    ]
    try:
        subprocess.run(
            command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        logger.info(f"Converted {mp3_path} to {wav_path}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logger.error(f"Failed to convert {mp3_path} to WAV: {e}")
        return False


def transcribe_audio(wav_path: Path, model: Model) -> Optional[str]:
    """Transcribes a WAV file using the Vosk model."""
    try:
        with wave.open(str(wav_path), "rb") as wf:
            if (
                wf.getnchannels() != 1
                or wf.getsampwidth() != 2
                or wf.getcomptype() != "NONE"
            ):
                logger.error("Audio file must be WAV format mono PCM.")
                return None

            rec = KaldiRecognizer(model, wf.getframerate())
            rec.SetWords(True)

            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if rec.AcceptWaveform(data):
                    pass

            result = json.loads(rec.FinalResult())
            return result.get("text")
    except Exception as e:
        logger.error(f"Failed to transcribe {wav_path}: {e}")
        return None


def process_mp3_file(
    mp3_path: Path, model: Model, temp_dir: Path
) -> Optional[str]:
    """Processes a single MP3 file: converts to WAV and transcribes."""
    wav_path = temp_dir / f"{mp3_path.stem}.wav"
    if not convert_mp3_to_wav(mp3_path, wav_path):
        return None
    transcription = transcribe_audio(wav_path, model)
    wav_path.unlink()  # Clean up the temporary WAV file
    return transcription
