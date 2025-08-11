import unittest
import wave
from pathlib import Path
from unittest.mock import patch, MagicMock

from badwordschecker.transcription import (
    convert_mp3_to_wav,
    transcribe_audio,
    process_mp3_file,
)

def create_silent_wav(path: Path, duration: int = 1, sample_rate: int = 16000):
    with wave.open(str(path), "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(b"\x00\x00" * sample_rate * duration)


class TestTranscription(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path("test_data")
        self.test_dir.mkdir(exist_ok=True)

    def tearDown(self):
        import shutil

        shutil.rmtree(self.test_dir)

    @patch("subprocess.run")
    def test_convert_mp3_to_wav_success(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0)
        result = convert_mp3_to_wav(Path("test.mp3"), Path("test.wav"))
        self.assertTrue(result)

    @patch("subprocess.run")
    def test_convert_mp3_to_wav_failure(self, mock_run):
        mock_run.side_effect = FileNotFoundError
        result = convert_mp3_to_wav(Path("test.mp3"), Path("test.wav"))
        self.assertFalse(result)

    def test_transcribe_audio(self):
        model_path = Path("vosk-model-it-0.22")
        if not model_path.exists():
            self.skipTest("Vosk model not found. Skipping transcription test.")

        from vosk import Model

        model = Model(str(model_path))
        wav_path = self.test_dir / "test.wav"
        create_silent_wav(wav_path)

        result = transcribe_audio(wav_path, model)
        self.assertEqual(result, "")

    @patch("badwordschecker.transcription.convert_mp3_to_wav", return_value=True)
    @patch("badwordschecker.transcription.transcribe_audio", return_value="transcribed text")
    @patch("pathlib.Path.unlink")
    def test_process_mp3_file(self, mock_unlink, mock_transcribe, mock_convert):
        model = MagicMock()
        temp_dir = Path("/tmp")
        result = process_mp3_file(Path("test.mp3"), model, temp_dir)
        self.assertEqual(result, "transcribed text")
        mock_convert.assert_called_once_with(Path("test.mp3"), temp_dir / "test.wav")
        mock_transcribe.assert_called_once_with(temp_dir / "test.wav", model)
        mock_unlink.assert_called_once()


if __name__ == "__main__":
    unittest.main()
