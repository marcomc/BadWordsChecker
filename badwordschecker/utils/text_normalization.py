import re
import unicodedata


def normalize_text(text: str) -> str:
    """Normalizes text by lowercasing, removing punctuation, and normalizing accents."""
    text = text.lower()
    text = "".join(
        c for c in unicodedata.normalize("NFD", text) if unicodedata.category(c) != "Mn"
    )
    text = re.sub(r"[^\w\s]", "", text)
    return text


def tokenize_text(text: str) -> list[str]:
    """Tokenizes text into a list of words."""
    return text.split()
