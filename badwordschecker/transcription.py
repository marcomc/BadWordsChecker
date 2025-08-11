import json
import logging
import subprocess
import tempfile
import wave
from pathlib import Path
from typing import Optional

from vosk import KaldiRecognizer, Model
import sys
import subprocess
import json
import logging

from badwordschecker.utils.system import silence_stderr

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
        # Use -hide_banner and -loglevel error to suppress ffmpeg output unless there is an error
        subprocess.run(
            command + ["-y", "-hide_banner", "-loglevel", "error"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        logger.debug(f"Converted {mp3_path} to {wav_path}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to convert {mp3_path} to WAV: {e.stderr.decode('utf-8')}")
        return False
    except FileNotFoundError:
        logger.error("ffmpeg not found. Please ensure it is installed and in your PATH.")
        return False


def transcribe_audio(wav_path: Path, model: Model, verbose: bool) -> Optional[str]:
    """Transcribes a WAV file using the Vosk model."""
    try:
        with wave.open(str(wav_path), "rb") as wf:
            # Vosk requires mono WAV files with a specific sample rate.
            # Check if the audio file meets these requirements.
            if (
                wf.getnchannels() != 1
                or wf.getsampwidth() != 2
                or wf.getcomptype() != "NONE"
            ):
                logger.error(
                    "Audio file must be WAV format mono PCM with 16kHz sample rate."
                )
                return None

            rec = KaldiRecognizer(model, wf.getframerate())
            rec.SetWords(True)

            total_frames = wf.getnframes()
            chunk_size = 4000
            processed_frames = 0
            last_reported_progress = -1
            results = []

            while True:
                data = wf.readframes(chunk_size)
                if len(data) == 0:
                    break
                
                processed_frames += chunk_size
                progress = int((processed_frames / total_frames) * 100) if total_frames > 0 else 0

                if progress > last_reported_progress and progress % 10 == 0:
                    sys.stderr.write(f"\rTranscription progress: {progress}%")
                    sys.stderr.flush()
                    last_reported_progress = progress

                if not verbose:
                    with silence_stderr():
                        if rec.AcceptWaveform(data):
                            partial_result = json.loads(rec.Result())
                            results.append(partial_result.get("text", ""))
                else:
                    if rec.AcceptWaveform(data):
                        partial_result = json.loads(rec.Result())
                        results.append(partial_result.get("text", ""))

            sys.stderr.write("\rTranscription complete.    \n")
            sys.stderr.flush()

            final_result = json.loads(rec.FinalResult())
            results.append(final_result.get("text", ""))
            
            return " ".join(results).strip()
    except Exception as e:
        logger.error(f"Failed to transcribe {wav_path}: {e}", exc_info=True)
        return None


def process_mp3_file(
    mp3_path: Path, model: Model
) -> Optional[str]:
    """Processes a single MP3 file: converts to WAV and transcribes."""
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as temp_wav_file:
        wav_path = Path(temp_wav_file.name)
        if not convert_mp3_to_wav(mp3_path, wav_path):
            return None
        
        transcription = transcribe_audio(wav_path, model)
        
        if transcription:
            save_transcription(transcription, mp3_path)
            
        return transcription

def save_transcription(text: str, mp3_path: Path):
    """Saves the transcription to a text file next to the MP3."""
    output_path = mp3_path.with_suffix(".txt")
    try:
        output_path.write_text(text, encoding="utf-8")
        logger.info(f"Transcription saved to {output_path}")
    except IOError as e:
        logger.error(f"Failed to save transcription to {output_path}: {e}")
